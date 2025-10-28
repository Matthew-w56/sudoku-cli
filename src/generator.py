"""
Sudoku puzzle generator with configurable difficulty levels.
"""
import random
from typing import List, Tuple
from src.board import Board
from src.solver import Solver


class Difficulty:
    """Difficulty levels based on number of cells to remove."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

    # Number of cells to remove for each difficulty
    REMOVE_COUNT = {
        EASY: (40, 45),      # Remove 40-45 cells
        MEDIUM: (46, 49),    # Remove 46-49 cells
        HARD: (50, 53),      # Remove 50-53 cells
        EXPERT: (54, 58),    # Remove 54-58 cells
    }


class Generator:
    """Generates valid Sudoku puzzles with configurable difficulty."""

    @staticmethod
    def generate(difficulty: str = Difficulty.EASY) -> Board:
        """
        Generate a new Sudoku puzzle.

        Args:
            difficulty: One of Difficulty.EASY, MEDIUM, HARD, or EXPERT

        Returns:
            A Board object with a valid puzzle
        """
        # Generate a complete valid board
        board = Generator._generate_complete_board()

        # Remove cells according to difficulty
        min_remove, max_remove = Difficulty.REMOVE_COUNT.get(
            difficulty, Difficulty.REMOVE_COUNT[Difficulty.EASY]
        )
        num_to_remove = random.randint(min_remove, max_remove)

        Generator._remove_cells(board, num_to_remove)

        # Mark all non-zero cells as given
        for row in range(board.SIZE):
            for col in range(board.SIZE):
                if board.grid[row][col] != 0:
                    board.mark_given(row, col)

        return board

    @staticmethod
    def _generate_complete_board() -> Board:
        """Generate a complete valid Sudoku board."""
        board = Board()

        # Fill diagonal 3x3 boxes first (they don't affect each other)
        Generator._fill_diagonal_boxes(board)

        # Solve the rest using backtracking with randomness
        Solver.solve_with_randomness(board)

        return board

    @staticmethod
    def _fill_diagonal_boxes(board: Board):
        """Fill the three diagonal 3x3 boxes with random valid numbers."""
        for box in range(3):
            start = box * board.BOX_SIZE
            Generator._fill_box(board, start, start)

    @staticmethod
    def _fill_box(board: Board, row: int, col: int):
        """Fill a 3x3 box starting at (row, col) with random numbers 1-9."""
        numbers = list(range(1, 10))
        random.shuffle(numbers)

        idx = 0
        for r in range(row, row + board.BOX_SIZE):
            for c in range(col, col + board.BOX_SIZE):
                board.grid[r][c] = numbers[idx]
                idx += 1

    @staticmethod
    def _remove_cells(board: Board, count: int):
        """
        Remove cells from the board while maintaining a unique solution.

        Args:
            board: The complete board to remove cells from
            count: Number of cells to attempt to remove
        """
        # Get all cell positions
        positions = [(r, c) for r in range(board.SIZE) for c in range(board.SIZE)]
        random.shuffle(positions)

        removed = 0
        attempts = 0
        max_attempts = count * 3  # Limit attempts to avoid infinite loops

        while removed < count and attempts < max_attempts:
            if not positions:
                break

            row, col = positions.pop()
            attempts += 1

            # Save the current value
            backup = board.grid[row][col]

            # Try removing the cell
            board.grid[row][col] = 0

            # Check if the puzzle still has a unique solution
            # For performance, we only check if there are <= 2 solutions
            board_copy = board.copy()
            solution_count = Solver.count_solutions(board_copy, limit=2)

            if solution_count == 1:
                # Successfully removed, keep it empty
                removed += 1
            else:
                # Multiple solutions or no solution, restore the value
                board.grid[row][col] = backup

    @staticmethod
    def generate_simple(difficulty: str = Difficulty.EASY) -> Board:
        """
        Generate a puzzle with a simpler algorithm (faster but may not guarantee uniqueness).
        This is a fallback if the main generator is too slow.
        """
        board = Generator._generate_complete_board()

        min_remove, max_remove = Difficulty.REMOVE_COUNT.get(
            difficulty, Difficulty.REMOVE_COUNT[Difficulty.EASY]
        )
        num_to_remove = random.randint(min_remove, max_remove)

        # Randomly remove cells without checking uniqueness
        positions = [(r, c) for r in range(board.SIZE) for c in range(board.SIZE)]
        random.shuffle(positions)

        for i in range(num_to_remove):
            row, col = positions[i]
            board.grid[row][col] = 0

        # Mark remaining cells as given
        for row in range(board.SIZE):
            for col in range(board.SIZE):
                if board.grid[row][col] != 0:
                    board.mark_given(row, col)

        return board
