"""
Sudoku board representation and validation logic.
"""
from typing import List, Tuple, Optional, Set
import copy


class Board:
    """Represents a 9x9 Sudoku board with validation and rendering capabilities."""

    SIZE = 9
    BOX_SIZE = 3

    def __init__(self):
        """Initialize an empty Sudoku board."""
        # 0 represents empty cells, 1-9 are filled cells
        self.grid: List[List[int]] = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        # Track which cells are part of the initial puzzle (immutable)
        self.given: List[List[bool]] = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def get(self, row: int, col: int) -> int:
        """Get the value at the specified position."""
        return self.grid[row][col]

    def set(self, row: int, col: int, value: int) -> bool:
        """
        Set a value at the specified position.
        Returns True if successful, False if the cell is given/immutable.
        """
        if self.given[row][col]:
            return False
        self.grid[row][col] = value
        return True

    def is_given(self, row: int, col: int) -> bool:
        """Check if a cell is part of the initial puzzle."""
        return self.given[row][col]

    def mark_given(self, row: int, col: int):
        """Mark a cell as part of the initial puzzle (immutable)."""
        self.given[row][col] = True

    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        """
        Check if placing num at (row, col) would be valid.
        Does not check if the cell is given.
        """
        # Check row
        for c in range(self.SIZE):
            if c != col and self.grid[row][c] == num:
                return False

        # Check column
        for r in range(self.SIZE):
            if r != row and self.grid[r][col] == num:
                return False

        # Check 3x3 box
        box_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        box_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(box_row, box_row + self.BOX_SIZE):
            for c in range(box_col, box_col + self.BOX_SIZE):
                if (r, c) != (row, col) and self.grid[r][c] == num:
                    return False

        return True

    def get_conflicts(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """
        Get all cells that conflict with the value at (row, col).
        Returns a set of (row, col) tuples.
        """
        conflicts = set()
        num = self.grid[row][col]

        if num == 0:
            return conflicts

        # Check row
        for c in range(self.SIZE):
            if c != col and self.grid[row][c] == num:
                conflicts.add((row, c))

        # Check column
        for r in range(self.SIZE):
            if r != row and self.grid[r][col] == num:
                conflicts.add((r, col))

        # Check 3x3 box
        box_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        box_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(box_row, box_row + self.BOX_SIZE):
            for c in range(box_col, box_col + self.BOX_SIZE):
                if (r, c) != (row, col) and self.grid[r][c] == num:
                    conflicts.add((r, c))

        return conflicts

    def is_complete(self) -> bool:
        """Check if the board is completely filled with valid numbers."""
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.grid[row][col] == 0:
                    return False
                if not self.is_valid_move(row, col, self.grid[row][col]):
                    return False
        return True

    def is_filled(self) -> bool:
        """Check if all cells are filled (regardless of validity)."""
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.grid[row][col] == 0:
                    return False
        return True

    def copy(self) -> 'Board':
        """Create a deep copy of the board."""
        new_board = Board()
        new_board.grid = copy.deepcopy(self.grid)
        new_board.given = copy.deepcopy(self.given)
        return new_board

    def clear(self):
        """Clear the entire board."""
        self.grid = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.given = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def to_dict(self) -> dict:
        """Serialize board to dictionary for saving."""
        return {
            'grid': self.grid,
            'given': self.given
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Board':
        """Deserialize board from dictionary."""
        board = cls()
        board.grid = data['grid']
        board.given = data['given']
        return board
