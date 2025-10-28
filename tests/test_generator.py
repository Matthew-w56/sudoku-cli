"""
Unit tests for the Generator class.
"""
import unittest
from src.generator import Generator, Difficulty
from src.solver import Solver


class TestGenerator(unittest.TestCase):
    """Test cases for Generator class."""

    def test_generate_easy_puzzle(self):
        """Test generating an easy puzzle."""
        board = Generator.generate(Difficulty.EASY)

        # Count given cells (non-zero)
        given_count = sum(
            1 for row in range(9) for col in range(9)
            if board.grid[row][col] != 0
        )

        # Easy should have 36-41 given cells (81 - 40 to 81 - 45)
        self.assertGreaterEqual(given_count, 36)
        self.assertLessEqual(given_count, 41)

        # Verify all non-zero cells are marked as given
        for row in range(9):
            for col in range(9):
                if board.grid[row][col] != 0:
                    self.assertTrue(board.is_given(row, col))

    def test_generate_medium_puzzle(self):
        """Test generating a medium puzzle."""
        board = Generator.generate(Difficulty.MEDIUM)

        given_count = sum(
            1 for row in range(9) for col in range(9)
            if board.grid[row][col] != 0
        )

        # Medium should have 32-35 given cells
        self.assertGreaterEqual(given_count, 32)
        self.assertLessEqual(given_count, 35)

    def test_generate_hard_puzzle(self):
        """Test generating a hard puzzle."""
        board = Generator.generate(Difficulty.HARD)

        given_count = sum(
            1 for row in range(9) for col in range(9)
            if board.grid[row][col] != 0
        )

        # Hard should have 28-31 given cells
        self.assertGreaterEqual(given_count, 28)
        self.assertLessEqual(given_count, 31)

    def test_generate_expert_puzzle(self):
        """Test generating an expert puzzle."""
        board = Generator.generate(Difficulty.EXPERT)

        given_count = sum(
            1 for row in range(9) for col in range(9)
            if board.grid[row][col] != 0
        )

        # Expert should have 23-27 given cells
        self.assertGreaterEqual(given_count, 23)
        self.assertLessEqual(given_count, 27)

    def test_generated_puzzle_is_solvable(self):
        """Test that generated puzzles are solvable."""
        for difficulty in [Difficulty.EASY, Difficulty.MEDIUM]:
            board = Generator.generate(difficulty)
            board_copy = board.copy()

            result = Solver.solve(board_copy)
            self.assertTrue(result, f"Generated {difficulty} puzzle is not solvable")

    def test_generate_simple(self):
        """Test the simple generation method."""
        board = Generator.generate_simple(Difficulty.EASY)

        # Should have cells removed
        empty_count = sum(
            1 for row in range(9) for col in range(9)
            if board.grid[row][col] == 0
        )

        self.assertGreater(empty_count, 0)

        # Should be solvable
        board_copy = board.copy()
        result = Solver.solve(board_copy)
        self.assertTrue(result)

    def test_generated_puzzles_are_different(self):
        """Test that generated puzzles are different from each other."""
        board1 = Generator.generate_simple(Difficulty.EASY)
        board2 = Generator.generate_simple(Difficulty.EASY)

        # Boards should be different
        same = True
        for row in range(9):
            for col in range(9):
                if board1.grid[row][col] != board2.grid[row][col]:
                    same = False
                    break
            if not same:
                break

        self.assertFalse(same, "Generated puzzles are identical")


if __name__ == '__main__':
    unittest.main()
