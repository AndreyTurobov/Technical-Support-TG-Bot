from functools import lru_cache
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class ProjectSettings(BaseSettings):
    TG_BOT_TOKEN: str
    START_MESSAGE: str = (
        'Welcome to techsupport bot.\n'
        'Please choose a chat for client support.\nGet all available chats: ' 
        '/chats, choose a chat: /listen_chat <chat_oid>'
    )
    WEB_API_BASE_URL: str = 'http://main-app:8000'
    KAFKA_BROKER_URL: str = 'kafka:29092'
    NEW_MESSAGE_TOPIC: str = 'new-messages'
    NEW_CHAT_TOPIC: str = 'new-chats-topic'
    DELETE_CHAT_TOPIC: str = 'chat-deleted'
    KAFKA_GROUP_ID: str = 'tg-bot'
    DATABASE_NAME: str = 'app/tg-bot.db'
    TELEGRAM_GROUP_ID: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache(1)
def get_settings() -> ProjectSettings:
    return ProjectSettings()
