from telegram import Bot

from faststream import Context
from faststream.kafka import KafkaRouter

from consumers.schemas import (
    NewChatMessageSchema,
    NewChatSchema,
)
from containers.factories import get_container
from services.web import BaseChatWebService
from settings import get_settings


settings = get_settings()
router = KafkaRouter()


@router.subscriber(settings.NEW_CHAT_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def new_chat_handler(message: NewChatSchema):
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        chat = await bot.get_chat(chat_id=settings.TELEGRAM_GROUP_ID)
        chat_title = f"{message.chat_title} | {message.chat_oid}"
        await chat.create_forum_topic(name=chat_title)


@router.subscriber(settings.NEW_MESSAGE_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def new_message_subscription_handler(
    message: NewChatMessageSchema,
    key: bytes = Context("message.raw_message.key"),
):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)  # type: ignore
        listeners = await service.get_chat_listeners(chat_oid=key.decode())
        chat_info = await service.get_chat_info(chat_oid=key.decode())

        bot = await request_container.get(Bot)

        for listener in listeners:
            await bot.send_message(
                chat_id=listener.oid,
                text=(
                    f'New message from chat (<code>{chat_info.oid}</code>) <b>{chat_info.title}</b> '
                    f'<blockquote>{message.message_text}</blockquote>'
                ),
                parse_mode='HTML',
            )
