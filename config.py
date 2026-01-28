# Game board dimensions
BOARD_WIDTH = 40
BOARD_HEIGHT = 20

# Speed settings (in milliseconds)
INITIAL_SPEED = 100  # ms per frame
SPEED_INCREMENT = 5  # faster as score increases
MIN_SPEED = 30  # minimum delay

# Character representations
BORDER_CHAR = '#'
SNAKE_HEAD = '@'
SNAKE_BODY = 'o'
FOOD_CHAR = '*'
BONUS_FOOD_CHAR = '$'

# Bonus food settings
BONUS_FOOD_INTERVAL = 4  # Spawn bonus after every N regular foods
BONUS_FOOD_DURATION = 10  # Seconds before bonus food disappears
BONUS_MAX_SCORE = 100  # Maximum bonus score (if eaten immediately)
BONUS_MIN_SCORE = 10  # Minimum bonus score (if eaten at last moment)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Opposite directions (to prevent 180-degree turns)
OPPOSITES = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}
