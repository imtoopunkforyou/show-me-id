from pydantic import BaseModel, field_validator
from abc import ABC
from typing import Optional, Union


class AbstractUser(BaseModel, ABC):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_premium: Optional[bool] = None
    is_bot: bool = False

    @property
    def at_sign_username(self) -> str:
        if self.username:
            at_sign = '@'
            return (at_sign + self.username).lower()

        return self.username

    @property
    def full_name(self) -> str:
        if hasattr(self, 'last_name'):
            if self.last_name is not None:
                return f'{self.first_name} {self.last_name}'

        return self.first_name

    @field_validator('is_premium')
    def _none_to_false(cls, value: Union[bool, None]) -> bool:
        return False if value is None else value


class HiddenUser(AbstractUser):
    pass


class SenderUser(AbstractUser):
    pass


class ForwardUser(AbstractUser):
    pass
