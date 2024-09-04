from typing import Union

from aiogram.enums.message_origin_type import MessageOriginType

from exceptions.exceptions import MessageDefinitionError
from dto.entity.public import AbstractPublicEntity, Channel, Chat
from dto.entity.user import (
    AbstractUser,
    ForwardUser,
    HiddenUser,
    SenderUser,
)
from dto.original import OriginalMessage, OriginalUser


class BaseTelegramMessage():
    """
    Base telegram message.

    Describes the general properties of a telegram message.
    """

    def __init__(self, message: OriginalMessage):
        self.message = message

    def is_forward_user(self) -> bool:
        """
        Checking if a message is a message from a user.

        It is assumed that the message has been forwarded.

        :return: True if `self.message` is a message from a user.
                 Otherwise False.
        :rtype: bool
        """
        if self._is_forward():
            return (
                self.message.forward_origin.type
                == MessageOriginType.USER.value
            )

        return False

    def is_hidden_user(self) -> bool:
        """
        Checking if the user profile is hidden (privacy settings).

        It is assumed that the message has been forwarded.

        :return: True if the user profile is hidden.
                 Otherwise False.
        :rtype: bool
        """
        if self._is_forward():
            return (
                self.message.forward_origin.type
                == MessageOriginType.HIDDEN_USER.value
            )

        return False

    def is_chat(self) -> bool:
        """
        Checking if the message was received from a chat.

        It is assumed that the message has been forwarded.

        :return: True if the `self.message` was received from a chat.
                 Otherwise False.
        :rtype: bool
        """
        if self._is_forward():
            return (
                self.message.forward_origin.type
                == MessageOriginType.CHAT.value
            )

        return False

    def is_channel(self) -> bool:
        """
        Checking if the message was received from a channel.

        It is assumed that the message has been forwarded.

        :return: True if the `self.message` was received from a channel.
                 Otherwise False.
        :rtype: bool
        """
        if self._is_forward():
            return (
                self.message.forward_origin.type
                == MessageOriginType.CHANNEL.value
            )

        return False

    def is_sender_user(self) -> bool:
        """
        Checking that the message was sent by the author.

        :return: True if the `self.message` was sent by the author.
                 Otherwise False.
        :rtype: bool
        """
        if not self._is_forward() and self.message.from_user:
            return isinstance(self.message.from_user, OriginalUser)

        return False

    def _is_forward(self) -> bool:
        """
        Shows whether a message belongs to its author.

        :return: True if `self.message` does not belong to the author.
                 Otherwise False.
        :rtype: bool
        """
        return bool(self.message.forward_origin)


class TelegramMessage(BaseTelegramMessage):
    """
    Telegram message.

    Provides the message object in the required form (_attrs of class).

    :param BaseTelegramMessage: Base telegram message.
    :type BaseTelegramMessage: dto.base.BaseTelegramMessage
    """

    _sender_user: SenderUser = SenderUser
    _channel: Channel = Channel
    _chat: Chat = Chat
    _hidden_user: HiddenUser = HiddenUser
    _forward_user: ForwardUser = ForwardUser

    def __init__(self, message: OriginalMessage):
        super().__init__(message=message)
        self._dto: Union[AbstractPublicEntity, AbstractUser, None] = ...

    @property
    def dto(self) -> Union[AbstractPublicEntity, AbstractUser, None]:
        """
        Telegram message in the required format.

        :raises MessageDefinitionError: Data Transport Object
                                        was not determined.

        :return: Data Transport Object.
        :rtype: Union[AbstractPublicEntity, AbstractUser, None]
        """
        self._dto: Union[
            AbstractPublicEntity,
            AbstractUser,
            None,
        ] = self._create_dto_object()

        if not self._dto:
            raise MessageDefinitionError

        return self._dto

    def _create_dto_object(
        self,
    ) -> Union[AbstractPublicEntity, AbstractUser, None]:
        dto = None
        original_forward_message = self.message.forward_origin
        original_user = self.message.from_user

        if self.is_forward_user():
            dto: ForwardUser = self._forward_user(
                id=original_forward_message.sender_user.id,
                is_bot=original_forward_message.sender_user.is_bot,
                first_name=original_forward_message.sender_user.first_name,
                last_name=original_forward_message.sender_user.last_name,
                username=original_forward_message.sender_user.username,
                is_premium=original_forward_message.sender_user.is_premium,
            )

        if self.is_hidden_user():
            dto: HiddenUser = self._hidden_user(
                first_name=original_forward_message.sender_user_name,
            )

        if self.is_chat():
            dto: Chat = self._chat(
                id=original_forward_message.sender_chat.id,
                title=original_forward_message.sender_chat.title,
            )

        if self.is_channel():
            dto: Channel = self._channel(
                id=original_forward_message.chat.id,
                title=original_forward_message.chat.title,
            )

        if self.is_sender_user():
            dto: SenderUser = self._sender_user(
                id=original_user.id,
                is_bot=original_user.is_bot,
                first_name=original_user.first_name,
                last_name=original_user.last_name,
                username=original_user.username,
                is_premium=original_user.is_premium,
            )

        return dto
