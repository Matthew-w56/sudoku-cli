# Sudoku CLI - Development Steps

## Phase 1: Design & Planning

### 1.1 Technology Stack Decision
- [ ] Choose language: Python (with curses) for rapid development and cross-platform support
- [ ] Choose terminal library: `curses` for Unix/Mac, `windows-curses` for Windows
- [ ] Alternative: Consider `blessed` library for better cross-platform support
- [ ] **Risk**: curses can be finicky on Windows - may need fallback plan

### 1.2 Data Structure Design
- [ ] Board representation: 9x9 2D array/list
- [ ] Cell states: empty (0), filled (1-9), given (immutable initial numbers)
- [ ] Cursor position: (row, col) tuple
- [ ] Game state: board, cursor, timer, move_count, difficulty
- [ ] **Risk**: Need to track which cells are "given" vs user-filled for validation

### 1.3 UI/UX Design
- [ ] Board display: ASCII art with box-drawing characters
- [ ] Cell highlighting: Different color/style for selected cell
- [ ] Visual feedback: Show conflicts (same number in row/col/box)
- [ ] Status bar: Timer, difficulty, controls reminder
- [ ] Color scheme: Define colors for given numbers, user input, errors, selection
- [ ] **Risk**: Color support varies by terminal - need graceful degradation

### 1.4 Control Scheme Design
- [ ] Arrow keys: Navigate grid
- [ ] Numbers 1-9: Fill selected cell
- [ ] 0/Backspace/Delete: Clear cell
- [ ] 'h': Show hints
- [ ] 's': Solve puzzle
- [ ] 'n': New game
- [ ] 'q': Quit
- [ ] 'u': Undo last move
- [ ] **Risk**: Need to handle key conflicts and provide discoverable controls

### 1.5 Algorithm Planning
- [ ] Puzzle generation: Backtracking algorithm to create valid complete board
- [ ] Cell removal: Remove cells while maintaining unique solution
- [ ] Difficulty levels: Easy (40-45 removed), Medium (46-49), Hard (50-53), Expert (54+)
- [ ] Validation: Check row, column, and 3x3 box constraints
- [ ] Solver: Backtracking algorithm for auto-solve and hint generation
- [ ] **Risk**: Puzzle generation can be slow - may need optimization or pre-generated puzzles

---

## Phase 2: Core Implementation

### 2.1 Project Setup
- [ ] Create directory structure: `src/`, `tests/`, `puzzles/`
- [ ] Initialize git repository
- [ ] Create `requirements.txt` or `pyproject.toml`
- [ ] Set up virtual environment
- [ ] Create main entry point: `sudoku.py`
- [ ] **Risk**: Package management might be overkill for simple tool

### 2.2 Basic Board Display
- [ ] Implement `Board` class with 9x9 grid
- [ ] Create `render()` method to display board with box-drawing characters
- [ ] Add row/column numbers for reference
- [ ] Test rendering in terminal
- [ ] **Risk**: Box-drawing characters may not display correctly in all terminals

### 2.3 Terminal Setup & Input Handling
- [ ] Initialize curses/blessed screen
- [ ] Enable color support
- [ ] Set up key input handling (non-blocking)
- [ ] Create game loop: render → get input → update → repeat
- [ ] Handle terminal resize gracefully
- [ ] Clean exit on errors (restore terminal state)
- [ ] **Risk**: Terminal state corruption if program crashes - need proper cleanup

### 2.4 Cursor Navigation
- [ ] Implement cursor position tracking
- [ ] Handle arrow key input (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT)
- [ ] Wrap cursor at edges or stop at boundaries (decide which)
- [ ] Highlight selected cell with different background color
- [ ] **Risk**: Arrow key codes differ across terminals - test thoroughly

### 2.5 Number Input
- [ ] Detect number keys 1-9
- [ ] Update board at cursor position
- [ ] Prevent overwriting "given" cells (initial puzzle numbers)
- [ ] Provide visual/audio feedback for invalid actions
- [ ] Implement clear cell (0, backspace, delete)
- [ ] **Risk**: Need to clearly distinguish given vs user-entered numbers

### 2.6 Puzzle Generation
- [ ] Implement solver using backtracking (will be used for generation too)
- [ ] Create complete valid 9x9 Sudoku board
- [ ] Randomly remove cells while checking for unique solution
- [ ] Implement difficulty levels (remove different amounts of cells)
- [ ] Cache/save generated puzzles for faster startup
- [ ] **Risk**: Generation can take 1-10 seconds - need loading indicator or pre-generation

### 2.7 Validation Logic
- [ ] Check if number exists in same row
- [ ] Check if number exists in same column
- [ ] Check if number exists in same 3x3 box
- [ ] Implement real-time validation (highlight conflicts)
- [ ] Implement completion check (puzzle solved correctly)
- [ ] **Risk**: 3x3 box calculation is tricky - test edge cases

### 2.8 Win Condition
- [ ] Detect when board is completely filled
- [ ] Validate all constraints are satisfied
- [ ] Display victory message
- [ ] Show completion time and move count
- [ ] Offer new game option
- [ ] **Risk**: False positives if validation logic has bugs

---

## Phase 3: Polish & Enhancement

### 3.1 Visual Polish
- [ ] Add color coding: given numbers (cyan), user numbers (white), errors (red), selection (yellow bg)
- [ ] Add thick borders between 3x3 boxes
- [ ] Add title screen with ASCII art logo
- [ ] Add status bar with timer and controls
- [ ] Improve spacing and alignment
- [ ] **Risk**: Over-complicated UI might be harder to read than simple version

### 3.2 Timer & Stats
- [ ] Track elapsed time from game start
- [ ] Display timer in status bar (MM:SS format)
- [ ] Track number of moves
- [ ] Display stats on win screen
- [ ] **Risk**: Timer needs to pause when showing help/menus

### 3.3 Undo System
- [ ] Implement move history stack
- [ ] Store (row, col, old_value, new_value) for each move
- [ ] Implement undo command ('u' key)
- [ ] Limit history size (last 50 moves?)
- [ ] **Risk**: Memory usage could grow with unlimited history

### 3.4 Hint System
- [ ] Use solver to find next correct move
- [ ] Show hint without revealing full solution
- [ ] Limit hints? Or penalize them?
- [ ] Visual indicator for hinted cell
- [ ] **Risk**: Solver might be slow on hard puzzles

### 3.5 Auto-Solver
- [ ] Implement 's' key to reveal solution
- [ ] Animate solution being filled in (optional)
- [ ] Confirm before solving (user might press accidentally)
- [ ] **Risk**: Solver must work correctly or app looks broken

### 3.6 Difficulty Selection
- [ ] Main menu to choose difficulty before game starts
- [ ] Easy / Medium / Hard / Expert options
- [ ] Show difficulty on status bar during game
- [ ] **Risk**: Difficulty balancing - my "easy" might be too hard

### 3.7 Save/Load Game
- [ ] Save current game state to file (`~/.sudoku-save.json`)
- [ ] Auto-save periodically or on exit
- [ ] Load saved game on startup (if exists)
- [ ] Option to abandon saved game and start new
- [ ] **Risk**: File I/O errors, corrupted save files

### 3.8 Help Screen
- [ ] Create help overlay showing all controls
- [ ] Toggle with 'h' or '?' key
- [ ] Pause timer when help is shown
- [ ] Clear explanation of game rules
- [ ] **Risk**: Help screen might obscure game board - need proper overlay/modal

### 3.9 Error Handling
- [ ] Handle terminal too small (minimum 40x20?)
- [ ] Handle terminal resize during game
- [ ] Catch and display keyboard interrupts gracefully
- [ ] Handle file I/O errors (save/load)
- [ ] Provide useful error messages
- [ ] **Risk**: Edge cases will definitely crash the app

### 3.10 Cross-Platform Testing
- [ ] Test on Linux terminal
- [ ] Test on macOS Terminal.app
- [ ] Test on Windows (PowerShell, CMD, Windows Terminal)
- [ ] Test with different color schemes
- [ ] Test with screen readers (basic accessibility)
- [ ] **Risk**: Will definitely have platform-specific bugs

### 3.11 Configuration File
- [ ] Create `~/.sudoku-config.json` for preferences
- [ ] Configurable color scheme
- [ ] Default difficulty level
- [ ] Key bindings customization (stretch goal)
- [ ] **Risk**: Config parsing errors could break app

### 3.12 Performance Optimization
- [ ] Profile puzzle generation time
- [ ] Consider pre-generating puzzles
- [ ] Optimize rendering (only redraw changed cells?)
- [ ] Test with slow terminals
- [ ] **Risk**: Premature optimization might complicate code

---

## Phase 4: Testing & Documentation

### 4.1 Unit Tests
- [ ] Test board validation logic
- [ ] Test solver algorithm
- [ ] Test puzzle generation (uniqueness)
- [ ] Test undo system
- [ ] **Risk**: UI code is hard to unit test

### 4.2 Integration Testing
- [ ] Simulate full game playthrough
- [ ] Test edge cases (all cells same number, empty board, etc)
- [ ] Test error conditions
- [ ] **Risk**: Terminal UI is difficult to automate

### 4.3 Documentation
- [ ] Write README.md with installation instructions
- [ ] Document controls clearly
- [ ] Add screenshots (terminal recordings with asciinema?)
- [ ] Document known issues/limitations
- [ ] **Risk**: Documentation will become outdated

### 4.4 Code Cleanup
- [ ] Remove debug print statements
- [ ] Add docstrings to all functions
- [ ] Consistent code style (run formatter)
- [ ] Remove dead code
- [ ] Add type hints (if using Python 3.7+)
- [ ] **Risk**: Cleanup might introduce bugs

---

## Known Limitations & Risks

### High Risk Items
1. **Puzzle generation speed**: May take 5-10 seconds for hard puzzles
2. **Cross-platform compatibility**: curses behavior varies significantly
3. **Terminal size**: Small terminals will break layout
4. **Color support**: Not all terminals support 256 colors

### Medium Risk Items
1. **Difficulty calibration**: My "easy" might not feel easy to users
2. **Solver performance**: Backtracking can be slow on hardest puzzles
3. **Undo system**: Complex interactions with validation
4. **Save file corruption**: JSON parsing might fail

### Low Risk Items
1. **ASCII art rendering**: Straightforward but may need tweaking
2. **Timer display**: Simple time tracking
3. **Win detection**: Straightforward validation check

---

## Estimated Timeline (Optimistic)

- **Phase 1 (Design)**: Already complete
- **Phase 2 (Core)**: 4-6 hours of focused work
- **Phase 3 (Polish)**: 3-5 hours
- **Phase 4 (Testing)**: 2-3 hours

**Total**: 9-14 hours of actual development time

**Reality check**: With bugs, testing, and revisions, expect 15-20 hours total.

---

## Success Criteria

- [ ] Can start game and see board
- [ ] Can navigate with arrow keys
- [ ] Can enter numbers 1-9
- [ ] Puzzles are generated at multiple difficulties
- [ ] Can detect and show puzzle completion
- [ ] Doesn't crash on basic inputs
- [ ] Works on at least Linux and macOS

## Stretch Goals (If Time Permits)

- [ ] Multiple puzzle themes/variants
- [ ] Daily challenge mode
- [ ] Leaderboard (local high scores)
- [ ] Pencil marks (small candidate numbers in cells)
- [ ] Color themes
- [ ] Sound effects (terminal beep on errors)
