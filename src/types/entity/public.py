
from pydantic import BaseModel
from abc import ABC


class AbstractPublicEntity(BaseModel, ABC):
    id: int
    title: str


class Chat(AbstractPublicEntity):
    pass


class Channel(AbstractPublicEntity):
    pass
