"""UI helpers for terminal interface"""
import sys
import time
import threading
from typing import Optional


class Colors:
    """ANSI color codes"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class Spinner:
    """Animated loading spinner"""

    def __init__(self, message: str = "Processing", style: str = "dots"):
        self.message = message
        self.is_running = False
        self.thread: Optional[threading.Thread] = None

        self.styles = {
            "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "line": ["-", "\\", "|", "/"],
            "arrow": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
            "dots2": ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],
            "pulse": ["◐", "◓", "◑", "◒"],
            "bouncing": ["⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"],
        }
        self.frames = self.styles.get(style, self.styles["dots"])
        self.current_frame = 0

    def _spin(self):
        """Spinner animation loop"""
        while self.is_running:
            frame = self.frames[self.current_frame]
            sys.stdout.write(f'\r{Colors.CYAN}{frame}{Colors.RESET} {Colors.DIM}{self.message}...{Colors.RESET}')
            sys.stdout.flush()
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            time.sleep(0.1)

        # Clear the spinner line
        sys.stdout.write('\r' + ' ' * (len(self.message) + 20) + '\r')
        sys.stdout.flush()

    def start(self):
        """Start the spinner"""
        self.is_running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the spinner"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=0.5)

    def update_message(self, message: str):
        """Update spinner message"""
        self.message = message


class ProgressBar:
    """Simple progress bar"""

    def __init__(self, total: int, width: int = 40, title: str = "Progress"):
        self.total = total
        self.current = 0
        self.width = width
        self.title = title

    def update(self, current: int):
        """Update progress"""
        self.current = current
        self.draw()

    def draw(self):
        """Draw progress bar"""
        if self.total == 0:
            percent = 100
        else:
            percent = int((self.current / self.total) * 100)

        filled = int((self.current / self.total) * self.width) if self.total > 0 else self.width
        bar = "█" * filled + "░" * (self.width - filled)

        sys.stdout.write(f'\r{Colors.CYAN}{self.title}{Colors.RESET}: [{bar}] {percent}%')
        sys.stdout.flush()

        if self.current >= self.total:
            sys.stdout.write('\n')

    def increment(self):
        """Increment progress by 1"""
        self.update(self.current + 1)


def print_box(text: str, color: str = Colors.CYAN, padding: int = 1):
    """Print text in a box"""
    lines = text.split('\n')
    max_length = max(len(line) for line in lines) if lines else 0
    width = max_length + (padding * 2)

    # Top border
    print(f"{color}╭{'─' * width}╮{Colors.RESET}")

    # Content
    for line in lines:
        padded_line = line.ljust(max_length)
        print(f"{color}│{Colors.RESET}{' ' * padding}{padded_line}{' ' * padding}{color}│{Colors.RESET}")

    # Bottom border
    print(f"{color}╰{'─' * width}╯{Colors.RESET}")


def print_section(title: str, color: str = Colors.BRIGHT_BLUE):
    """Print a section header"""
    print(f"\n{color}{'═' * 60}{Colors.RESET}")
    print(f"{color}{Colors.BOLD} {title}{Colors.RESET}")
    print(f"{color}{'═' * 60}{Colors.RESET}\n")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.BRIGHT_GREEN}✓ {Colors.RESET} {message}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.BRIGHT_RED}✗ {Colors.RESET} {message}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.BRIGHT_BLUE}ℹ {Colors.RESET} {message}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.BRIGHT_YELLOW}⚠ {Colors.RESET} {message}")


def clear_line():
    """Clear current line"""
    sys.stdout.write('\r' + ' ' * 100 + '\r')
    sys.stdout.flush()


def clear_lines(n: int):
    """Clear n lines"""
    for _ in range(n):
        sys.stdout.write('\033[F\033[K')
    sys.stdout.flush()
