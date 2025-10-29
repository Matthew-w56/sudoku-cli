# Sudoku CLI

A terminal-based Sudoku game built with Python and the `blessed` library.

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
./venv/bin/python -m src.game
```

## Features

- Four difficulty levels (Easy, Medium, Hard, Expert)
- Real-time conflict highlighting
- Auto-save/resume functionality
- Hint system and undo support
- Rich terminal UI with box-drawing characters

## Architecture

```
src/
├── board.py       # Board state, validation, and conflict detection
├── solver.py      # Backtracking solver and hint generator
├── generator.py   # Puzzle generation with unique solution verification
├── game_state.py  # Game state management, save/load, undo history
├── game.py        # Main game loop and input handling
└── renderer.py    # Terminal UI rendering with blessed
```

### Key Implementation Details

- **Puzzle Generation**: Fills diagonal 3x3 boxes independently, then solves with randomized backtracking. Removes cells while maintaining unique solutions using constraint counting.
- **Rendering**: Uses Unicode box-drawing characters and ANSI colors via `blessed`. Highlights conflicts, cursor position, and same numbers automatically.
- **State Management**: Maintains undo stack, tracks timer state (pause/resume), and serializes to JSON for auto-save.

## Controls

| Key | Action |
|-----|--------|
| Arrow keys | Navigate |
| 1-9 | Fill cell |
| 0/Backspace | Clear cell |
| h | Hint |
| u | Undo |
| n | New game |
| ? | Help |
| q | Quit |

## Technical Notes

- Minimum terminal size: 50x30
- Auto-saves on exit (if incomplete)
- Given cells are immutable and displayed in cyan
- Conflicts shown in real-time (red highlighting)
