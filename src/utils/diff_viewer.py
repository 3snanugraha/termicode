"""Diff viewer for displaying code changes"""
import difflib
from typing import List, Tuple
from .ui_helpers import Colors


class DiffViewer:
    """Display file changes in a clean diff format"""

    @staticmethod
    def generate_diff(old_content: str, new_content: str, filename: str = "") -> List[str]:
        """Generate unified diff between old and new content"""
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm=''
        )

        return list(diff)

    @staticmethod
    def colorize_diff_line(line: str) -> str:
        """Colorize a diff line"""
        if line.startswith('+++') or line.startswith('---'):
            return f"{Colors.BOLD}{Colors.WHITE}{line}{Colors.RESET}"
        elif line.startswith('@@'):
            return f"{Colors.CYAN}{line}{Colors.RESET}"
        elif line.startswith('+'):
            return f"{Colors.BRIGHT_GREEN}{line}{Colors.RESET}"
        elif line.startswith('-'):
            return f"{Colors.BRIGHT_RED}{line}{Colors.RESET}"
        else:
            return f"{Colors.DIM}{line}{Colors.RESET}"

    @staticmethod
    def print_diff(old_content: str, new_content: str, filename: str = ""):
        """Print colorized diff"""
        diff_lines = DiffViewer.generate_diff(old_content, new_content, filename)

        if not diff_lines:
            print(f"{Colors.DIM}No changes{Colors.RESET}")
            return

        # Print header
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_BLUE}{'═' * 60}{Colors.RESET}")
        if filename:
            print(f"{Colors.BOLD}{Colors.BRIGHT_BLUE} Changes to: {filename}{Colors.RESET}")
        else:
            print(f"{Colors.BOLD}{Colors.BRIGHT_BLUE} File Changes{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_BLUE}{'═' * 60}{Colors.RESET}\n")

        # Print diff lines
        for line in diff_lines:
            print(DiffViewer.colorize_diff_line(line.rstrip()))

        print()  # Empty line after diff

    @staticmethod
    def print_side_by_side(old_content: str, new_content: str, width: int = 80):
        """Print side-by-side comparison (simplified)"""
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()

        max_lines = max(len(old_lines), len(new_lines))
        col_width = width // 2 - 3

        print(f"\n{Colors.BOLD}{'Before'.center(col_width)} │ {'After'.center(col_width)}{Colors.RESET}")
        print(f"{Colors.DIM}{'─' * col_width}─┼─{'─' * col_width}{Colors.RESET}")

        for i in range(max_lines):
            old_line = old_lines[i] if i < len(old_lines) else ""
            new_line = new_lines[i] if i < len(new_lines) else ""

            old_display = old_line[:col_width].ljust(col_width)
            new_display = new_line[:col_width].ljust(col_width)

            # Color based on difference
            if old_line != new_line:
                if not old_line:
                    # Added line
                    print(f"{Colors.DIM}{old_display}{Colors.RESET} │ {Colors.BRIGHT_GREEN}{new_display}{Colors.RESET}")
                elif not new_line:
                    # Removed line
                    print(f"{Colors.BRIGHT_RED}{old_display}{Colors.RESET} │ {Colors.DIM}{new_display}{Colors.RESET}")
                else:
                    # Modified line
                    print(f"{Colors.BRIGHT_RED}{old_display}{Colors.RESET} │ {Colors.BRIGHT_GREEN}{new_display}{Colors.RESET}")
            else:
                # Unchanged line
                print(f"{Colors.DIM}{old_display} │ {new_display}{Colors.RESET}")

        print()


class FileSummary:
    """Display file operation summary"""

    @staticmethod
    def print_file_created(filename: str, lines: int = 0):
        """Print file created message"""
        print(f"{Colors.BRIGHT_GREEN}✓{Colors.RESET} Created: {Colors.BOLD}{filename}{Colors.RESET}", end='')
        if lines > 0:
            print(f" {Colors.DIM}({lines} lines){Colors.RESET}")
        else:
            print()

    @staticmethod
    def print_file_modified(filename: str, additions: int = 0, deletions: int = 0):
        """Print file modified message"""
        print(f"{Colors.BRIGHT_YELLOW}✓{Colors.RESET} Modified: {Colors.BOLD}{filename}{Colors.RESET}", end='')
        if additions > 0 or deletions > 0:
            parts = []
            if additions > 0:
                parts.append(f"{Colors.BRIGHT_GREEN}+{additions}{Colors.RESET}")
            if deletions > 0:
                parts.append(f"{Colors.BRIGHT_RED}-{deletions}{Colors.RESET}")
            print(f" {Colors.DIM}({', '.join(parts)}){Colors.RESET}")
        else:
            print()

    @staticmethod
    def print_file_read(filename: str, lines: int = 0):
        """Print file read message"""
        print(f"{Colors.BRIGHT_BLUE}ℹ{Colors.RESET} Reading: {Colors.BOLD}{filename}{Colors.RESET}", end='')
        if lines > 0:
            print(f" {Colors.DIM}({lines} lines){Colors.RESET}")
        else:
            print()

    @staticmethod
    def print_command_executed(command: str, status: str = "success"):
        """Print command execution message"""
        icon = f"{Colors.BRIGHT_GREEN}✓{Colors.RESET}" if status == "success" else f"{Colors.BRIGHT_RED}✗{Colors.RESET}"
        print(f"{icon} Executed: {Colors.DIM}${Colors.RESET} {Colors.BOLD}{command}{Colors.RESET}")
