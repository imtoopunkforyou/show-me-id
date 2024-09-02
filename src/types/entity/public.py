from abc import ABC

from pydantic import BaseModel


class AbstractPublicEntity(BaseModel, ABC):
    """
    Some public telegram entity (like chat, channel, etc).

    :param BaseModel: A base class for creating Pydantic models.
    :type BaseModel: pydantic._internal._model_construction.ModelMetaclass

    :param ABC: Helper class that provides a standard way to
                create an ABC using inheritance.
    :type ABC: abc.ABCMeta
    """

    id: int
    title: str


class Chat(AbstractPublicEntity):
    """
    Telegram chat.

    :param AbstractPublicEntity: Public telegram entity.
    :type AbstractPublicEntity: ModelMetaclass
    """


class Channel(AbstractPublicEntity):
    """
    Telegram channel.

    :param AbstractPublicEntity: Public telegram entity.
    :type AbstractPublicEntity: ModelMetaclass.
    """
