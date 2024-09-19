import os
from pathlib import Path, PosixPath
from typing import cast

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR: PosixPath = cast(PosixPath, Path(__file__).resolve().parent)
TEMPLATES_DIR: str = '{base_dir}/templates/'.format(
    base_dir=BASE_DIR,
)

BOT_TOKEN: str = cast(str, os.getenv('BOT_TOKEN'))
BOT_PROPERTIES: DefaultBotProperties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
)

RENDER_ENVIROMENT: Environment = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(
        (
            'html',
        ),
    ),
)
