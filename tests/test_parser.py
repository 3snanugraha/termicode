"""Test response parser fix"""
from src.utils.response_parser import ResponseParser

# Simulate AI response with multi-line JSON tool call
test_response = """Mari saya baca file tersebut:

```json
{
  "tool_calls": [
    {
      "name": "read_file",
      "arguments": {
        "file_path": "README.md"
      }
    }
  ]
}
```

Setelah membaca, saya akan analisis isinya."""

parser = ResponseParser()
text, tool_calls = parser.extract_tool_calls(test_response)

print("=== PARSING RESULT ===")
print(f"Text content: {text}")
print(f"\nTool calls found: {tool_calls is not None}")
if tool_calls:
    print(f"Number of tool calls: {len(tool_calls)}")
    for i, call in enumerate(tool_calls):
        print(f"\nTool {i+1}:")
        print(f"  Name: {call.get('name')}")
        print(f"  Arguments: {call.get('arguments')}")
else:
    print("No tool calls extracted!")
