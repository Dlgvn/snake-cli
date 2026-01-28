import curses
from config import BORDER_CHAR, SNAKE_HEAD, SNAKE_BODY, FOOD_CHAR


class UI:
    def __init__(self, stdscr, board_width, board_height):
        self.stdscr = stdscr
        self.board_width = board_width
        self.board_height = board_height

        # Calculate offsets for centering
        self.offset_x = 2
        self.offset_y = 3

        # Setup curses
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(True)  # Non-blocking input
        self.stdscr.keypad(True)  # Enable arrow keys

        # Initialize colors if available
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Snake
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Food
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Border
            curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # UI

    def draw_border(self):
        """Draw the Nokia-style game border."""
        color = curses.color_pair(3) if curses.has_colors() else 0
        ui_color = curses.color_pair(4) if curses.has_colors() else 0

        # Top UI border
        self.stdscr.addstr(0, 0, '┌' + '─' * (self.board_width + 4) + '┐', ui_color)
        self.stdscr.addstr(1, 0, '│', ui_color)
        self.stdscr.addstr(2, 0, '├' + '─' * (self.board_width + 4) + '┤', ui_color)

        # Game area border
        for y in range(self.board_height + 2):
            self.stdscr.addstr(self.offset_y + y, 0, '│ ', ui_color)
            self.stdscr.addstr(self.offset_y + y, self.board_width + 5, ' │', ui_color)

        # Top border of game area
        self.stdscr.addstr(self.offset_y, self.offset_x, BORDER_CHAR * (self.board_width + 2), color)

        # Side borders of game area
        for y in range(self.board_height):
            self.stdscr.addstr(self.offset_y + 1 + y, self.offset_x, BORDER_CHAR, color)
            self.stdscr.addstr(self.offset_y + 1 + y, self.offset_x + self.board_width + 1, BORDER_CHAR, color)

        # Bottom border of game area
        self.stdscr.addstr(self.offset_y + self.board_height + 1, self.offset_x,
                          BORDER_CHAR * (self.board_width + 2), color)

        # Bottom UI borders
        bottom = self.offset_y + self.board_height + 2
        self.stdscr.addstr(bottom, 0, '├' + '─' * (self.board_width + 4) + '┤', ui_color)
        self.stdscr.addstr(bottom + 1, 0, '│', ui_color)
        self.stdscr.addstr(bottom + 1, self.board_width + 5, '│', ui_color)
        self.stdscr.addstr(bottom + 2, 0, '└' + '─' * (self.board_width + 4) + '┘', ui_color)

    def draw_score(self, score):
        """Draw the score at the top."""
        ui_color = curses.color_pair(4) if curses.has_colors() else 0
        title = "  SNAKE"
        score_text = f"Score: {score}"
        padding = self.board_width + 4 - len(title) - len(score_text)
        self.stdscr.addstr(1, 1, title + ' ' * padding + score_text + ' ', ui_color)

    def draw_controls(self):
        """Draw control hints at the bottom."""
        ui_color = curses.color_pair(4) if curses.has_colors() else 0
        bottom = self.offset_y + self.board_height + 3
        controls = "  ← → ↑ ↓ to move   Q to quit"
        padding = self.board_width + 4 - len(controls)
        self.stdscr.addstr(bottom, 1, controls + ' ' * max(0, padding), ui_color)

    def draw_snake(self, snake):
        """Draw the snake on the board."""
        color = curses.color_pair(1) if curses.has_colors() else 0

        for i, (x, y) in enumerate(snake.body):
            char = SNAKE_HEAD if i == 0 else SNAKE_BODY
            screen_x = self.offset_x + 1 + x
            screen_y = self.offset_y + 1 + y
            try:
                self.stdscr.addch(screen_y, screen_x, char, color)
            except curses.error:
                pass

    def draw_food(self, food):
        """Draw the food on the board."""
        if food.position is None:
            return

        color = curses.color_pair(2) if curses.has_colors() else 0
        x, y = food.position
        screen_x = self.offset_x + 1 + x
        screen_y = self.offset_y + 1 + y
        try:
            self.stdscr.addch(screen_y, screen_x, FOOD_CHAR, color)
        except curses.error:
            pass

    def clear_game_area(self):
        """Clear only the game area."""
        for y in range(self.board_height):
            for x in range(self.board_width):
                screen_x = self.offset_x + 1 + x
                screen_y = self.offset_y + 1 + y
                try:
                    self.stdscr.addch(screen_y, screen_x, ' ')
                except curses.error:
                    pass

    def render(self, snake, food, score):
        """Render the complete game frame."""
        self.stdscr.clear()
        self.draw_border()
        self.draw_score(score)
        self.draw_controls()
        self.draw_snake(snake)
        self.draw_food(food)
        self.stdscr.refresh()

    def get_input(self):
        """Get keyboard input (non-blocking)."""
        try:
            return self.stdscr.getch()
        except:
            return -1

    def show_game_over(self, score):
        """Display game over screen."""
        self.stdscr.clear()
        ui_color = curses.color_pair(4) if curses.has_colors() else 0

        center_y = (self.board_height + 8) // 2
        center_x = (self.board_width + 6) // 2

        messages = [
            "╔══════════════════╗",
            "║    GAME OVER!    ║",
            f"║   Score: {score:5}   ║",
            "║                  ║",
            "║  Press ENTER to  ║",
            "║  continue...     ║",
            "╚══════════════════╝"
        ]

        for i, msg in enumerate(messages):
            x = center_x - len(msg) // 2
            self.stdscr.addstr(center_y - 3 + i, x, msg, ui_color)

        self.stdscr.refresh()
        self.stdscr.nodelay(False)

        while True:
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER, 10, 13]:
                break

        self.stdscr.nodelay(True)

    def show_menu(self):
        """Display main menu and return selection."""
        self.stdscr.nodelay(False)
        selected = 0
        options = ["New Game", "Leaderboard", "Quit"]

        while True:
            self.stdscr.clear()
            ui_color = curses.color_pair(4) if curses.has_colors() else 0
            snake_color = curses.color_pair(1) if curses.has_colors() else 0

            center_y = 5
            center_x = (self.board_width + 6) // 2

            # ASCII art title
            title = [
                " ███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗",
                " ██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝",
                " ███████╗██╔██╗ ██║███████║█████╔╝ █████╗  ",
                " ╚════██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  ",
                " ███████║██║ ╚████║██║  ██║██║  ██╗███████╗",
                " ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝"
            ]

            for i, line in enumerate(title):
                x = center_x - len(line) // 2
                try:
                    self.stdscr.addstr(center_y + i, max(0, x), line, snake_color)
                except curses.error:
                    pass

            menu_y = center_y + len(title) + 3

            for i, option in enumerate(options):
                prefix = "► " if i == selected else "  "
                text = prefix + option
                x = center_x - len(text) // 2
                attr = curses.A_BOLD if i == selected else 0
                try:
                    self.stdscr.addstr(menu_y + i * 2, x, text, ui_color | attr)
                except curses.error:
                    pass

            hint = "Use ↑↓ to select, ENTER to confirm"
            try:
                self.stdscr.addstr(menu_y + len(options) * 2 + 2,
                                  center_x - len(hint) // 2, hint, ui_color)
            except curses.error:
                pass

            self.stdscr.refresh()

            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                selected = (selected - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected = (selected + 1) % len(options)
            elif key in [curses.KEY_ENTER, 10, 13]:
                self.stdscr.nodelay(True)
                return selected

    def show_leaderboard(self, scores):
        """Display the leaderboard."""
        self.stdscr.nodelay(False)
        self.stdscr.clear()

        ui_color = curses.color_pair(4) if curses.has_colors() else 0
        gold_color = curses.color_pair(3) if curses.has_colors() else 0

        center_x = (self.board_width + 6) // 2

        self.stdscr.addstr(2, center_x - 7, "═══ LEADERBOARD ═══", gold_color)

        if not scores:
            self.stdscr.addstr(6, center_x - 8, "No scores yet!", ui_color)
        else:
            for i, entry in enumerate(scores):
                rank = f"{i + 1:2}."
                name = entry['name'][:10].ljust(10)
                score = f"{entry['score']:5}"
                line = f"{rank} {name} {score}"
                color = gold_color if i < 3 else ui_color
                self.stdscr.addstr(5 + i, center_x - len(line) // 2, line, color)

        hint = "Press ENTER to return"
        self.stdscr.addstr(18, center_x - len(hint) // 2, hint, ui_color)

        self.stdscr.refresh()

        while True:
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER, 10, 13]:
                break

    def get_player_name(self):
        """Get player name for leaderboard."""
        self.stdscr.nodelay(False)
        curses.echo()
        curses.curs_set(1)

        ui_color = curses.color_pair(4) if curses.has_colors() else 0
        center_x = (self.board_width + 6) // 2
        center_y = (self.board_height + 8) // 2

        self.stdscr.clear()
        self.stdscr.addstr(center_y - 2, center_x - 10, "NEW HIGH SCORE!", ui_color | curses.A_BOLD)
        self.stdscr.addstr(center_y, center_x - 12, "Enter your name: ", ui_color)
        self.stdscr.refresh()

        name = ""
        try:
            name = self.stdscr.getstr(center_y, center_x + 5, 10).decode('utf-8')
        except:
            name = "Player"

        curses.noecho()
        curses.curs_set(0)
        self.stdscr.nodelay(True)

        return name.strip() or "Player"
