# Snake CLI

A Nokia-style Snake game for the terminal, built with Python and curses.

```
┌──────────────────────────────────────────┐
│  SNAKE           Score: 30               │
├──────────────────────────────────────────┤
│ ########################################│
│ #                                      # │
│ #     ooooo@                           # │
│ #                     *                # │
│ #                                      # │
│ ########################################│
├──────────────────────────────────────────┤
│  ← → ↑ ↓ to move   Q to quit           │
└──────────────────────────────────────────┘
```

## Installation

No dependencies required - just Python 3 with the standard library.

```bash
git clone https://github.com/Dlgvn/snake-cli.git
cd snake-cli
python3 main.py
```

## Controls

| Key | Action |
|-----|--------|
| ↑ ↓ ← → | Move snake |
| Q | Quit game |
| Enter | Confirm selection |

## Options

```bash
python3 main.py --width 60 --height 30 --speed 80
```

| Option | Default | Description |
|--------|---------|-------------|
| `--width`, `-w` | 40 | Board width |
| `--height`, `-H` | 20 | Board height |
| `--speed`, `-s` | 100 | Initial speed (ms per frame) |

## Features

- Classic snake gameplay
- Nokia-style bordered UI with colors
- Speed increases as you score
- Leaderboard with top 10 scores
- Configurable board size and speed

## Project Structure

```
├── main.py           # Entry point and CLI args
├── game.py           # Game loop and state
├── snake.py          # Snake movement and collision
├── food.py           # Food spawning
├── leaderboard.py    # Score persistence
├── ui.py             # Terminal rendering
├── config.py         # Game settings
└── scores.json       # Saved scores (generated)
```
