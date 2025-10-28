"""
Game state management including undo, timer, and statistics.
"""
import time
import json
import os
from typing import List, Tuple, Optional
from pathlib import Path
from src.board import Board


class Move:
    """Represents a single move in the game."""

    def __init__(self, row: int, col: int, old_value: int, new_value: int):
        self.row = row
        self.col = col
        self.old_value = old_value
        self.new_value = new_value


class GameState:
    """Manages the overall game state including board, cursor, timer, and history."""

    MAX_HISTORY = 100  # Limit undo history to prevent memory issues

    def __init__(self, board: Board, difficulty: str):
        """Initialize game state with a board and difficulty."""
        self.board = board
        self.difficulty = difficulty
        self.cursor = (0, 0)  # (row, col)
        self.start_time = time.time()
        self.elapsed_time = 0.0  # For loaded games
        self.move_count = 0
        self.history: List[Move] = []
        self.is_paused = False
        self.hint_cell: Optional[Tuple[int, int]] = None

    def move_cursor(self, delta_row: int, delta_col: int):
        """Move the cursor by the given delta, wrapping at edges."""
        new_row = (self.cursor[0] + delta_row) % 9
        new_col = (self.cursor[1] + delta_col) % 9
        self.cursor = (new_row, new_col)

    def set_cell(self, value: int) -> bool:
        """
        Set the current cell to the given value.
        Returns True if successful, False if the cell is given.
        """
        row, col = self.cursor
        old_value = self.board.get(row, col)

        if self.board.set(row, col, value):
            # Record the move for undo
            self.history.append(Move(row, col, old_value, value))

            # Limit history size
            if len(self.history) > self.MAX_HISTORY:
                self.history.pop(0)

            self.move_count += 1
            self.hint_cell = None  # Clear hint when user makes a move
            return True

        return False

    def undo(self) -> bool:
        """
        Undo the last move.
        Returns True if successful, False if no moves to undo.
        """
        if not self.history:
            return False

        move = self.history.pop()
        self.board.grid[move.row][move.col] = move.old_value
        self.move_count = max(0, self.move_count - 1)
        self.hint_cell = None

        return True

    def get_elapsed_time(self) -> float:
        """Get the total elapsed time in seconds."""
        if self.is_paused:
            return self.elapsed_time

        return self.elapsed_time + (time.time() - self.start_time)

    def get_time_string(self) -> str:
        """Get formatted time string (MM:SS)."""
        total_seconds = int(self.get_elapsed_time())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def pause(self):
        """Pause the timer."""
        if not self.is_paused:
            self.elapsed_time += time.time() - self.start_time
            self.is_paused = True

    def resume(self):
        """Resume the timer."""
        if self.is_paused:
            self.start_time = time.time()
            self.is_paused = False

    def get_conflicts(self) -> set:
        """Get all cells that have conflicts with the current cursor position."""
        row, col = self.cursor
        return self.board.get_conflicts(row, col)

    def is_complete(self) -> bool:
        """Check if the puzzle is solved correctly."""
        return self.board.is_complete()

    def to_dict(self) -> dict:
        """Serialize game state to dictionary."""
        return {
            'board': self.board.to_dict(),
            'difficulty': self.difficulty,
            'cursor': self.cursor,
            'elapsed_time': self.get_elapsed_time(),
            'move_count': self.move_count,
            'history': [
                {
                    'row': m.row,
                    'col': m.col,
                    'old_value': m.old_value,
                    'new_value': m.new_value
                }
                for m in self.history
            ]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GameState':
        """Deserialize game state from dictionary."""
        board = Board.from_dict(data['board'])
        game_state = cls(board, data['difficulty'])
        game_state.cursor = tuple(data['cursor'])
        game_state.elapsed_time = data['elapsed_time']
        game_state.move_count = data['move_count']
        game_state.start_time = time.time()

        # Restore history
        game_state.history = [
            Move(m['row'], m['col'], m['old_value'], m['new_value'])
            for m in data['history']
        ]

        return game_state

    def save_to_file(self, filepath: str = None):
        """Save game state to a file."""
        if filepath is None:
            filepath = os.path.expanduser("~/.sudoku-save.json")

        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str = None) -> Optional['GameState']:
        """Load game state from a file. Returns None if file doesn't exist."""
        if filepath is None:
            filepath = os.path.expanduser("~/.sudoku-save.json")

        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except (json.JSONDecodeError, KeyError, IOError):
            return None

    @staticmethod
    def delete_save_file(filepath: str = None):
        """Delete the save file."""
        if filepath is None:
            filepath = os.path.expanduser("~/.sudoku-save.json")

        if os.path.exists(filepath):
            os.remove(filepath)
