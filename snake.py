from config import UP, DOWN, LEFT, RIGHT, OPPOSITES, BOARD_WIDTH, BOARD_HEIGHT


class Snake:
    def __init__(self, start_x=None, start_y=None):
        # Start in the middle of the board
        if start_x is None:
            start_x = BOARD_WIDTH // 2
        if start_y is None:
            start_y = BOARD_HEIGHT // 2

        # Initial snake: 3 segments, moving right
        self.body = [
            (start_x, start_y),      # Head
            (start_x - 1, start_y),  # Body
            (start_x - 2, start_y),  # Tail
        ]
        self.direction = RIGHT
        self._grow_pending = False

    @property
    def head(self):
        return self.body[0]

    def change_direction(self, new_direction):
        """Change direction if not opposite to current."""
        if new_direction in OPPOSITES and OPPOSITES[new_direction] != self.direction:
            self.direction = new_direction

    def move(self, width=None, height=None):
        """Move the snake in the current direction with wall wrapping."""
        head_x, head_y = self.head
        dx, dy = self.direction
        new_x = head_x + dx
        new_y = head_y + dy

        # Wrap around walls if dimensions provided
        if width is not None:
            new_x = new_x % width
        if height is not None:
            new_y = new_y % height

        new_head = (new_x, new_y)

        # Insert new head
        self.body.insert(0, new_head)

        # Remove tail unless growing
        if self._grow_pending:
            self._grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        """Mark snake to grow on next move."""
        self._grow_pending = True

    def check_wall_collision(self, width, height):
        """Check if snake hit the wall."""
        x, y = self.head
        return x < 0 or x >= width or y < 0 or y >= height

    def check_self_collision(self):
        """Check if snake hit itself."""
        return self.head in self.body[1:]

    def check_collision(self, width, height):
        """Check for any collision."""
        return self.check_wall_collision(width, height) or self.check_self_collision()
