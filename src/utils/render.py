from src import config
from src.types import SenderUser, Channel, Chat, HiddenUser, ForwardUser, AbstractPublicEntity, AbstractUser, FileNameLikeStr, HTMLikeStr
from typing import Union
from src.config import RENDER_ENVIROMENT
from jinja2 import Environment
from abc import ABC, abstractmethod
from jinja2.environment import Template
from src.exceptions import RenderDTOError


class AbstractHTMLRender(ABC):
    def __init__(self, dto: Union[AbstractPublicEntity, AbstractUser]):
        self.dto = dto
        self.enviroment: Environment = RENDER_ENVIROMENT

    def __get_filename(self, filename: str) -> FileNameLikeStr:
        file_extension = '.html'

        return filename + file_extension

    def _get_template(self, filename: str) -> Template:
        filename = self.__get_filename(filename)

        return self.enviroment.get_template(filename)

    @abstractmethod
    def render(self) -> HTMLikeStr:
        ...

    @property
    def is_user(self) -> bool:
        return isinstance(self.dto, AbstractUser)


class MessageHTMLRender(AbstractHTMLRender):
    _user: str = 'user'
    _public_entity: str = 'public_entity'

    def __init__(self, dto: Union[AbstractUser, AbstractPublicEntity]):
        super().__init__(dto=dto)

    def render(self) -> HTMLikeStr:
        template: Template = None
        template_kwargs: dict[str, Union[str, int, bool]] = None

        if self.is_user:
            template = self._get_template(self._user)
            template_kwargs = dict(
                id=self.dto.id,
                name=self.dto.full_name,
                username=self.dto.at_sign_username,
                is_premium=self.dto.is_premium,
            )
        elif self.is_public_entity:
            template = self._get_template(self._public_entity)
            template_kwargs = dict(
                id=self.dto.id,
                title=self.dto.title,
            )

        if not template or not template:
            raise RenderDTOError

        return template.render(**template_kwargs)

    @property
    def is_public_entity(self) -> bool:
        return isinstance(self.dto, AbstractPublicEntity)


class CommandHTMLRender(AbstractHTMLRender):
    _start: str = 'start'

    def __init__(self, dto: SenderUser):
        super().__init__(dto=dto)

    def render(self) -> HTMLikeStr:
        template: Template = None
        template_kwargs: dict[str, Union[str, int, bool]] = None

        if self.is_user:
            template = self._get_template(self._start)
            template_kwargs = dict(
                full_name=self.dto.full_name,
            )

        if not template or not template:
            raise RenderDTOError

        return template.render(**template_kwargs)
