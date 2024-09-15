from abc import ABC
from typing import Optional, Self, Union

from pydantic import BaseModel, field_validator


class AbstractUser(BaseModel, ABC):
    """
    Telegram user.

    :param BaseModel: A base class for creating Pydantic models.
    :type BaseModel: pydantic._internal._model_construction.ModelMetaclass.

    :param ABC: Helper class that provides a
                standard way to create an ABC using
                inheritance.
    :type ABC: abc.ABCMeta.
    """

    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_premium: Optional[bool] = None
    is_bot: bool = False

    @property
    def at_sign_username(self: Self) -> Union[str, None]:
        """Username format like `@username`."""
        if self.username:
            at_sign = '@'
            return (at_sign + self.username).lower()

        return self.username

    @property
    def full_name(self) -> str:
        """User full name."""
        if self.last_name is not None:
            return '{first_name} {last_name}'.format(
                first_name=self.first_name,
                last_name=self.last_name,
            )

        return self.first_name

    @field_validator('is_premium')
    @classmethod
    def _none_to_false(cls, premium_value: Union[bool, None]) -> bool:
        return False if premium_value is None else premium_value


class SenderUser(AbstractUser):
    """
    The one who sent the message.

    :param AbstractUser: Telegram user.
    :type AbstractUser: pydantic._internal._model_construction.ModelMetaclass.
    """


class ForwardUser(AbstractUser):
    """
    The one whose message was forwarded.

    :param AbstractUser: Telegram user.
    :type AbstractUser: pydantic._internal._model_construction.ModelMetaclass.
    """
