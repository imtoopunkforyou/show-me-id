from abc import ABC, abstractmethod
from typing import Optional, Union

from config import RENDER_ENVIROMENT
from dto.entity.public import AbstractPublicEntity
from dto.entity.user import AbstractUser
from jinja2 import Environment
from jinja2.environment import Template
from render.exceptions import RenderDTOError
from render.types import FileNameLikeStr, HTMLikeStr, TemplateMessageKwargs


class AbstractHTMLRender(ABC):
    """Converts DTO object to html message."""

    def __init__(self, dto: Union[AbstractPublicEntity, AbstractUser]):
        self.dto = dto
        self.enviroment: Environment = RENDER_ENVIROMENT

    @abstractmethod
    def execute(self) -> HTMLikeStr:
        """
        Converts DTO to html message.

        :return: html message.
        :rtype: HTMLikeStr
        """

    @property
    def is_user(self) -> bool:
        """
        Is DTO a user or not.

        :return: `True` if dto a user. Otherwise `False`.
        :rtype: bool
        """
        return isinstance(self.dto, AbstractUser)

    def _get_filename(self, filename: str) -> FileNameLikeStr:
        file_extension = '.html'

        return filename + file_extension

    def _get_template_obj(self, filename: str) -> Template:
        filename = self._get_filename(filename)

        return self.enviroment.get_template(filename)


class MessageHTMLRender(AbstractHTMLRender):
    """
    Converts DTO object to html message.

    Works with messages from the user (but not with commands).

    :param AbstractHTMLRender: Abstract render.
    :type AbstractHTMLRender: abc.ABC

    :raises RenderDTOError: Failed to create template object.
    """

    user_template_filename: str = 'user'
    public_entity_template_filename: str = 'public_entity'

    def __init__(self, dto: Union[AbstractUser, AbstractPublicEntity]):
        super().__init__(dto=dto)

    def execute(self) -> HTMLikeStr:
        """
        Converts DTO to html message.

        :raises RenderDTOError: Failed to create template object.

        :return: html message.
        :rtype: HTMLikeStr
        """
        template: Optional[Template] = None
        template_kwargs: Optional[TemplateMessageKwargs] = None

        if self.is_user:
            template = self._get_template_obj(self.user_template_filename)
            template_kwargs = {
                'id': self.dto.id,
                'name': self.dto.full_name,  # type: ignore [union-attr]
                'username': self.dto.at_sign_username,  # type: ignore
                'is_premium': self.dto.is_premium,  # type: ignore [union-attr]
            }
        elif self.is_public_entity:
            template = self._get_template_obj(
                self.public_entity_template_filename,
            )
            template_kwargs = {
                'id': self.dto.id,
                'title': self.dto.title,  # type: ignore [union-attr]
            }

        if not template or not template_kwargs:
            raise RenderDTOError

        return template.render(**template_kwargs)

    @property
    def is_public_entity(self) -> bool:
        """
        Is DTO a public entity or not.

        :return: `True` if DTO a public entity.
                 Otherwise `False`.
        :rtype: bool
        """
        return isinstance(self.dto, AbstractPublicEntity)


class CommandHTMLRender(AbstractHTMLRender):
    """
    Converts DTO object to html message.

    Works with commands from the user (but not with messages).

    :param AbstractHTMLRender: Abstract render.
    :type AbstractHTMLRender: abc.ABC

    :raises RenderDTOError: Failed to create template object.
    """

    start_template_filename: str = 'start'

    def __init__(
        self,
        dto: Union[AbstractPublicEntity, AbstractUser],
    ):
        super().__init__(dto=dto)

    def execute(self) -> HTMLikeStr:
        """
        Converts DTO to html message.

        :raises RenderDTOError: Failed to create template object.

        :return: html message.
        :rtype: HTMLikeStr
        """
        template: Optional[Template] = None
        template_kwargs: Optional[TemplateMessageKwargs] = None

        if self.is_user:
            template = self._get_template_obj(self.start_template_filename)
            template_kwargs = {
                'full_name': self.dto.full_name,  # type: ignore [union-attr]
            }

        if not template or not template_kwargs:
            raise RenderDTOError

        return template.render(**template_kwargs)
