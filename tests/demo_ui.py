"""Demo of the new interactive UI features"""
import sys
import time
from src.utils import (
    Colors, Spinner, ProgressBar, print_box, print_section,
    print_success, print_error, print_info, print_warning,
    DiffViewer, FileSummary
)

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def demo_spinners():
    """Demo loading spinners"""
    print_section("Loading Animations", Colors.BRIGHT_CYAN)

    styles = ["dots", "line", "arrow", "dots2", "pulse", "bouncing"]

    for style in styles:
        spinner = Spinner(f"Loading with '{style}' style", style=style)
        spinner.start()
        time.sleep(2)
        spinner.stop()
        print_success(f"Completed {style} animation!")

    print()


def demo_progress():
    """Demo progress bars"""
    print_section("Progress Bars", Colors.BRIGHT_CYAN)

    progress = ProgressBar(total=100, title="Processing files")
    for i in range(101):
        progress.update(i)
        time.sleep(0.02)

    print()


def demo_messages():
    """Demo message types"""
    print_section("Message Types", Colors.BRIGHT_CYAN)

    print_success("Operation completed successfully!")
    print_error("An error occurred during processing")
    print_info("This is an informational message")
    print_warning("Warning: This action cannot be undone")
    print()


def demo_file_operations():
    """Demo file operation messages"""
    print_section("File Operations", Colors.BRIGHT_CYAN)

    FileSummary.print_file_created("new_module.py", lines=45)
    FileSummary.print_file_modified("main.py", additions=12, deletions=5)
    FileSummary.print_file_read("config.json", lines=120)
    FileSummary.print_command_executed("npm install", "success")
    FileSummary.print_command_executed("pytest tests/", "error")
    print()


def demo_diff():
    """Demo diff viewer"""
    print_section("Diff Viewer", Colors.BRIGHT_CYAN)

    old_code = """def calculate_sum(a, b):
    result = a + b
    print(result)
    return result
"""

    new_code = """def calculate_sum(a: int, b: int) -> int:
    '''Calculate sum of two numbers'''
    result = a + b
    return result
"""

    DiffViewer.print_diff(old_code, new_code, "math_utils.py")


def demo_box():
    """Demo text box"""
    print_section("Text Boxes", Colors.BRIGHT_CYAN)

    print_box("This is a simple box", Colors.BRIGHT_GREEN)
    print()
    print_box("Multi-line box\\nWith multiple lines\\nOf content", Colors.BRIGHT_MAGENTA, padding=2)
    print()


def main():
    """Run all demos"""
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}")
    print("═" * 60)
    print(" Terminal UI Demo ".center(60))
    print("═" * 60)
    print(f"{Colors.RESET}\n")

    demo_spinners()
    demo_progress()
    demo_messages()
    demo_file_operations()
    demo_diff()
    demo_box()

    print(f"{Colors.BRIGHT_GREEN}✓ Demo completed!{Colors.RESET}\n")


if __name__ == "__main__":
    main()
