"""Bash command execution tool"""
import subprocess
import os
from typing import Dict, Any
from .base import Tool, ToolResult


class BashTool(Tool):
    """Execute bash/shell commands"""

    @property
    def name(self) -> str:
        return "bash"

    @property
    def description(self) -> str:
        return "Execute a bash/shell command and return the output. Use for git, npm, pip, and other CLI tools."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (default: 30)",
                    "default": 30
                }
            },
            "required": ["command"]
        }

    def execute(self, command: str, timeout: int = 30) -> ToolResult:
        try:
            # Use shell=True to support commands with pipes, redirects, etc.
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd()
            )

            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"

            if result.returncode != 0:
                return ToolResult(
                    success=False,
                    output=output,
                    error=f"Command exited with code {result.returncode}"
                )

            return ToolResult(success=True, output=output or "Command executed successfully (no output)")

        except subprocess.TimeoutExpired:
            return ToolResult(success=False, output="", error=f"Command timed out after {timeout} seconds")
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
