from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from sqlite3 import Row

from aiosqlite.core import connect

from dtos.messages import ChatInfoDTO
from exceptions.chats import ChatInfoNotFoundError
from repositories.sqls import (
    ADD_NEW_CHAT_INFO,
    GET_CHATS_COUNT,
    GET_CHAT_INFO_BY_EXTERNAL_ID,
    GET_CHAT_INFO_BY_TELEGRAM_ID,
)


class BaseChatsRepository(ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_chat_id: str) -> ChatInfoDTO:
        ...

    @abstractmethod
    async def get_by_external_id(self, web_chat_id: str) -> ChatInfoDTO:
        ...

    @abstractmethod
    async def check_chat_exists(
            self,
            web_chat_id: str | None,
            telegram_chat_id: str | None,
    ) -> bool:
        ...

    @abstractmethod
    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        ...


@dataclass(eq=False)
class SQLChatsRepository(BaseChatsRepository):
    database_url: str

    async def _execute_query(self, query: str, params: tuple) -> Row | None:
        async with connect(self.database_url) as connection:
            cursor = await connection.cursor()
            await cursor.execute(query, params)
            result = await cursor.fetchone()
        return result

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        async with connect(self.database_url) as connection:
            cursor = await connection.cursor()
            await cursor.execute(
                ADD_NEW_CHAT_INFO,
                (chat_info.external_id, chat_info.telegram_id),
            )
            await connection.commit()
        return chat_info

    async def get_by_telegram_id(self, telegram_chat_id: str) -> ChatInfoDTO:
        result = await self._execute_query(
            GET_CHAT_INFO_BY_TELEGRAM_ID,
            (telegram_chat_id,),
        )
        if result is None:
            raise ChatInfoNotFoundError(
                telegram_chat_id=telegram_chat_id,
            )
        return ChatInfoDTO(
            telegram_chat_id=result[0],
            web_chat_id=result[1],
        )

    async def get_by_external_id(self, web_chat_id: str) -> ChatInfoDTO:
        result = await self._execute_query(
            GET_CHAT_INFO_BY_EXTERNAL_ID,
            (web_chat_id,),
        )
        if result is None:
            raise ChatInfoNotFoundError(
                web_chat_id=web_chat_id,
            )
        return ChatInfoDTO(
            telegram_chat_id=result[0],
            web_chat_id=result[1],
        )

    async def check_chat_exists(
            self,
            web_chat_id: str | None,
            telegram_chat_id: str | None,
    ) -> bool:
        result = await self._execute_query(
            GET_CHATS_COUNT,
            (web_chat_id, telegram_chat_id),
        )
        return result is not None
