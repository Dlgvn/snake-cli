import random


class Food:
    def __init__(self):
        self.position = None

    def spawn(self, snake_body, board_width, board_height):
        """Spawn food at a random position not occupied by the snake."""
        available_positions = []

        for x in range(board_width):
            for y in range(board_height):
                if (x, y) not in snake_body:
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
