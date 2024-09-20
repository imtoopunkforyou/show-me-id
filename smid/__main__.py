import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from config import BOT_PROPERTIES, BOT_TOKEN, LOGS_ENABLE
from dto.message import TelegramMessage
from dto.original import OriginalMessage
from render.render import CommandHTMLRender, MessageHTMLRender

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: OriginalMessage) -> None:
    """
    Command handler `/start`.

    Send a greeting message to the user.

    :param message: message from user.
    :type message: OriginalMessage
    """
    msg = TelegramMessage(message)
    rendered_template = CommandHTMLRender(msg.dto).execute()

    await message.answer(rendered_template)


@dp.message()
async def show_id(message: OriginalMessage) -> None:
    """
    Handler for all incoming messages.

    Provides the user or entity ID in response to the message.

    :param message: message from user
    :type message: OriginalMessage
    """
    msg = TelegramMessage(message)
    rendered_template = MessageHTMLRender(msg.dto).execute()

    await message.reply(rendered_template)


async def main() -> None:
    """Entry point to the application."""
    bot = Bot(
        token=BOT_TOKEN,
        default=BOT_PROPERTIES,
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    if LOGS_ENABLE:
        logging.basicConfig(
            level=logging.INFO,
            stream=sys.stdout,
        )

    asyncio.run(main())
