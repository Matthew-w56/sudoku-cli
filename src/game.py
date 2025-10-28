"""
Main game loop and controller.
"""
from blessed import Terminal
import time
from src.board import Board
from src.renderer import Renderer
from src.generator import Generator, Difficulty
from src.solver import Solver
from src.game_state import GameState


class Game:
    """Main game controller managing the game loop and user input."""

    def __init__(self):
        """Initialize the game."""
        self.term = Terminal()
        self.renderer = Renderer(self.term)
        self.game_state: GameState = None
        self.running = True
        self.show_help = False

    def run(self):
        """Main game loop."""
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            try:
                # Check for saved game
                saved_game = GameState.load_from_file()
                if saved_game:
                    if self._ask_load_saved_game():
                        self.game_state = saved_game
                        self.game_state.resume()
                    else:
                        GameState.delete_save_file()
                        difficulty = self._select_difficulty()
                        if difficulty is None:
                            return
                        self._start_new_game(difficulty)
                else:
                    difficulty = self._select_difficulty()
                    if difficulty is None:
                        return
                    self._start_new_game(difficulty)

                # Main game loop
                while self.running:
                    self._render()
                    self._handle_input()
                    time.sleep(0.016)  # ~60 FPS

            except KeyboardInterrupt:
                pass
            finally:
                # Auto-save on exit if game is not complete
                if self.game_state and not self.game_state.is_complete():
                    self.game_state.save_to_file()

    def _render(self):
        """Render the current game state."""
        if self.show_help:
            self.renderer.render_help_screen()
            return

        # Check for win condition
        if self.game_state.is_complete():
            self.renderer.render_win_screen(
                self.game_state.get_time_string(),
                self.game_state.move_count
            )
            return

        # Normal game rendering
        self.renderer.clear()
        self.renderer.render_title()

        # Get conflicts for the current cell
        conflicts = self.game_state.get_conflicts()

        # Render the board
        self.renderer.render_board(
            self.game_state.board,
            self.game_state.cursor,
            conflicts,
            self.game_state.hint_cell
        )

        # Render status and controls
        self.renderer.render_status(
            self.game_state.difficulty,
            self.game_state.get_time_string(),
            self.game_state.move_count
        )
        self.renderer.render_controls()

    def _handle_input(self):
        """Handle user input."""
        key = self.term.inkey(timeout=0.016)

        if not key:
            return

        # Help screen toggle
        if key == '?' or key.lower() == 'h':
            if not self.show_help:
                self.game_state.pause()
            else:
                self.game_state.resume()
            self.show_help = not self.show_help
            return

        # If help is showing, any key closes it
        if self.show_help:
            self.show_help = False
            self.game_state.resume()
            return

        # If game is complete, only allow new game or quit
        if self.game_state.is_complete():
            if key.lower() == 'n':
                difficulty = self._select_difficulty()
                if difficulty:
                    self._start_new_game(difficulty)
            elif key.lower() == 'q':
                GameState.delete_save_file()
                self.running = False
            return

        # Navigation
        if key.name == 'KEY_UP':
            self.game_state.move_cursor(-1, 0)
        elif key.name == 'KEY_DOWN':
            self.game_state.move_cursor(1, 0)
        elif key.name == 'KEY_LEFT':
            self.game_state.move_cursor(0, -1)
        elif key.name == 'KEY_RIGHT':
            self.game_state.move_cursor(0, 1)

        # Number input
        elif key in '123456789':
            row, col = self.game_state.cursor
            num = int(key)

            if self.game_state.board.is_given(row, col):
                self._show_temp_message("Cannot modify given cells!", is_error=True)
            else:
                self.game_state.set_cell(num)

        # Clear cell
        elif key in '0' or key.name in ('KEY_BACKSPACE', 'KEY_DELETE'):
            row, col = self.game_state.cursor
            if self.game_state.board.is_given(row, col):
                self._show_temp_message("Cannot modify given cells!", is_error=True)
            else:
                self.game_state.set_cell(0)

        # Undo
        elif key.lower() == 'u':
            if not self.game_state.undo():
                self._show_temp_message("Nothing to undo!", is_error=True)

        # Hint
        elif key.lower() == 'h' and not self.show_help:
            self._give_hint()

        # New game
        elif key.lower() == 'n':
            if self._confirm_new_game():
                difficulty = self._select_difficulty()
                if difficulty:
                    self._start_new_game(difficulty)

        # Quit
        elif key.lower() == 'q':
            self.running = False

    def _start_new_game(self, difficulty: str):
        """Start a new game with the given difficulty."""
        self.renderer.render_loading(f"Generating {difficulty.upper()} puzzle...")

        # Generate puzzle
        board = Generator.generate(difficulty)
        self.game_state = GameState(board, difficulty)
        self.show_help = False

        # Delete old save file
        GameState.delete_save_file()

    def _select_difficulty(self) -> str:
        """Show difficulty selection menu. Returns None if user quits."""
        difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD, Difficulty.EXPERT]
        selected = 0

        while True:
            self.renderer.render_difficulty_menu(selected)

            key = self.term.inkey()

            if key.name == 'KEY_UP':
                selected = (selected - 1) % len(difficulties)
            elif key.name == 'KEY_DOWN':
                selected = (selected + 1) % len(difficulties)
            elif key.name == 'KEY_ENTER' or key == '\n' or key == '\r':
                return difficulties[selected]
            elif key.lower() == 'q':
                return None

    def _give_hint(self):
        """Provide a hint to the player."""
        hint = Solver.get_hint(self.game_state.board)

        if hint:
            row, col, value = hint
            self.game_state.hint_cell = (row, col)
            self._show_temp_message(f"Hint: Try {value} at row {row+1}, col {col+1}")
        else:
            self._show_temp_message("No hints available!", is_error=True)

    def _confirm_new_game(self) -> bool:
        """Ask user to confirm new game."""
        return self._ask_yes_no("Start new game? Current progress will be lost. (y/n): ")

    def _ask_load_saved_game(self) -> bool:
        """Ask user if they want to load saved game."""
        return self._ask_yes_no("Continue saved game? (y/n): ")

    def _ask_yes_no(self, prompt: str) -> bool:
        """Display a yes/no prompt and return the result."""
        self.renderer.render_message(prompt)

        while True:
            key = self.term.inkey()
            if key.lower() == 'y':
                return True
            elif key.lower() == 'n':
                return False

    def _show_temp_message(self, message: str, is_error: bool = False, duration: float = 2.0):
        """Show a temporary message that disappears after duration seconds."""
        self.renderer.render_message(message, is_error=is_error)
        time.sleep(duration)

    def check_terminal_size(self) -> bool:
        """Check if terminal is large enough. Returns True if OK."""
        width, height = self.renderer.get_terminal_size()
        min_width = 50
        min_height = 30

        if width < min_width or height < min_height:
            self.renderer.clear()
            msg = f"Terminal too small! Need at least {min_width}x{min_height}, got {width}x{height}"
            print(msg)
            return False

        return True
