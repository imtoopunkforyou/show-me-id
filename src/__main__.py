import asyncio
from typing import NoReturn

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart

from config import BOT_PROPERTIES, BOT_TOKEN
from dto.message import TelegramMessage
from render.render import CommandHTMLRender, MessageHTMLRender
from dto.entity.user import SenderUser
from dto.original import OriginalMessage

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: OriginalMessage) -> NoReturn:
    """
    Command handler `/start`.

    Send a greeting message to the user.

    :param message: message from user.
    :type message: OriginalMessage
    """
    dto: SenderUser = TelegramMessage(message).dto
    rendered_template = CommandHTMLRender(dto).execute()

    await message.answer(rendered_template)


@dp.message()
async def show_id(message: OriginalMessage) -> NoReturn:
    """
    Handler for all incoming messages.

    Provides the user or entity ID in response to the message.

    :param message: message from user
    :type message: OriginalMessage
    """
    dto = TelegramMessage(message).dto
    rendered_template = MessageHTMLRender(dto).execute()

    await message.reply(rendered_template)


async def main() -> NoReturn:
    """Entry point to the application."""
    bot = Bot(
        token=BOT_TOKEN,
        default=BOT_PROPERTIES,
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
