from jinja2 import Environment, PackageLoader, select_autoescape

BOT_TOKEN: str = ...
RENDER_ENVIROMENT: Environment = Environment(
    loader=PackageLoader('src'),
    autoescape=select_autoescape(('html', ))
)
