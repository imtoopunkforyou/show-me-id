from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from jinja2 import Environment, PackageLoader, select_autoescape

BOT_TOKEN: str = ''
BOT_PROPERTIES = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
)

RENDER_ENVIROMENT: Environment = Environment(
    loader=PackageLoader('smid'),
    autoescape=select_autoescape(
        (
            'html',
        ),
    ),
)
