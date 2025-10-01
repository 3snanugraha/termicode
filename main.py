#!/usr/bin/env python3
"""Interactive CLI interface for Terminal Coding Assistant with enhanced UI"""
import os
import sys
from dotenv import load_dotenv
from src.assistant import CodingAssistant
from src.utils import Colors, Spinner, print_box, print_section, print_success, print_error, print_info

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables from .env file
load_dotenv()


def print_banner():
    """Print welcome banner"""
    banner = f"""{Colors.BRIGHT_CYAN}
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        {Colors.BOLD}Terminal Coding Assistant by Tris{Colors.RESET}{Colors.BRIGHT_CYAN}                       ║
║                                                            ║
║  {Colors.BRIGHT_WHITE}AI-powered coding assistant for your terminal{Colors.BRIGHT_CYAN}           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

    print(f"{Colors.DIM}Features:{Colors.RESET}")
    print(f"  {Colors.BRIGHT_GREEN}•{Colors.RESET} Read & analyze files")
    print(f"  {Colors.BRIGHT_GREEN}•{Colors.RESET} Write & edit code")
    print(f"  {Colors.BRIGHT_GREEN}•{Colors.RESET} Search patterns")
    print(f"  {Colors.BRIGHT_GREEN}•{Colors.RESET} Run shell commands")
    print(f"  {Colors.BRIGHT_GREEN}•{Colors.RESET} Interactive diff viewer")
    print()
    print(f"{Colors.DIM}Commands: {Colors.BRIGHT_WHITE}clear{Colors.DIM}, {Colors.BRIGHT_WHITE}pwd{Colors.DIM}, {Colors.BRIGHT_WHITE}exit{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}\n")


def main():
    """Main CLI loop with enhanced UI"""
    # Check for HF_TOKEN
    if not os.environ.get("HF_TOKEN"):
        print_error("HF_TOKEN environment variable is not set!")
        print(f"{Colors.YELLOW}Please set it with: {Colors.BOLD}export HF_TOKEN='your-token'{Colors.RESET}")
        sys.exit(1)

    # Initialize assistant
    spinner = Spinner("Initializing AI assistant", style="dots")
    spinner.start()

    try:
        assistant = CodingAssistant()
        spinner.stop()
        print_success("AI assistant ready!")
    except Exception as e:
        spinner.stop()
        print_error(f"Failed to initialize assistant: {e}")
        sys.exit(1)

    # Print banner
    print()
    print_banner()
    print_info(f"Working Directory: {Colors.BOLD}{os.getcwd()}{Colors.RESET}")
    print()

    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input(f"{Colors.BOLD}{Colors.BRIGHT_GREEN}You ▶{Colors.RESET} ")

            if not user_input.strip():
                continue

            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print(f"\n{Colors.BRIGHT_CYAN}Goodbye! 👋{Colors.RESET}\n")
                break

            # Check for special commands
            if user_input.lower() == 'clear':
                assistant.reset_conversation()
                print_success("Conversation history cleared.")
                continue

            if user_input.lower() == 'pwd':
                print_info(f"Current directory: {Colors.BOLD}{os.getcwd()}{Colors.RESET}")
                continue

            # Show thinking spinner
            print()
            thinking_spinner = Spinner("AI is thinking", style="dots2")
            thinking_spinner.start()

            # Collect response
            response_chunks = []
            try:
                for chunk in assistant.process_message_stream_interactive(user_input):
                    response_chunks.append(chunk)
            except AttributeError:
                # Fallback if interactive mode not available
                thinking_spinner.stop()
                print(f"{Colors.BRIGHT_BLUE}Assistant ▶{Colors.RESET}\n")
                for chunk in assistant.process_message_stream(user_input):
                    print(chunk, end='', flush=True)
                    response_chunks.append(chunk)
                print("\n")
                continue

            thinking_spinner.stop()

            # Display response
            full_response = "".join(response_chunks)

            if full_response.strip():
                print(f"{Colors.BRIGHT_BLUE}Assistant ▶{Colors.RESET}")
                print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")
                print(f"{full_response}")
                print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")

            print()

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⚠ Interrupted. Type 'exit' to quit.{Colors.RESET}\n")
            continue

        except EOFError:
            # Handle EOF (when stdin is closed or no interactive input)
            print(f"\n{Colors.BRIGHT_CYAN}Goodbye! 👋{Colors.RESET}\n")
            break

        except Exception as e:
            print_error(f"An error occurred: {e}")
            if os.environ.get("DEBUG"):
                import traceback
                traceback.print_exc()
            print()
            continue


if __name__ == "__main__":
    main()
