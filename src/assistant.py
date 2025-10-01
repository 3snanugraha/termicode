"""Main assistant logic"""
import os
import re
from typing import List, Dict, Any
from src.ai_client import AIClient
from src.utils.tool_executor import ToolExecutor
from src.utils.interactive_executor import InteractiveToolExecutor
from src.utils.response_parser import ResponseParser
from src.prompts import get_system_prompt


class CodingAssistant:
    """Terminal-based coding assistant"""

    def __init__(self, model: str = None, interactive: bool = True):
        # Read model from environment if not provided
        if model is None:
            model = os.getenv('MODEL', 'deepseek-ai/DeepSeek-V3.2-Exp')

        self.ai_client = AIClient(model=model)
        self.tool_executor = ToolExecutor()
        self.interactive_executor = InteractiveToolExecutor(verbose=False) if interactive else None
        self.response_parser = ResponseParser()
        self.conversation_history: List[Dict[str, str]] = []

        # Read MODE from environment (DEBUG or SILENT)
        self.mode = os.getenv('MODE', 'SILENT').upper()

        # Initialize with system prompt
        self.system_prompt = get_system_prompt()

    def _get_messages(self) -> List[Dict[str, str]]:
        """Get messages for API call including system prompt"""
        return [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history
        ]

    def process_message(self, user_message: str) -> str:
        """Process user message and return response"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get AI response
        messages = self._get_messages()
        response = self.ai_client.chat(messages, temperature=0.7)

        assistant_message = response.content

        # Parse response for tool calls
        text_content, tool_calls = self.response_parser.extract_tool_calls(assistant_message)

        full_response_parts = []

        # Add text content if any
        if text_content:
            full_response_parts.append(text_content)

        # Execute tool calls if present
        if tool_calls:
            tool_results = self.tool_executor.execute_tool_calls(tool_calls)
            tool_output = self.response_parser.format_tool_results(tool_results)
            full_response_parts.append(tool_output)

            # Add tool results to conversation for context
            tool_context = f"Tool execution results:\n{tool_output}"
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            self.conversation_history.append({
                "role": "user",
                "content": tool_context
            })

            # Get follow-up response from AI
            messages = self._get_messages()
            follow_up = self.ai_client.chat(messages, temperature=0.7)
            follow_up_content = follow_up.content

            full_response_parts.append("\n" + follow_up_content)

            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": follow_up_content
            })
        else:
            # No tool calls, just add assistant message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

        return "\n".join(full_response_parts)

    def process_message_stream(self, user_message: str):
        """Process message with streaming response"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Stream AI response
        messages = self._get_messages()
        full_response = []

        for chunk in self.ai_client.chat_stream(messages, temperature=0.7):
            full_response.append(chunk)
            yield chunk

        # Process complete response for tool calls
        assistant_message = "".join(full_response)
        text_content, tool_calls = self.response_parser.extract_tool_calls(assistant_message)

        # Execute tool calls if present
        if tool_calls:
            yield "\n\n"

            tool_results = self.tool_executor.execute_tool_calls(tool_calls)
            tool_output = self.response_parser.format_tool_results(tool_results)
            yield tool_output

            # Add to conversation history
            tool_context = f"Tool execution results:\n{tool_output}"
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            self.conversation_history.append({
                "role": "user",
                "content": tool_context
            })

            # Get follow-up response
            yield "\n"
            messages = self._get_messages()
            follow_up_parts = []

            for chunk in self.ai_client.chat_stream(messages, temperature=0.7):
                follow_up_parts.append(chunk)
                yield chunk

            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": "".join(follow_up_parts)
            })
        else:
            # No tool calls, just add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

    def process_message_stream_interactive(self, user_message: str):
        """Process message with interactive UI (clean output with diffs)"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Stream AI response
        messages = self._get_messages()
        full_response = []

        # In DEBUG mode, show everything including JSON blocks
        if self.mode == 'DEBUG':
            for chunk in self.ai_client.chat_stream(messages, temperature=0.7):
                full_response.append(chunk)
                yield chunk
        else:
            # In SILENT mode, collect all response first then filter JSON blocks
            for chunk in self.ai_client.chat_stream(messages, temperature=0.7):
                full_response.append(chunk)

            # Remove JSON blocks from response
            response_text = "".join(full_response)

            # Remove all ```json ... ``` blocks
            cleaned_text = re.sub(r'```json\s*\{[^`]*\}\s*```', '', response_text, flags=re.DOTALL)

            # Yield the cleaned text
            if cleaned_text.strip():
                yield cleaned_text

        # Process complete response for tool calls
        assistant_message = "".join(full_response)
        text_content, tool_calls = self.response_parser.extract_tool_calls(assistant_message)

        # Execute tool calls if present (with interactive UI)
        if tool_calls and self.interactive_executor:
            yield "\n\n"

            # Use interactive executor for clean UI
            tool_results = self.interactive_executor.execute_tool_calls_interactive(tool_calls)

            # Add to conversation history
            tool_output_plain = self.response_parser.format_tool_results(tool_results)
            tool_context = f"Tool execution results:\n{tool_output_plain}"

            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            self.conversation_history.append({
                "role": "user",
                "content": tool_context
            })

            # Get follow-up response
            yield "\n"
            messages = self._get_messages()
            follow_up_parts = []

            # Stream follow-up response (with SILENT mode filtering)
            if self.mode == 'DEBUG':
                for chunk in self.ai_client.chat_stream(messages, temperature=0.7):
                    follow_up_parts.append(chunk)
                    yield chunk
            else:
                # SILENT mode - collect and filter
                for chunk in self.ai_client.chat_stream(messages, temperature=0.7):
                    follow_up_parts.append(chunk)

                # Remove JSON blocks
                follow_up_text = "".join(follow_up_parts)
                cleaned_follow_up = re.sub(r'```json\s*\{[^`]*\}\s*```', '', follow_up_text, flags=re.DOTALL)

                if cleaned_follow_up.strip():
                    yield cleaned_follow_up

            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": "".join(follow_up_parts)
            })
        else:
            # No tool calls or no interactive executor, just add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
