"""Context manager to handle conversation history with token limits"""
from typing import List, Dict, Any


class ContextManager:
    """Manage conversation context with token limits and summarization"""

    def __init__(self, max_messages: int = 20, max_tokens_estimate: int = 8000):
        """
        Initialize context manager

        Args:
            max_messages: Maximum number of messages to keep in history
            max_tokens_estimate: Rough estimate of max tokens (4 chars ≈ 1 token)
        """
        self.max_messages = max_messages
        self.max_tokens_estimate = max_tokens_estimate

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation: 4 chars ≈ 1 token)"""
        return len(text) // 4

    def get_total_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Calculate total tokens in message history"""
        total = 0
        for msg in messages:
            total += self.estimate_tokens(msg.get('content', ''))
        return total

    def truncate_history(
        self,
        history: List[Dict[str, str]],
        system_prompt: str = ""
    ) -> List[Dict[str, str]]:
        """
        Truncate history to fit within token limits

        Strategy:
        1. Keep most recent messages
        2. Keep first message if it contains important context
        3. Remove middle messages if needed
        """
        if not history:
            return history

        # Calculate system prompt tokens
        system_tokens = self.estimate_tokens(system_prompt)

        # Check if we're within limits
        total_tokens = self.get_total_tokens(history)

        if total_tokens + system_tokens <= self.max_tokens_estimate and len(history) <= self.max_messages:
            return history

        # Strategy: Keep recent messages
        truncated = []
        tokens_used = system_tokens

        # Start from most recent and work backwards
        for message in reversed(history):
            msg_tokens = self.estimate_tokens(message.get('content', ''))

            if tokens_used + msg_tokens > self.max_tokens_estimate:
                break

            if len(truncated) >= self.max_messages:
                break

            truncated.insert(0, message)
            tokens_used += msg_tokens

        return truncated

    def sliding_window(
        self,
        history: List[Dict[str, str]],
        window_size: int = 10
    ) -> List[Dict[str, str]]:
        """
        Keep only last N message pairs (user + assistant)

        Args:
            history: Full conversation history
            window_size: Number of recent message pairs to keep
        """
        if len(history) <= window_size * 2:
            return history

        # Keep last N pairs
        return history[-(window_size * 2):]

    def compress_history(
        self,
        history: List[Dict[str, str]],
        keep_recent: int = 4
    ) -> List[Dict[str, str]]:
        """
        Compress history by keeping first and last messages, summarizing middle

        Args:
            history: Full conversation history
            keep_recent: Number of recent messages to keep in full
        """
        if len(history) <= keep_recent + 2:
            return history

        # Keep first message (often contains initial context)
        first_messages = history[:2]  # First user message + response

        # Keep recent messages
        recent_messages = history[-keep_recent:]

        # Create summary of middle messages
        middle_count = len(history) - keep_recent - 2
        summary = {
            "role": "system",
            "content": f"[{middle_count} previous messages summarized for context]"
        }

        return first_messages + [summary] + recent_messages

    def get_context_stats(self, history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Get statistics about current context"""
        total_tokens = self.get_total_tokens(history)
        user_messages = len([m for m in history if m.get('role') == 'user'])
        assistant_messages = len([m for m in history if m.get('role') == 'assistant'])

        return {
            'total_messages': len(history),
            'user_messages': user_messages,
            'assistant_messages': assistant_messages,
            'estimated_tokens': total_tokens,
            'tokens_remaining': self.max_tokens_estimate - total_tokens,
            'usage_percentage': (total_tokens / self.max_tokens_estimate) * 100
        }
