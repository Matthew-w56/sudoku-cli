#!/usr/bin/env python3
"""
Sudoku CLI - A terminal-based Sudoku game

Usage:
    python sudoku.py
    or
    ./sudoku.py (if executable)
"""
import sys
from src.game import Game


def main():
    """Main entry point for the Sudoku CLI game."""
    game = Game()

    # Check terminal size before starting
    if not game.check_terminal_size():
        print("\nPlease resize your terminal and try again.")
        sys.exit(1)

    # Run the game
    game.run()


if __name__ == "__main__":
    main()
