from telegram import (
    Update,
    Bot,
)
from telegram.ext import ContextTypes

from containers.factories import get_container
from handlers.converters.chats import convert_chats_dtos_to_message
from services.web import BaseChatWebService


async def get_tread_name(bot: Bot, chat_id: int, message_thread_id: int) -> str:
    # TODO: refactor this
    chat = await bot.get_chat(chat_id=chat_id)
    message = await chat.get_messages(message_thread_id=message_thread_id)
    return message.text


async def get_all_chats_handlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)  # type: ignore
        chats = await service.get_all_chats()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,  # type: ignore
        text=convert_chats_dtos_to_message(chats=chats),
        parse_mode='HTML',
    )


async def set_chat_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)  # type: ignore

        await service.add_listener(
            telegram_chat_id=update.effective_chat.id,
            chat_oid=context.args[0],
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text='Listener added to the chat',
            parse_mode='HTML',
        )


async def quit_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,  # type: ignore
        text='Chat has been closed.',
        parse_mode='HTML',
    )


async def send_message_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="It is necessary to respond specifically to the user's message.",
        message_thread_id=update.message.message_thread_id,
    )
    try:
        ...
    except IndexError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text="It is necessary to respond specifically to the user's message.",
            parse_mode='HTML',
        )

        return
