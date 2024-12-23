from dataclasses import dataclass
import json

from exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class BaseWebException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def response_json(self) -> dict:
        return json.loads(self.response_content)

    @property
    def error_text(self) -> str:
        return self.response_json.get('detail', {}).get('error', '')


@dataclass(frozen=True, eq=False)
class ChatListRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return "Couldn't get a list of all chats."


@dataclass(frozen=True, eq=False)
class ListenerListRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return "Couldn't get a list of chat listeners."


@dataclass(frozen=True, eq=False)
class ListenerAddRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return "Couldn't add chat listener to the chat."


@dataclass(frozen=True, eq=False)
class ChatAlreadyExistsError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return "Chat with this data already exists."


@dataclass(frozen=True, eq=False)
class ChatInfoNotFoundError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return "Couldn't find information about the chat."


@dataclass(frozen=True, eq=False)
class ChatNotFoundByTelegramIdError(ApplicationException):
    telegram_chat_id: str

    @property
    def message(self) -> str:
        return "Couldn't find chat by telegram chat id."


@dataclass(frozen=True, eq=False)
class ChatNotFoundByWebIdError(ApplicationException):
    web_chat_id: str

    @property
    def message(self) -> str:
        return "Couldn't find chat by web chat id."


@dataclass(frozen=True, eq=False)
class ChatInfoRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return "Couldn't get a information about the chat."


@dataclass(frozen=True, eq=False)
class SendMessageToChatError(ApplicationException):
    @property
    def message(self) -> str:
        return "Couldn't send message to the chat."
