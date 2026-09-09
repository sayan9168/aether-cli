"""Chat engine with tool calling support."""

from __future__ import annotations

import json
from typing import Any, Generator

from litellm import completion

from aether.config import Settings
from aether.tools import execute_tool, get_tools_schema
from aether.ui import print_error, print_info


class ChatEngine:
    """Handles conversation with the LLM including tool use."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.messages: list[dict[str, Any]] = [
            {"role": "system", "content": settings.system_prompt}
        ]
        self.model = settings.model

    def clear_history(self) -> None:
        self.messages = [{"role": "system", "content": self.settings.system_prompt}]

    def set_model(self, model: str) -> None:
        self.model = model.strip()

    def chat(self, user_input: str) -> str:
        """Send a user message and return the final assistant response."""
        self.messages.append({"role": "user", "content": user_input})

        max_tool_rounds = 8
        for _ in range(max_tool_rounds):
            try:
                response = completion(
                    model=self.model,
                    messages=self.messages,
                    tools=get_tools_schema(),
                    tool_choice="auto",
                    max_tokens=self.settings.max_tokens,
                    temperature=self.settings.temperature,
                    stream=False,
                )
            except Exception as e:
                print_error(f"LLM error: {e}")
                # Remove the last user message so they can retry cleanly
                if self.messages and self.messages[-1].get("role") == "user":
                    self.messages.pop()
                return f"Error communicating with the model: {e}"

            message = response.choices[0].message
            tool_calls = getattr(message, "tool_calls", None) or []

            msg_dict: dict[str, Any] = {
                "role": "assistant",
                "content": message.content or "",
            }
            if tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments or "{}",
                        },
                    }
                    for tc in tool_calls
                ]

            self.messages.append(msg_dict)

            if not tool_calls:
                return message.content or "(empty response)"

            for tc in tool_calls:
                name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}

                print_info(f"Running tool: {name}({args})")
                result = execute_tool(name, args)

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": name,
                        "content": str(result)[:50_000],
                    }
                )

        return "Reached maximum tool call rounds. Stopping."

    def stream_chat(self, user_input: str) -> Generator[str, None, None]:
        """Stream a simple response (no tools)."""
        self.messages.append({"role": "user", "content": user_input})

        try:
            response = completion(
                model=self.model,
                messages=self.messages,
                max_tokens=self.settings.max_tokens,
                temperature=self.settings.temperature,
                stream=True,
            )

            full_content = ""
            for chunk in response:
                delta = chunk.choices[0].delta
                if delta and getattr(delta, "content", None):
                    full_content += delta.content
                    yield delta.content

            self.messages.append({"role": "assistant", "content": full_content})

        except Exception as e:
            print_error(f"Streaming error: {e}")
            yield f"\n[Error: {e}]"
