"""Parse AI responses for tool calls"""
import json
import re
from typing import Optional, Dict, Any, List, Tuple


class ResponseParser:
    """Parse AI responses to extract tool calls"""

    @staticmethod
    def extract_tool_calls(response: str) -> Tuple[Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        Extract tool calls from AI response.
        Returns: (text_content, tool_calls)
        """
        # Try to find JSON with tool_calls (match multi-line JSON properly)
        json_pattern = r'```json\s*(\{[^`]+\})\s*```'
        json_match = re.search(json_pattern, response, re.DOTALL)

        if json_match:
            try:
                json_str = json_match.group(1)
                data = json.loads(json_str)

                if 'tool_calls' in data:
                    # Extract text before and after JSON
                    text_parts = response.split('```json')
                    text_before = text_parts[0].strip()
                    text_after = text_parts[1].split('```', 1)[1].strip() if len(text_parts[1].split('```', 1)) > 1 else ""

                    text_content = f"{text_before}\n{text_after}".strip()

                    return (text_content or None, data['tool_calls'])
            except json.JSONDecodeError as e:
                # JSON parsing failed - return as text with error info
                print(f"[DEBUG] JSON parsing failed: {e}")
                print(f"[DEBUG] Attempted to parse: {json_str[:200]}...")
                pass
            except Exception as e:
                print(f"[DEBUG] Unexpected error in extract_tool_calls: {e}")
                pass

        # No tool calls found, return full response as text
        return (response, None)

    @staticmethod
    def format_tool_results(results: List[Dict[str, Any]]) -> str:
        """Format tool execution results for display"""
        output = []

        for result in results:
            tool_name = result['tool']
            tool_result = result['result']

            output.append(f"\n[Tool: {tool_name}]")
            output.append(tool_result)
            output.append("")

        return "\n".join(output)
