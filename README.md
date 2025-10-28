# Sudoku CLI

A feature-rich, terminal-based Sudoku game built with Python and the blessed library.

## Features

- **Multiple Difficulty Levels**: Easy, Medium, Hard, and Expert
- **Dynamic Puzzle Generation**: Unlimited unique puzzles generated on-the-fly
- **Beautiful TUI**: Colorful interface with box-drawing characters
- **Real-time Validation**: Instant visual feedback for conflicts
- **Smart Features**:
  - Hints system to help when stuck
  - Undo/redo functionality
  - Auto-solver
  - Timer and move counter
  - Auto-save/load game state
- **Comprehensive Help**: Built-in help screen with all controls
- **Cross-platform**: Works on Linux, macOS, and Windows

## Screenshots

```
                           SUDOKU
                          CLI Edition

     ┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓
     ┃ 5 │ 3 │ . ┃ . │ 7 │ . ┃ . │ . │ . ┃
     ┠───┼───┼───╂───┼───┼───╂───┼───┼───┨
     ┃ 6 │ . │ . ┃ 1 │ 9 │ 5 ┃ . │ . │ . ┃
     ┠───┼───┼───╂───┼───┼───╂───┼───┼───┨
     ┃ . │ 9 │ 8 ┃ . │ . │ . ┃ . │ 6 │ . ┃
     ┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫
     ┃ 8 │ . │ . ┃ . │ 6 │ . ┃ . │ . │ 3 ┃
     ┠───┼───┼───╂───┼───┼───╂───┼───┼───┨
     ┃ 4 │ . │ . ┃ 8 │ . │ 3 ┃ . │ . │ 1 ┃
     ┠───┼───┼───╂───┼───┼───╂───┼───┼───┨
     ┃ 7 │ . │ . ┃ . │ 2 │ . ┃ . │ . │ 6 ┃
     ┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫
     ┃ . │ 6 │ . ┃ . │ . │ . ┃ 2 │ 8 │ . ┃
     ┠───┼───┼───╂───┼───┼───╂───┼───┼───┨
     ┃ . │ . │ . ┃ 4 │ 1 │ 9 ┃ . │ . │ 5 ┃
     ┠───┼───┼───╂───┼───┼───╂───┼───┼───┨
     ┃ . │ . │ . ┃ . │ 8 │ . ┃ . │ 7 │ 9 ┃
     ┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛

     Difficulty: MEDIUM  |  Time: 05:23  |  Moves: 42
```

## How to Play

### Objective

Fill the 9x9 grid with digits 1-9 such that:
- Each row contains all digits from 1 to 9
- Each column contains all digits from 1 to 9
- Each 3x3 box contains all digits from 1 to 9

### Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** | Navigate the grid |
| **1-9** | Fill the selected cell |
| **0, Backspace, Delete** | Clear the selected cell |
| **h** | Get a hint for the current puzzle |
| **s** | Auto-solve the puzzle |
| **u** | Undo the last move |
| **n** | Start a new game |
| **?** | Show/hide help screen |
| **q** | Quit the game |

### Color Coding

- **Cyan**: Given numbers (part of the initial puzzle, cannot be modified)
- **White**: Your numbers (user-entered)
- **Red**: Conflicting numbers (violate Sudoku rules)
- **Yellow**: Hint cells
- **Yellow Background**: Current cursor position

## Features in Detail

### Difficulty Levels

- **Easy**: 40-45 cells removed (36-41 given)
- **Medium**: 46-49 cells removed (32-35 given)
- **Hard**: 50-53 cells removed (28-31 given)
- **Expert**: 54-58 cells removed (23-27 given)

### Puzzle Generation

Puzzles are generated dynamically using a backtracking algorithm:
1. Creates a complete valid Sudoku board
2. Removes cells while ensuring a unique solution
3. Generation typically takes 1-5 seconds depending on difficulty

### Auto-save

The game automatically saves your progress when you exit. When you restart, you'll be prompted to continue your saved game.

Save files are stored at:
- Linux/macOS: `~/.sudoku-save.json`
- Windows: `%USERPROFILE%\.sudoku-save.json`

### Hints and Solver

- **Hints**: Suggests one valid move at a time
- **Solver**: Automatically fills in the entire solution
- Both use the same backtracking algorithm that generates puzzles

## Architecture

### Project Structure

```
sudoku-cli/
├── src/
│   ├── __init__.py
│   ├── board.py         # Board data structure and validation
│   ├── solver.py        # Backtracking solver algorithm
│   ├── generator.py     # Puzzle generation with difficulty levels
│   ├── renderer.py      # Terminal UI rendering (blessed)
│   ├── game_state.py    # Game state management, save/load
│   └── game.py          # Main game loop and controller
├── tests/
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_solver.py
│   └── test_generator.py
├── sudoku.py            # Entry point
├── requirements.txt
├── STEPS.md            # Development roadmap
└── README.md
```

### Key Components

- **Board**: 9x9 grid representation with validation logic
- **Solver**: Backtracking algorithm for solving and generating puzzles
- **Generator**: Creates valid puzzles with configurable difficulty
- **Renderer**: Terminal UI using blessed library for cross-platform support
- **GameState**: Manages game state, history, timer, and persistence

## Development

### Running

./venv/bin/python -m unittest discover tests/ -v
./venv/bin/python ./sudoku.py

### Test Coverage

The project includes comprehensive unit tests:
- Board validation and data structures (13 tests)
- Solver algorithm (6 tests)
- Puzzle generation (7 tests)

All 26 tests pass successfully.

## Known Limitations

1. **Terminal Size**: Requires a minimum terminal size of 50x30 characters
2. **Generation Time**: Expert puzzles may take 5-10 seconds to generate
3. **No Pencil Marks**: Currently doesn't support candidate numbers in cells
4. **Single Undo**: Undo history is limited to the last 100 moves

## Future Enhancements

Potential features for future versions:
- Pencil marks (candidate numbers)
- Multiple color themes
- Statistics tracking (best times, completion rates)
- Daily challenge mode
- Puzzle import/export
- Configurable key bindings
- Sound effects (terminal beep)

## Troubleshooting

### Terminal too small error

Resize your terminal to at least 50 columns by 30 rows.

### Colors not displaying

Make sure your terminal supports ANSI colors. Most modern terminals do.

### Puzzle generation is slow

This is normal for harder difficulties. The algorithm ensures unique solutions. You can modify `generator.py` to use `generate_simple()` for faster (but potentially non-unique) puzzles.

## License

This project is open source and available for personal and educational use.

## Acknowledgments

- Built with [blessed](https://github.com/jquast/blessed) for cross-platform terminal handling
- Inspired by classic Sudoku puzzles
- Developed following the comprehensive plan in STEPS.md

---

Enjoy playing Sudoku in your terminal!
