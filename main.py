#!/usr/bin/env python3
"""
Snake CLI - A Nokia-style Snake game for the terminal.

Controls:
    Arrow keys - Change direction
    Q - Quit game

Usage:
    python main.py [--width WIDTH] [--height HEIGHT] [--speed SPEED]
"""

import argparse
import curses
import sys

from config import BOARD_WIDTH, BOARD_HEIGHT, INITIAL_SPEED
from game import Game
from ui import UI
from leaderboard import get_top_scores


def main(stdscr, args):
    """Main application loop."""
    # Initialize UI for menu
    ui = UI(stdscr, args.width, args.height)

    while True:
        choice = ui.show_menu()

        if choice == 0:  # New Game
            game = Game(stdscr, args.width, args.height)
            game.run()
        elif choice == 1:  # Leaderboard
            scores = get_top_scores()
            ui.show_leaderboard(scores)
        elif choice == 2:  # Quit
            break


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Snake CLI - A Nokia-style Snake game for the terminal.'
    )
    parser.add_argument(
        '--width', '-w',
        type=int,
        default=BOARD_WIDTH,
        help=f'Board width (default: {BOARD_WIDTH})'
    )
    parser.add_argument(
        '--height', '-H',
        type=int,
        default=BOARD_HEIGHT,
        help=f'Board height (default: {BOARD_HEIGHT})'
    )
    parser.add_argument(
        '--speed', '-s',
        type=int,
        default=INITIAL_SPEED,
        help=f'Initial speed in ms per frame (default: {INITIAL_SPEED})'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    # Validate arguments
    if args.width < 10:
        print("Error: Width must be at least 10")
        sys.exit(1)
    if args.height < 10:
        print("Error: Height must be at least 10")
        sys.exit(1)
    if args.speed < 10:
        print("Error: Speed must be at least 10ms")
        sys.exit(1)

    try:
        curses.wrapper(lambda stdscr: main(stdscr, args))
    except KeyboardInterrupt:
        pass
    except curses.error as e:
        print(f"Terminal error: {e}")
        print("Make sure your terminal window is large enough.")
        sys.exit(1)
