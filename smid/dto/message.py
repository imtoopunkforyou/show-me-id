from typing import Type, Union

from aiogram.enums.message_origin_type import MessageOriginType
from dto.entity.public import AbstractPublicEntity, Channel, Chat
from dto.entity.user import AbstractUser, ForwardUser, SenderUser
from dto.original import OriginalChat, OriginalMessage, OriginalUser
from exceptions.exceptions import MessageDefinitionError


class BaseTelegramMessage():
    """
    Base telegram message.

    Describes the general properties of a telegram message.
    """

    def __init__(
        self,
        message: OriginalMessage,
    ):
        self.message = message

    def is_forward_user(self) -> bool:
        """
        Checking if a message is a message from a user.

        It is assumed that the message has been forwarded.

        :return: True if `self.message` is a message from a user.
                 Otherwise False.
        :rtype: bool
        """
        if self.message.forward_origin:
            return (
                self.message.forward_origin.type
                == MessageOriginType.USER.value
            )

        return False

    def is_hidden_user(self) -> bool:
        """
        Checking if the user profile is hidden (privacy settings).

        It is assumed that the message has been forwarded.
        No user information will be provided.

        :return: True if the user profile is hidden.
                 Otherwise False.
        :rtype: bool
        """
        if self.message.forward_origin:
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
        if self.message.forward_origin:
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
        if self.message.forward_origin:
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
        if not self.message.forward_origin and self.message.from_user:
            return isinstance(self.message.from_user, OriginalUser)

        return False


class TelegramMessage(BaseTelegramMessage):
    """
    Telegram message.

    Provides the message object in the required form (_attrs of class).

    :param BaseTelegramMessage: Base telegram message.
    :type BaseTelegramMessage: dto.base.BaseTelegramMessage
    """

    _sender_user: Type[SenderUser] = SenderUser
    _channel: Type[Channel] = Channel
    _chat: Type[Chat] = Chat
    _forward_user: Type[ForwardUser] = ForwardUser

    def __init__(self, message: OriginalMessage):
        super().__init__(message=message)

    @property
    def dto(self) -> Union[AbstractPublicEntity, AbstractUser]:
        """
        Telegram message in the required format.

        :raises MessageDefinitionError: Data Transport Object
                                        was not determined.

        :return: Data Transport Object.
        :rtype: Union[AbstractPublicEntity, AbstractUser, None]
        """
        self._dto: Union[AbstractPublicEntity, AbstractUser, None] = self._create_dto_object()

        if not self._dto:
            raise MessageDefinitionError

        return self._dto

    def _create_dto_object(
        self,
    ) -> Union[AbstractPublicEntity, AbstractUser, None]:
        if self.is_forward_user():
            user: OriginalUser = self.message.forward_origin.sender_user  # type: ignore [union-attr]
            return self._forward_user(
                id=user.id,
                is_bot=user.is_bot,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                is_premium=user.is_premium,
            )

        if self.is_chat():
            chat: OriginalChat = self.message.forward_origin.sender_chat  # type: ignore [union-attr]
            return self._chat(
                id=chat.id,
                title=chat.title,
            )

        if self.is_channel():
            channel: OriginalChat = self.message.forward_origin.chat  # type: ignore [union-attr]
            return self._channel(
                id=channel.id,
                title=channel.title,
            )

        if self.is_sender_user():
            original_user: OriginalUser = self.message.from_user  # type: ignore [assignment]
            return self._sender_user(
                id=original_user.id,
                is_bot=original_user.is_bot,
                first_name=original_user.first_name,
                last_name=original_user.last_name,
                username=original_user.username,
                is_premium=original_user.is_premium,
            )

        return None
