"""
Terminal UI renderer using blessed library.
"""
from blessed import Terminal
from src.board import Board
from typing import Set, Tuple, Optional


class Renderer:
    """Handles all terminal rendering for the Sudoku game."""

    def __init__(self, term: Terminal):
        """Initialize the renderer with a blessed Terminal instance."""
        self.term = term

        # Color definitions
        self.COLOR_GIVEN = self.term.cyan
        self.COLOR_USER = self.term.white
        self.COLOR_ERROR = self.term.red
        self.COLOR_HIGHLIGHT = self.term.black_on_yellow
        self.COLOR_CURSOR = self.term.black_on_white
        self.COLOR_TITLE = self.term.bold_magenta
        self.COLOR_STATUS = self.term.green
        self.COLOR_HINT = self.term.yellow
        self.COLOR_SAME_NUMBER = self.term.on_blue  # Highlight cells with same number
        self.COLOR_THICK_BORDER = self.term.magenta  # Color for 3x3 box borders
        self.COLOR_COMPLETE = self.term.on_bright_black  # Subtle gray for completed numbers

        # Fallback for terminals without certain capabilities
        # If dim/bold don't work, use a pass-through function
        try:
            test = self.term.dim("test")
            self.COLOR_DIM = self.term.dim
        except (TypeError, AttributeError):
            self.COLOR_DIM = lambda text: text  # Just return text unchanged

        try:
            test = self.term.bold("test")
            self.COLOR_BOLD = self.term.bold
        except (TypeError, AttributeError):
            self.COLOR_BOLD = lambda text: text  # Just return text unchanged

        # Board display settings
        self.board_start_row = 3
        self.board_start_col = 5

    def clear(self):
        """Clear the entire screen."""
        print(self.term.clear())

    def render_title(self):
        """Render the game title."""
        title = "SUDOKU"
        subtitle = "CLI Edition"

        # Center the title
        col = (self.term.width - len(title)) // 2

        with self.term.location(col, 0):
            print(self.COLOR_TITLE(title))

        col = (self.term.width - len(subtitle)) // 2
        with self.term.location(col, 1):
            print(self.COLOR_DIM(subtitle))

    def render_board(self, board: Board, cursor: Tuple[int, int],
                    conflicts: Set[Tuple[int, int]] = None,
                    hint_cell: Optional[Tuple[int, int]] = None):
        """
        Render the Sudoku board with colors and highlighting.

        Args:
            board: The Board object to render
            cursor: Current cursor position (row, col)
            conflicts: Set of cells with conflicts (shown in red)
            hint_cell: Cell to highlight as a hint
        """
        if conflicts is None:
            conflicts = set()

        cursor_row, cursor_col = cursor

        # Draw the board with box-drawing characters
        lines = self._build_board_lines(board, cursor, conflicts, hint_cell)

        for i, line in enumerate(lines):
            with self.term.location(self.board_start_col, self.board_start_row + i):
                print(line)

        # Draw the number count tracker on the right
        self.render_number_counts(board)

    def _build_board_lines(self, board: Board, cursor: Tuple[int, int],
                          conflicts: Set[Tuple[int, int]],
                          hint_cell: Optional[Tuple[int, int]]) -> list:
        """Build the board display as a list of lines."""
        lines = []
        cursor_row, cursor_col = cursor

        # Get the number at cursor position for highlighting same numbers
        cursor_num = board.get(cursor_row, cursor_col)

        # Top border (colored for thick borders)
        lines.append(self.COLOR_THICK_BORDER("┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓"))

        for row in range(9):
            # Build the row with numbers
            line_parts = [self.COLOR_THICK_BORDER("┃")]

            for col in range(9):
                num = board.get(row, col)
                is_cursor = (row, col) == (cursor_row, cursor_col)
                is_conflict = (row, col) in conflicts
                is_hint = hint_cell and (row, col) == hint_cell
                is_given = board.is_given(row, col)
                is_same_number = (num != 0 and num == cursor_num and not is_cursor)

                # Format the cell
                if num == 0:
                    cell_text = "   "  # Empty space instead of dot
                else:
                    cell_text = f" {num} "

                # Apply colors (priority order matters!)
                if is_cursor:
                    cell_text = self.COLOR_CURSOR(cell_text)
                elif is_hint:
                    cell_text = self.COLOR_HINT(cell_text)
                elif is_conflict:
                    cell_text = self.COLOR_ERROR(cell_text)
                elif is_same_number:
                    # Highlight cells with same number as cursor
                    cell_text = self.COLOR_SAME_NUMBER(cell_text)
                elif is_given:
                    cell_text = self.COLOR_GIVEN(cell_text)
                else:
                    cell_text = self.COLOR_USER(cell_text)

                line_parts.append(cell_text)

                # Add vertical separators (thick borders in magenta)
                if col == 2 or col == 5:
                    line_parts.append(self.COLOR_THICK_BORDER("┃"))
                elif col == 8:
                    line_parts.append(self.COLOR_THICK_BORDER("┃"))
                else:
                    line_parts.append("│")

            lines.append("".join(line_parts))

            # Add horizontal separators (thick borders in magenta)
            if row == 2 or row == 5:
                lines.append(self.COLOR_THICK_BORDER("┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫"))
            elif row < 8:
                # Thin horizontal line, but color intersections with thick vertical lines (including outer borders)
                line = (self.COLOR_THICK_BORDER("┠") + "───┼───┼───" +
                       self.COLOR_THICK_BORDER("╂") + "───┼───┼───" +
                       self.COLOR_THICK_BORDER("╂") + "───┼───┼───" +
                       self.COLOR_THICK_BORDER("┨"))
                lines.append(line)

        # Bottom border (colored for thick borders)
        lines.append(self.COLOR_THICK_BORDER("┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛"))

        return lines

    def render_number_counts(self, board: Board):
        """Render the count of each number on the right side of the board."""
        # Position to the right of the board (board is ~45 chars wide, add spacing)
        count_col = self.board_start_col + 48
        start_row = self.board_start_row + 1

        # Title
        with self.term.location(count_col, start_row):
            print(self.COLOR_DIM("Filled Quantity:"))

        # Count occurrences of each number
        counts = {i: 0 for i in range(1, 10)}
        for row in range(9):
            for col in range(9):
                num = board.get(row, col)
                if num != 0:
                    counts[num] += 1

        # Display each number with its count
        for num in range(1, 10):
            count = counts[num]
            row = start_row + 1 + num

            text = f"{num}: {count}"

            # Highlight if complete (count is 9)
            if count == 9:
                text = self.COLOR_COMPLETE(text)

            with self.term.location(count_col, row):
                print(text)

    def render_status(self, difficulty: str, time_str: str, moves: int):
        """Render the status bar below the board."""
        row = self.board_start_row + 20

        status_line = f"Difficulty: {difficulty.upper()}  |  Time: {time_str}  |  Moves: {moves}"

        with self.term.location(self.board_start_col, row):
            print(self.COLOR_STATUS(status_line))

    def render_controls(self):
        """Render the control hints."""
        row = self.board_start_row + 22

        controls = [
            "Controls:",
            "  Arrows: Navigate  |  1-9: Fill cell  |  0/Backspace: Clear",
            "  h: Hint  |  n: New game  |  u: Undo  |  ?: Help  |  q: Quit"
        ]

        for i, line in enumerate(controls):
            with self.term.location(self.board_start_col, row + i):
                print(self.COLOR_DIM(line))

    def render_message(self, message: str, row: int = None, is_error: bool = False):
        """Render a temporary message to the user."""
        if row is None:
            row = self.board_start_row + 19

        with self.term.location(self.board_start_col, row):
            print(self.term.clear_eol(), end="")  # Clear the line first

        with self.term.location(self.board_start_col, row):
            if is_error:
                print(self.COLOR_ERROR(message))
            else:
                print(self.COLOR_STATUS(message))

    def render_win_screen(self, time_str: str, moves: int):
        """Render the victory screen."""
        self.clear()

        messages = [
            "",
            "╔═══════════════════════════════════╗",
            "║                                   ║",
            "║     🎉  CONGRATULATIONS!  🎉      ║",
            "║                                   ║",
            "║      You solved the puzzle!       ║",
            "║                                   ║",
            f"║       Time: {time_str:^15}       ║",
            f"║       Moves: {moves:^14}       ║",
            "║                                   ║",
            "╚═══════════════════════════════════╝",
            "",
            "      Press 'n' for new game",
            "         Press 'q' to quit",
        ]

        start_row = (self.term.height - len(messages)) // 2

        for i, msg in enumerate(messages):
            col = (self.term.width - len(msg)) // 2
            with self.term.location(col, start_row + i):
                if "CONGRATULATIONS" in msg or "🎉" in msg:
                    print(self.COLOR_TITLE(msg))
                else:
                    print(msg)

    def render_help_screen(self):
        """Render the help overlay."""
        help_text = [
            "╔════════════════════════════════════════════╗",
            "║              SUDOKU HELP                   ║",
            "╠════════════════════════════════════════════╣",
            "║                                            ║",
            "║  OBJECTIVE:                                ║",
            "║    Fill the 9x9 grid with digits 1-9      ║",
            "║    Each row, column, and 3x3 box must     ║",
            "║    contain all digits from 1 to 9         ║",
            "║                                            ║",
            "║  NAVIGATION:                               ║",
            "║    Arrow Keys ............ Move cursor     ║",
            "║                                            ║",
            "║  INPUT:                                    ║",
            "║    1-9 ................... Fill cell       ║",
            "║    0, Backspace, Delete .. Clear cell      ║",
            "║                                            ║",
            "║  ACTIONS:                                  ║",
            "║    h ..................... Get a hint      ║",
            "║    u ..................... Undo move       ║",
            "║    n ..................... New game        ║",
            "║    ? ..................... Toggle help     ║",
            "║    q ..................... Quit game       ║",
            "║                                            ║",
            "║  COLORS:                                   ║",
            "║    Cyan .................. Given numbers   ║",
            "║    White ................. Your numbers    ║",
            "║    Red ................... Conflicts       ║",
            "║    Yellow ................ Hints           ║",
            "║                                            ║",
            "╚════════════════════════════════════════════╝",
            "",
            "          Press any key to continue",
        ]

        start_row = max(0, (self.term.height - len(help_text)) // 2)
        start_col = max(0, (self.term.width - 46) // 2)

        for i, line in enumerate(help_text):
            with self.term.location(start_col, start_row + i):
                print(line)

    def render_difficulty_menu(self, selected: int):
        """Render the difficulty selection menu."""
        self.clear()

        difficulties = ["Easy", "Medium", "Hard", "Expert"]
        descriptions = [
            "Perfect for beginners",
            "Moderate challenge",
            "For experienced players",
            "Ultimate challenge"
        ]

        title = "SELECT DIFFICULTY"
        subtitle = "Use arrow keys to select, Enter to confirm"

        messages = [
            "",
            title,
            subtitle,
            "",
            ""
        ]

        for i, diff in enumerate(difficulties):
            if i == selected:
                messages.append(f"  ▶ {diff} - {descriptions[i]}  ")
            else:
                messages.append(f"    {diff} - {descriptions[i]}  ")

        messages.append("")
        messages.append("Press 'q' to quit")

        start_row = (self.term.height - len(messages)) // 2

        for i, msg in enumerate(messages):
            col = (self.term.width - len(msg)) // 2

            with self.term.location(col, start_row + i):
                if msg == title:
                    print(self.COLOR_TITLE(msg))
                elif "▶" in msg:
                    print(self.COLOR_HIGHLIGHT(msg))
                else:
                    print(msg)

    def render_saved_game_menu(self, selected: int):
        """Render the saved game menu."""
        self.clear()

        options = ["Continue Saved Game", "Start New Game"]
        descriptions = [
            "Resume from where you left off",
            "Begin a fresh puzzle"
        ]

        title = "SAVED GAME FOUND"
        subtitle = "Use arrow keys to select, Enter to confirm"

        messages = [
            "",
            title,
            subtitle,
            "",
            ""
        ]

        for i, option in enumerate(options):
            if i == selected:
                messages.append(f"  ▶ {option} - {descriptions[i]}  ")
            else:
                messages.append(f"    {option} - {descriptions[i]}  ")

        messages.append("")
        messages.append("Press 'q' to quit")

        start_row = (self.term.height - len(messages)) // 2

        for i, msg in enumerate(messages):
            col = (self.term.width - len(msg)) // 2

            with self.term.location(col, start_row + i):
                if msg == title:
                    print(self.COLOR_TITLE(msg))
                elif "▶" in msg:
                    print(self.COLOR_HIGHLIGHT(msg))
                else:
                    print(msg)

    def render_loading(self, message: str = "Generating puzzle..."):
        """Render a loading screen."""
        self.clear()

        messages = [
            "",
            message,
            "",
            "Please wait..."
        ]

        start_row = (self.term.height - len(messages)) // 2

        for i, msg in enumerate(messages):
            col = (self.term.width - len(msg)) // 2
            with self.term.location(col, start_row + i):
                print(self.COLOR_BOLD(msg))

    def get_terminal_size(self) -> Tuple[int, int]:
        """Get terminal dimensions (width, height)."""
        return (self.term.width, self.term.height)
