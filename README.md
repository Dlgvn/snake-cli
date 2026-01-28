# Snake CLI

A Nokia-style Snake game for the terminal, built with Python and curses.

```
┌──────────────────────────────────────────┐
│  SNAKE           Score: 50   BONUS: 8.5s │
├──────────────────────────────────────────┤
│ ########################################│
│ #                                      # │
│ #     ooooo@              $$           # │
│ #                  *      $$           # │
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
- **Wall wrapping** - pass through walls and appear on the opposite side
- **Bonus food** - 2x2 bonus spawns every 4 foods with timed scoring (10-100 points)
- Nokia-style bordered UI with colors
- Speed increases as you score
- Leaderboard with top 10 scores
- Configurable board size and speed

## Gameplay

### Regular Food (`*`)
- Eat to grow and score 10 points
- Speed increases as your score grows

### Bonus Food (`$$`)
- Spawns after every 4 regular foods eaten
- Appears as a 2x2 block in magenta
- Timer counts down from 10 seconds
- **Faster = more points**: up to 100 points if eaten immediately, minimum 10 points
- Disappears if not collected in time

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
