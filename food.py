import random
import time

from config import BONUS_FOOD_DURATION, BONUS_MAX_SCORE, BONUS_MIN_SCORE


class Food:
    def __init__(self):
        self.position = None

    def spawn(self, snake_body, board_width, board_height, excluded_positions=None):
        """Spawn food at a random position not occupied by the snake."""
        available_positions = []
        excluded = excluded_positions or []

        for x in range(board_width):
            for y in range(board_height):
                if (x, y) not in snake_body and (x, y) not in excluded:
                    available_positions.append((x, y))

        if available_positions:
            self.position = random.choice(available_positions)
        else:
            # No space left - snake wins!
            self.position = None

        return self.position

    def is_eaten(self, snake_head):
        """Check if food was eaten by the snake."""
        return self.position == snake_head


class BonusFood:
    def __init__(self):
        self.position = None  # Top-left of 2x2 bonus food
        self.spawn_time = None
        self.active = False

    def spawn(self, snake_body, board_width, board_height, regular_food_pos=None):
        """Spawn bonus food (2x2) at a random position."""
        available_positions = []
        excluded = [regular_food_pos] if regular_food_pos else []

        # Need space for 2x2, so limit range
        for x in range(board_width - 1):
            for y in range(board_height - 1):
                # Check all 4 cells of the 2x2 area
                cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                if all(cell not in snake_body and cell not in excluded for cell in cells):
                    available_positions.append((x, y))

        if available_positions:
            self.position = random.choice(available_positions)
            self.spawn_time = time.time()
            self.active = True
        else:
            self.position = None
            self.active = False

        return self.position

    def get_all_positions(self):
        """Get all 4 positions occupied by the 2x2 bonus food."""
        if not self.position:
            return []
        x, y = self.position
        return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]

    def is_eaten(self, snake_head):
        """Check if snake head touched any part of the bonus food."""
        return self.active and snake_head in self.get_all_positions()

    def is_expired(self):
        """Check if bonus food has timed out."""
        if not self.active or not self.spawn_time:
            return False
        return time.time() - self.spawn_time > BONUS_FOOD_DURATION

    def get_time_remaining(self):
        """Get seconds remaining before bonus expires."""
        if not self.active or not self.spawn_time:
            return 0
        remaining = BONUS_FOOD_DURATION - (time.time() - self.spawn_time)
        return max(0, remaining)

    def calculate_bonus_score(self):
        """Calculate bonus score based on how quickly it was eaten."""
        if not self.spawn_time:
            return BONUS_MIN_SCORE

        elapsed = time.time() - self.spawn_time
        # Linear interpolation: fast = max score, slow = min score
        ratio = 1 - (elapsed / BONUS_FOOD_DURATION)
        ratio = max(0, min(1, ratio))  # Clamp between 0 and 1
        score = int(BONUS_MIN_SCORE + (BONUS_MAX_SCORE - BONUS_MIN_SCORE) * ratio)
        return score

    def despawn(self):
        """Remove the bonus food."""
        self.position = None
        self.spawn_time = None
        self.active = False
