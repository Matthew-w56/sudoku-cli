"""
Unit tests for the Board class.
"""
import unittest
from src.board import Board


class TestBoard(unittest.TestCase):
    """Test cases for Board class."""

    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()

    def test_initial_board_is_empty(self):
        """Test that a new board is empty."""
        for row in range(9):
            for col in range(9):
                self.assertEqual(self.board.get(row, col), 0)
                self.assertFalse(self.board.is_given(row, col))

    def test_set_and_get(self):
        """Test setting and getting cell values."""
        self.board.set(0, 0, 5)
        self.assertEqual(self.board.get(0, 0), 5)

        self.board.set(8, 8, 9)
        self.assertEqual(self.board.get(8, 8), 9)

    def test_given_cells_cannot_be_modified(self):
        """Test that cells marked as given cannot be modified."""
        self.board.set(0, 0, 5)
        self.board.mark_given(0, 0)

        # Try to modify
        result = self.board.set(0, 0, 7)
        self.assertFalse(result)
        self.assertEqual(self.board.get(0, 0), 5)

    def test_is_valid_move_row_conflict(self):
        """Test validation for row conflicts."""
        self.board.set(0, 0, 5)
        self.assertFalse(self.board.is_valid_move(0, 5, 5))
        self.assertTrue(self.board.is_valid_move(0, 5, 3))

    def test_is_valid_move_column_conflict(self):
        """Test validation for column conflicts."""
        self.board.set(0, 0, 5)
        self.assertFalse(self.board.is_valid_move(5, 0, 5))
        self.assertTrue(self.board.is_valid_move(5, 0, 3))

    def test_is_valid_move_box_conflict(self):
        """Test validation for 3x3 box conflicts."""
        self.board.set(0, 0, 5)
        self.assertFalse(self.board.is_valid_move(2, 2, 5))
        self.assertTrue(self.board.is_valid_move(2, 2, 3))

    def test_get_conflicts(self):
        """Test conflict detection."""
        # Place same number in row
        self.board.set(0, 0, 5)
        self.board.set(0, 5, 5)

        conflicts = self.board.get_conflicts(0, 0)
        self.assertIn((0, 5), conflicts)

    def test_is_complete_empty_board(self):
        """Test that an empty board is not complete."""
        self.assertFalse(self.board.is_complete())

    def test_is_complete_valid_board(self):
        """Test a valid complete board."""
        # Create a simple valid 9x9 board
        valid_board = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]

        for row in range(9):
            for col in range(9):
                self.board.grid[row][col] = valid_board[row][col]

        self.assertTrue(self.board.is_complete())

    def test_is_filled(self):
        """Test if board is filled."""
        self.assertFalse(self.board.is_filled())

        # Fill board
        for row in range(9):
            for col in range(9):
                self.board.set(row, col, 1)

        self.assertTrue(self.board.is_filled())

    def test_copy(self):
        """Test board copying."""
        self.board.set(0, 0, 5)
        self.board.mark_given(0, 0)

        copy = self.board.copy()
        self.assertEqual(copy.get(0, 0), 5)
        self.assertTrue(copy.is_given(0, 0))

        # Modify copy
        copy.given[0][0] = False
        copy.set(0, 0, 7)

        # Original should be unchanged
        self.assertEqual(self.board.get(0, 0), 5)
        self.assertTrue(self.board.is_given(0, 0))

    def test_clear(self):
        """Test clearing the board."""
        self.board.set(0, 0, 5)
        self.board.mark_given(0, 0)

        self.board.clear()

        self.assertEqual(self.board.get(0, 0), 0)
        self.assertFalse(self.board.is_given(0, 0))

    def test_serialization(self):
        """Test board serialization and deserialization."""
        self.board.set(0, 0, 5)
        self.board.mark_given(0, 0)

        data = self.board.to_dict()
        restored = Board.from_dict(data)

        self.assertEqual(restored.get(0, 0), 5)
        self.assertTrue(restored.is_given(0, 0))


if __name__ == '__main__':
    unittest.main()
