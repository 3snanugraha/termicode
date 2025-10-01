"""File operation tools"""
import os
import glob as glob_module
import re
from pathlib import Path
from typing import Dict, Any
from .base import Tool, ToolResult


class ReadTool(Tool):
    """Read file contents"""

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Read contents of a file. Returns file content with line numbers."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read"
                },
                "start_line": {
                    "type": "integer",
                    "description": "Optional: Line number to start reading from (1-indexed)"
                },
                "end_line": {
                    "type": "integer",
                    "description": "Optional: Line number to stop reading at (inclusive)"
                }
            },
            "required": ["file_path"]
        }

    def execute(self, file_path: str, start_line: int = None, end_line: int = None) -> ToolResult:
        try:
            # Convert to absolute path if relative
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            if not os.path.exists(file_path):
                return ToolResult(success=False, output="", error=f"File not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if start_line is not None:
                start_line = max(1, start_line) - 1
            else:
                start_line = 0

            if end_line is not None:
                end_line = min(len(lines), end_line)
            else:
                end_line = len(lines)

            numbered_lines = [f"{i+1:4d} | {line.rstrip()}" for i, line in enumerate(lines[start_line:end_line], start=start_line)]
            output = "\n".join(numbered_lines)

            return ToolResult(success=True, output=output)
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))


class WriteTool(Tool):
    """Write content to a file"""

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Write content to a file. Creates new file or overwrites existing file."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }

    def execute(self, file_path: str, content: str) -> ToolResult:
        try:
            # Convert to absolute path if relative
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            # Create directory if it doesn't exist
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Verify file was created
            if not os.path.exists(file_path):
                return ToolResult(success=False, output="", error=f"File was not created: {file_path}")

            return ToolResult(success=True, output=f"File written successfully: {file_path}")
        except Exception as e:
            return ToolResult(success=False, output="", error=f"{str(e)} (attempted path: {file_path})")


class EditTool(Tool):
    """Edit file by replacing text"""

    @property
    def name(self) -> str:
        return "edit_file"

    @property
    def description(self) -> str:
        return "Edit a file by replacing old_text with new_text. Supports replace_all option."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to edit"
                },
                "old_text": {
                    "type": "string",
                    "description": "Text to find and replace (must be exact match)"
                },
                "new_text": {
                    "type": "string",
                    "description": "Text to replace with"
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "If true, replace all occurrences. If false, replace only first occurrence.",
                    "default": False
                }
            },
            "required": ["file_path", "old_text", "new_text"]
        }

    def execute(self, file_path: str, old_text: str, new_text: str, replace_all: bool = False) -> ToolResult:
        try:
            # Convert to absolute path if relative
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            if not os.path.exists(file_path):
                return ToolResult(success=False, output="", error=f"File not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if old_text not in content:
                return ToolResult(success=False, output="", error="Text to replace not found in file")

            if replace_all:
                new_content = content.replace(old_text, new_text)
                count = content.count(old_text)
            else:
                new_content = content.replace(old_text, new_text, 1)
                count = 1

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return ToolResult(success=True, output=f"Replaced {count} occurrence(s) in {file_path}")
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))


class GlobTool(Tool):
    """Find files matching pattern"""

    @property
    def name(self) -> str:
        return "glob"

    @property
    def description(self) -> str:
        return "Find files matching a glob pattern (e.g., '**/*.py', 'src/*.js')"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern to match files"
                },
                "path": {
                    "type": "string",
                    "description": "Base directory to search in (default: current directory)"
                }
            },
            "required": ["pattern"]
        }

    def execute(self, pattern: str, path: str = ".") -> ToolResult:
        try:
            os.chdir(path)
            matches = glob_module.glob(pattern, recursive=True)
            matches = sorted([str(Path(m)) for m in matches if os.path.isfile(m)])

            if not matches:
                return ToolResult(success=True, output="No files found matching pattern")

            output = "\n".join(matches)
            return ToolResult(success=True, output=output)
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))


class GrepTool(Tool):
    """Search for pattern in files"""

    @property
    def name(self) -> str:
        return "grep"

    @property
    def description(self) -> str:
        return "Search for a regex pattern in files. Can filter by file type."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for"
                },
                "path": {
                    "type": "string",
                    "description": "Directory or file to search in (default: current directory)"
                },
                "file_pattern": {
                    "type": "string",
                    "description": "Glob pattern to filter files (e.g., '*.py')"
                },
                "case_insensitive": {
                    "type": "boolean",
                    "description": "If true, search is case-insensitive",
                    "default": False
                },
                "show_line_numbers": {
                    "type": "boolean",
                    "description": "If true, show line numbers",
                    "default": True
                }
            },
            "required": ["pattern"]
        }

    def execute(
        self,
        pattern: str,
        path: str = ".",
        file_pattern: str = "*",
        case_insensitive: bool = False,
        show_line_numbers: bool = True
    ) -> ToolResult:
        try:
            flags = re.IGNORECASE if case_insensitive else 0
            regex = re.compile(pattern, flags)

            results = []

            # Find files to search
            if os.path.isfile(path):
                files = [path]
            else:
                glob_pattern = os.path.join(path, "**", file_pattern)
                files = glob_module.glob(glob_pattern, recursive=True)
                files = [f for f in files if os.path.isfile(f)]

            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if regex.search(line):
                                if show_line_numbers:
                                    results.append(f"{file_path}:{line_num}: {line.rstrip()}")
                                else:
                                    results.append(f"{file_path}: {line.rstrip()}")
                except Exception:
                    continue

            if not results:
                return ToolResult(success=True, output="No matches found")

            output = "\n".join(results)
            return ToolResult(success=True, output=output)
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
