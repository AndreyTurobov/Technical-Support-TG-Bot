from functools import lru_cache
import environ

from pydantic_settings import BaseSettings


env = environ.Env()
environ.Env.read_env('.env')


class ProjectSettings(BaseSettings):
    TG_BOT_TOKEN: str = env('TG_BOT_TOKEN')
    START_MESSAGE: str = env(
        'START_MESSAGE',
        default=(
            'Welcome to techsupport bot.\n'
            'Please choose a chat for client support.\nGet all available chats: ' 
            '/chats, choose a chat: /set_chats <chat_oid>'
        ),
    )
    WEB_API_BASE_URL: str = env('WEB_API_BASE_URL', default='http://localhost:8000')


@lru_cache(1)
def get_settings() -> ProjectSettings:
    return ProjectSettings()
