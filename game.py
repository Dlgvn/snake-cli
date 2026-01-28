import curses
import time

from config import (
    BOARD_WIDTH, BOARD_HEIGHT, INITIAL_SPEED,
    SPEED_INCREMENT, MIN_SPEED, UP, DOWN, LEFT, RIGHT
)
from snake import Snake
from food import Food
from ui import UI
from leaderboard import save_score, is_high_score


class Game:
    def __init__(self, stdscr, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT):
        self.stdscr = stdscr
        self.board_width = board_width
        self.board_height = board_height
        self.ui = UI(stdscr, board_width, board_height)
        self.reset()

    def reset(self):
        """Reset game state for a new game."""
        self.snake = Snake(self.board_width // 2, self.board_height // 2)
        self.food = Food()
        self.food.spawn(self.snake.body, self.board_width, self.board_height)
        self.score = 0
        self.game_over = False
        self.speed = INITIAL_SPEED

    def handle_input(self):
        """Process keyboard input."""
        key = self.ui.get_input()

        if key == curses.KEY_UP:
            self.snake.change_direction(UP)
        elif key == curses.KEY_DOWN:
            self.snake.change_direction(DOWN)
        elif key == curses.KEY_LEFT:
            self.snake.change_direction(LEFT)
        elif key == curses.KEY_RIGHT:
            self.snake.change_direction(RIGHT)
        elif key in [ord('q'), ord('Q')]:
            self.game_over = True
            return False  # Signal to quit without game over screen

        return True

    def update(self):
        """Update game state."""
        # Move snake with wall wrapping
        self.snake.move(self.board_width, self.board_height)

        # Check self collision only (walls wrap around)
        if self.snake.check_self_collision():
            self.game_over = True
            return

        # Check food collision
        if self.food.is_eaten(self.snake.head):
            self.snake.grow()
            self.score += 10
            self.food.spawn(self.snake.body, self.board_width, self.board_height)

            # Increase speed
            self.speed = max(MIN_SPEED, INITIAL_SPEED - (self.score // 50) * SPEED_INCREMENT)

            # Check win condition (filled the board)
            if self.food.position is None:
                self.score += 100  # Bonus for winning
                self.game_over = True

    def run(self):
        """Main game loop."""
        show_game_over = True

        while not self.game_over:
            start_time = time.time()

            # Handle input
            if not self.handle_input():
                show_game_over = False
                break

            # Update game state
            self.update()

            # Render
            if not self.game_over:
                self.ui.render(self.snake, self.food, self.score)

            # Frame timing
            elapsed = (time.time() - start_time) * 1000
            sleep_time = max(0, self.speed - elapsed)
            time.sleep(sleep_time / 1000)

        # Game over
        if show_game_over and self.score > 0:
            self.ui.show_game_over(self.score)

            # Check for high score
            if is_high_score(self.score):
                name = self.ui.get_player_name()
                save_score(name, self.score)

        return self.score


def run_game(stdscr, board_width=BOARD_WIDTH, board_height=BOARD_HEIGHT):
    """Entry point for curses wrapper."""
    game = Game(stdscr, board_width, board_height)
    return game.run()
