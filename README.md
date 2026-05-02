# TextGames

This repository now treats `dev/games.py` as the active game source.

## What is kept
- `dev/games.py` — current game implementation
- `dev/text.txt` and related `dev/` assets if needed by the current game

## What is ignored
- old root version files like `main_*.py`, `text_game_*.py`, and `text_games_*.py`
- old experiment folders: `new/`, `busted/`, `oo/`, `split/`
- generated artifacts like `*.exe`

## Git workflow recommendations
1. Make small, focused commits.
2. Use branches for new experiments and features.
3. Keep the repo history clean; do not store multiple versioned copies of the same file.
4. Use `.gitignore` for temporary files, editor state, and build outputs.
