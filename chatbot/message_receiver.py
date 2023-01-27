from typing import Tuple
from abc import ABC, abstractmethod

class MessageReceiver(ABC):
    @abstractmethod
    def receive_message(self, message: str, chat_history: Tuple[list[str], list[str]] = tuple()) -> str:
        pass
