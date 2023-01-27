import os

from typing import Tuple
from overrides import overrides

import openai

from .message_receiver import MessageReceiver


class Bot(MessageReceiver):
    def __init__(self, name: str, initial_prompt: str, start_seq: str = "AI", restart_seq: str = "Human") -> None:
        super().__init__()

        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("The OPENAI_API_KEY environment variable is not set.")

        self._name = name
        self._initial_prompt = f"{initial_prompt}"
        self._start_seq = start_seq
        self._restart_seq = restart_seq

    @property
    def name(self) -> str:
        return self._name

    @overrides
    def receive_message(self, message: str, chat_history: Tuple[list[str], list[str]] = tuple()) -> str:
        formatted_history = self._format_chat_history(chat_history)
        return self._generate_response(formatted_history, message)

    def _format_chat_history(self, chat_history: Tuple[list[str], list[str]]) -> str:
        # If empty tuple, nothing to format.
        if not chat_history:
            return ""

        messages, responses = chat_history
        if len(messages) == 0:
            return ""

        formatted_history = []
        for i in range(len(messages)):
            formatted_history.append(f"{self._restart_seq}: {messages[i]}")
            formatted_history.append(f"{self._start_seq}: {responses[i]}")

        return "\n".join(formatted_history)

    def _generate_response(self, formatted_history: str, message: str) -> str:
        history_separator = "\n" if formatted_history else ""
        formatted_message = f"{self._initial_prompt}\n\n \
                                   {formatted_history}{history_separator} \
                                   {self._restart_seq}: {message}\n"

        # Request a response from the OpenAI API.
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=formatted_message,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[f"\n{self._restart_seq}", f"\n{self._start_seq}"]
        )

        # Get the response text.
        choices = response["choices"]
        response_text = choices[0].get("text").strip()

        # Remove possible bot name followed by colon and stop sequences.
        response_text = self._remove_prefix(response_text, f"{self._name}:")
        response_text = self._remove_prefix(response_text, f"{self._start_seq}:")
        response_text = self._remove_prefix(response_text, f"{self._restart_seq}:")
        return response_text

    def _remove_prefix(self, text: str, prefix: str) -> str:
        tokens = text.split(prefix, maxsplit=1)
        return tokens[1].strip() if len(tokens) > 1 else tokens[0]
