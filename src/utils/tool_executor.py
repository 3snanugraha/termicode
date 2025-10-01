"""Tool execution manager"""
from typing import List, Dict, Any
from src.tools import (
    ReadTool, WriteTool, EditTool, GlobTool, GrepTool, BashTool
)


class ToolExecutor:
    """Manages and executes tools"""

    def __init__(self):
        self.tools = {
            'read_file': ReadTool(),
            'write_file': WriteTool(),
            'edit_file': EditTool(),
            'glob': GlobTool(),
            'grep': GrepTool(),
            'bash': BashTool(),
        }

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all tool definitions for function calling"""
        return [tool.to_function_definition() for tool in self.tools.values()]

    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute a tool and return result"""
        if tool_name not in self.tools:
            return f"Error: Unknown tool '{tool_name}'"

        tool = self.tools[tool_name]

        try:
            result = tool.execute(**kwargs)
            return str(result)
        except TypeError as e:
            # Handle parameter mismatches
            error_msg = str(e)
            if "unexpected keyword argument" in error_msg:
                return f"Error: Invalid parameters for {tool_name}. {error_msg}\nProvided: {list(kwargs.keys())}"
            elif "missing" in error_msg:
                return f"Error: Missing required parameters for {tool_name}. {error_msg}"
            else:
                return f"Error executing {tool_name}: {error_msg}"
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

    def execute_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Execute multiple tool calls and return results"""
        results = []

        for call in tool_calls:
            tool_name = call.get('name')
            arguments = call.get('arguments', {})

            result = self.execute_tool(tool_name, **arguments)

            results.append({
                'tool': tool_name,
                'arguments': arguments,
                'result': result
            })

        return results
