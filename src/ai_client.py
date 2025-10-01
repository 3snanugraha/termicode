"""AI Client wrapper for HuggingFace API using OpenAI SDK"""
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI


class AIClient:
    """Wrapper for AI model interaction via HuggingFace"""

    def __init__(self, model: str = "deepseek-ai/DeepSeek-V3.2-Exp"):
        self.model = model
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.environ.get("HF_TOKEN"),
        )

        if not os.environ.get("HF_TOKEN"):
            raise ValueError("HF_TOKEN environment variable is required")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Any:
        """Send chat completion request to AI model"""
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens:
            params["max_tokens"] = max_tokens

        if stream:
            params["stream"] = True
            return self.client.chat.completions.create(**params)

        completion = self.client.chat.completions.create(**params)

        if not completion.choices or len(completion.choices) == 0:
            raise ValueError("No response from AI model")

        return completion.choices[0].message

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        """Stream chat completion responses"""
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
