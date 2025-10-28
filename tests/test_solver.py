"""
Unit tests for the Solver class.
"""
import unittest
from src.board import Board
from src.solver import Solver


class TestSolver(unittest.TestCase):
    """Test cases for Solver class."""

    def test_solve_empty_board(self):
        """Test solving an empty board."""
        board = Board()
        result = Solver.solve(board)

        self.assertTrue(result)
        self.assertTrue(board.is_complete())

    def test_solve_partial_board(self):
        """Test solving a partially filled board."""
        board = Board()

        # Set up a simple puzzle
        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        for row in range(9):
            for col in range(9):
                board.grid[row][col] = puzzle[row][col]

        result = Solver.solve(board)

        self.assertTrue(result)
        self.assertTrue(board.is_complete())

    def test_solve_unsolvable_board(self):
        """Test that an unsolvable board returns False."""
        board = Board()

        # Create an invalid board with impossible configuration
        # Fill first row with all 1s (impossible sudoku)
        for col in range(9):
            board.grid[0][col] = 1

        result = Solver.solve(board)
        self.assertFalse(result)

    def test_count_solutions_unique(self):
        """Test counting solutions for a puzzle with unique solution."""
        board = Board()

        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        for row in range(9):
            for col in range(9):
                board.grid[row][col] = puzzle[row][col]

        count = Solver.count_solutions(board, limit=2)
        self.assertEqual(count, 1)

    def test_get_hint(self):
        """Test getting a hint for a puzzle."""
        board = Board()

        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        for row in range(9):
            for col in range(9):
                board.grid[row][col] = puzzle[row][col]

        hint = Solver.get_hint(board)

        self.assertIsNotNone(hint)
        self.assertEqual(len(hint), 3)

        row, col, value = hint
        self.assertTrue(0 <= row < 9)
        self.assertTrue(0 <= col < 9)
        self.assertTrue(1 <= value <= 9)
        self.assertEqual(board.grid[row][col], 0)  # Should be an empty cell

    def test_get_solution(self):
        """Test getting complete solution."""
        board = Board()

        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        for row in range(9):
            for col in range(9):
                board.grid[row][col] = puzzle[row][col]

        solution = Solver.get_solution(board)

        self.assertIsNotNone(solution)
        self.assertTrue(solution.is_complete())

        # Original board should be unchanged
        self.assertEqual(board.grid[0][2], 0)


if __name__ == '__main__':
    unittest.main()
