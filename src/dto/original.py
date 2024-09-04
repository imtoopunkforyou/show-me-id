"""Original aiogram types."""

from typing import Union

from aiogram.types import Message
from aiogram.types.message_origin_channel import MessageOriginChannel
from aiogram.types.message_origin_chat import MessageOriginChat
from aiogram.types.message_origin_hidden_user import MessageOriginHiddenUser
from aiogram.types.message_origin_user import MessageOriginUser
from aiogram.types.user import User

OriginalMessage = Message
OriginalUser = User
OriginalForwardMessage = Union[
    MessageOriginUser,
    MessageOriginHiddenUser,
    MessageOriginChat,
    MessageOriginChannel,
]
