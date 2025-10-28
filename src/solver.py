"""
Sudoku solver using backtracking algorithm.
"""
from typing import Optional, Tuple, List
import random
from src.board import Board


class Solver:
    """Sudoku solver and puzzle generator using backtracking."""

    @staticmethod
    def solve(board: Board) -> bool:
        """
        Solve the Sudoku puzzle using backtracking.
        Modifies the board in place.
        Returns True if solved, False if no solution exists.
        """
        empty = Solver._find_empty_cell(board)
        if not empty:
            return True  # Board is complete

        row, col = empty

        # Try numbers 1-9 in random order for variety
        numbers = list(range(1, 10))
        for num in numbers:
            if board.is_valid_move(row, col, num):
                board.grid[row][col] = num

                if Solver.solve(board):
                    return True

                # Backtrack
                board.grid[row][col] = 0

        return False

    @staticmethod
    def solve_with_randomness(board: Board) -> bool:
        """
        Solve the Sudoku puzzle with randomized number ordering.
        This creates variety in generated puzzles.
        """
        empty = Solver._find_empty_cell(board)
        if not empty:
            return True

        row, col = empty

        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for num in numbers:
            if board.is_valid_move(row, col, num):
                board.grid[row][col] = num

                if Solver.solve_with_randomness(board):
                    return True

                board.grid[row][col] = 0

        return False

    @staticmethod
    def _find_empty_cell(board: Board) -> Optional[Tuple[int, int]]:
        """Find the next empty cell (value = 0). Returns None if board is full."""
        for row in range(board.SIZE):
            for col in range(board.SIZE):
                if board.grid[row][col] == 0:
                    return (row, col)
        return None

    @staticmethod
    def count_solutions(board: Board, limit: int = 2) -> int:
        """
        Count the number of solutions for a puzzle.
        Stops counting after reaching limit (for efficiency).
        Used to ensure puzzles have unique solutions.
        """
        count = [0]  # Use list to allow modification in nested function

        def backtrack():
            if count[0] >= limit:
                return

            empty = Solver._find_empty_cell(board)
            if not empty:
                count[0] += 1
                return

            row, col = empty

            for num in range(1, 10):
                if board.is_valid_move(row, col, num):
                    board.grid[row][col] = num
                    backtrack()
                    board.grid[row][col] = 0

        backtrack()
        return count[0]

    @staticmethod
    def get_hint(board: Board) -> Optional[Tuple[int, int, int]]:
        """
        Find one valid move for the current board.
        Returns (row, col, value) or None if no solution exists.
        """
        # Create a copy to avoid modifying the original
        temp_board = board.copy()

        # Try to solve
        if Solver.solve(temp_board):
            # Find the first cell that differs
            for row in range(board.SIZE):
                for col in range(board.SIZE):
                    if board.grid[row][col] == 0 and temp_board.grid[row][col] != 0:
                        return (row, col, temp_board.grid[row][col])

        return None

    @staticmethod
    def get_solution(board: Board) -> Optional[Board]:
        """
        Get the complete solution for the board.
        Returns a new Board object with the solution, or None if unsolvable.
        """
        solution = board.copy()
        if Solver.solve(solution):
            return solution
        return None
