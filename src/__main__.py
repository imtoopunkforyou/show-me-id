import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from pydantic import BaseModel
from aiogram.enums.message_origin_type import MessageOriginType
from typing import Optional
from utils import DTOMessage
from typing import NoReturn
from src.types import OriginalMessage
from src.types import SenderUser
from config import BOT_TOKEN
from src.utils import MessageHTMLRender, CommandHTMLRender


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: OriginalMessage) -> NoReturn:
    dto: SenderUser = DTOMessage(message).create()
    rendered_template = CommandHTMLRender(dto).render()

    await message.answer(rendered_template)

    return None


@dp.message()
async def show_id(message: OriginalMessage) -> NoReturn:
    dto = DTOMessage(message=message).create()
    rendered_template = MessageHTMLRender(dto).render()

    await message.reply(rendered_template)

    return None


async def main() -> NoReturn:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

    return None


if __name__ == '__main__':
    asyncio.run(main())
