from telegram import Update
from telegram.ext import CallbackContext

from exceptions.base import ApplicationException
from exceptions.chats import BaseWebException


async def send_error_message(update: Update, message: str) -> None:
    await update.effective_message.reply_text(message)  # type: ignore


async def error_handler(update: Update, context: CallbackContext) -> None:
    try:
        raise context.error  # type: ignore

    except BaseWebException as error:
        error_message = '\n'.join((error.message, error.error_text))
        await send_error_message(update, error_message)

    except ApplicationException as error:
        print(error.meta)
        await send_error_message(update, error.message)
