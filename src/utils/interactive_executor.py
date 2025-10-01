"""Interactive tool executor with UI enhancements"""
import os
from typing import List, Dict, Any
from .tool_executor import ToolExecutor
from .ui_helpers import Colors, Spinner, print_success, print_error, print_info, clear_line
from .diff_viewer import DiffViewer, FileSummary


class InteractiveToolExecutor(ToolExecutor):
    """Enhanced tool executor with interactive UI"""

    def __init__(self, verbose: bool = False):
        super().__init__()
        self.verbose = verbose
        self._file_cache: Dict[str, str] = {}  # Cache original file contents for diffs

    def execute_tool_calls_interactive(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Execute tool calls with interactive UI feedback"""
        results = []

        for i, call in enumerate(tool_calls, 1):
            tool_name = call.get('name')
            arguments = call.get('arguments', {})

            # Show spinner for tool execution
            spinner = Spinner(f"Executing {tool_name}", style="dots")
            spinner.start()

            result = self.execute_tool(tool_name, **arguments)

            spinner.stop()

            # Display result based on tool type
            self._display_tool_result(tool_name, arguments, result)

            results.append({
                'tool': tool_name,
                'arguments': arguments,
                'result': result
            })

        return results

    def _display_tool_result(self, tool_name: str, arguments: Dict[str, Any], result: str):
        """Display tool execution result with appropriate formatting"""
        file_path = arguments.get('file_path', '')

        if tool_name == "read_file":
            self._display_read_result(file_path, result)

        elif tool_name == "write_file":
            self._display_write_result(file_path, arguments.get('content', ''), result)

        elif tool_name == "edit_file":
            self._display_edit_result(file_path, arguments, result)

        elif tool_name == "bash":
            self._display_bash_result(arguments.get('command', ''), result)

        elif tool_name == "glob":
            self._display_glob_result(arguments.get('pattern', ''), result)

        elif tool_name == "grep":
            self._display_grep_result(arguments.get('pattern', ''), result)

        else:
            # Generic display
            if "Error:" in result:
                print_error(result)
            else:
                print_success(result)

    def _display_read_result(self, file_path: str, result: str):
        """Display file read result"""
        if result.startswith("Error:"):
            print_error(f"Failed to read {file_path}")
            # Always show error details (even if not verbose)
            print(f"{Colors.DIM}{result}{Colors.RESET}")
        else:
            lines = result.count('\n') + 1
            FileSummary.print_file_read(file_path, lines)

            # Cache content for potential diffs later
            self._file_cache[file_path] = result

            if self.verbose:
                print(f"\n{Colors.DIM}{result}{Colors.RESET}\n")

    def _display_write_result(self, file_path: str, content: str, result: str):
        """Display file write result"""
        if result.startswith("Error:"):
            print_error(f"Failed to create {file_path}")
            # Always show error details
            print(f"{Colors.DIM}{result}{Colors.RESET}")
        else:
            # Show success message
            lines = content.count('\n') + 1
            FileSummary.print_file_created(file_path, lines)

            # Verify file was actually created
            import os
            if not os.path.exists(file_path):
                print_error(f"Warning: File was reported as created but does not exist at {file_path}")
                if self.verbose:
                    print(f"{Colors.DIM}Result: {result}{Colors.RESET}")

    def _display_edit_result(self, file_path: str, arguments: Dict[str, Any], result: str):
        """Display file edit result with diff"""
        if result.startswith("Error:"):
            print_error(f"Failed to edit {file_path}")
            # Always show error details
            print(f"{Colors.DIM}{result}{Colors.RESET}")
            return

        # Get old and new content
        old_content = self._file_cache.get(file_path, "")

        # Read new content
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    new_content = f.read()

                # Calculate changes
                old_lines = old_content.splitlines()
                new_lines = new_content.splitlines()
                additions = len([l for l in new_lines if l not in old_lines])
                deletions = len([l for l in old_lines if l not in new_lines])

                FileSummary.print_file_modified(file_path, additions, deletions)

                # Show diff
                if old_content:
                    DiffViewer.print_diff(old_content, new_content, file_path)
                else:
                    print_info("No previous content cached to show diff")

                # Update cache
                self._file_cache[file_path] = new_content
            else:
                FileSummary.print_file_modified(file_path)
        except Exception as e:
            if self.verbose:
                print_error(f"Could not display diff: {e}")
            else:
                FileSummary.print_file_modified(file_path)

    def _display_bash_result(self, command: str, result: str):
        """Display bash command result"""
        if result.startswith("Error:"):
            FileSummary.print_command_executed(command, "error")
            if self.verbose:
                print(f"\n{Colors.BRIGHT_RED}{result}{Colors.RESET}\n")
        else:
            FileSummary.print_command_executed(command, "success")
            if self.verbose and result and result != "Command executed successfully (no output)":
                print(f"\n{Colors.DIM}Output:{Colors.RESET}")
                print(f"{Colors.DIM}{result}{Colors.RESET}\n")

    def _display_glob_result(self, pattern: str, result: str):
        """Display glob search result"""
        if result.startswith("Error:"):
            print_error(f"Failed to search for pattern: {pattern}")
            if self.verbose:
                print(f"{Colors.DIM}{result}{Colors.RESET}")
        else:
            matches = result.splitlines() if result != "No files found matching pattern" else []
            print_info(f"Found {len(matches)} file(s) matching '{pattern}'")

            if matches and self.verbose:
                for match in matches[:10]:  # Limit to first 10
                    print(f"  {Colors.DIM}•{Colors.RESET} {match}")
                if len(matches) > 10:
                    print(f"  {Colors.DIM}... and {len(matches) - 10} more{Colors.RESET}")

    def _display_grep_result(self, pattern: str, result: str):
        """Display grep search result"""
        if result.startswith("Error:"):
            print_error(f"Failed to search for pattern: {pattern}")
            if self.verbose:
                print(f"{Colors.DIM}{result}{Colors.RESET}")
        else:
            matches = result.splitlines() if result != "No matches found" else []
            print_info(f"Found {len(matches)} match(es) for '{pattern}'")

            if matches and self.verbose:
                for match in matches[:10]:  # Limit to first 10
                    print(f"  {Colors.DIM}{match}{Colors.RESET}")
                if len(matches) > 10:
                    print(f"  {Colors.DIM}... and {len(matches) - 10} more{Colors.RESET}")
