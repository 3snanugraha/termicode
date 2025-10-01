"""Test write_file parsing and execution"""
from src.utils.response_parser import ResponseParser
from src.utils.tool_executor import ToolExecutor

# Simulate AI response with write_file
test_response = """Saya akan update README:

```json
{
  "tool_calls": [
    {
      "name": "write_file",
      "arguments": {
        "file_path": "test_output.md",
        "content": "# Test File\\n\\nThis is a test\\n- Item 1\\n- Item 2"
      }
    }
  ]
}
```

File telah diupdate."""

parser = ResponseParser()
executor = ToolExecutor()

# Parse response
text, tool_calls = parser.extract_tool_calls(test_response)

print("=== PARSING ===")
print(f"Tool calls found: {tool_calls is not None}")

if tool_calls:
    print(f"\n=== EXECUTING TOOLS ===")
    results = executor.execute_tool_calls(tool_calls)

    for result in results:
        print(f"\nTool: {result['tool']}")
        print(f"Result: {result['result']}")

    # Check if file was created
    import os
    if os.path.exists('test_output.md'):
        print("\n✅ File successfully created!")
        with open('test_output.md', 'r') as f:
            print(f"Content:\n{f.read()}")
    else:
        print("\n❌ File was NOT created!")
else:
    print("❌ No tool calls parsed!")
