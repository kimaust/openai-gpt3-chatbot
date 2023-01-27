from typing import Tuple

from .message_receiver import MessageReceiver


class User:
    def __init__(self, name: str = "You", max_message_count: int = 5) -> None:
        super().__init__()

        self._name = name
        self._messages = []
        self._responses = []

        # The maximum number of latest messages to keep track of to provide a context during conversation.
        self._max_message_count = max_message_count
        if self._max_message_count < 0:
            raise ValueError("The maximum message count must be greater than or equal to 0.")

    @property
    def name(self) -> str:
        return self._name

    def send_message(self, recipient: MessageReceiver, message: str) -> str:
        # Store up to max count specified for this user.
        if len(self._messages) > self._max_message_count:
            self._messages.pop(0)
            self._responses.pop(0)

        response = recipient.receive_message(message, self._get_chat_history())
        self._messages.append(message)
        self._responses.append(response)

        return response

    def _get_chat_history(self) -> Tuple[list[str], list[str]]:
        if len(self._messages) == 0:
            return tuple()

        return self._messages, self._responses
