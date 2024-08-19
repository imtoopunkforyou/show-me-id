from aiogram.enums.message_origin_type import MessageOriginType
from typing import Union
from src.types import SenderUser, Channel, Chat, HiddenUser, ForwardUser, OriginalForwardMessage, OriginalUser, OriginalMessage, AbstractPublicEntity, AbstractUser
from src.exceptions import MessageDefinitionError


class DTOMessage(object):
    _sender_user: SenderUser = SenderUser
    _channel: Channel = Channel
    _chat: Chat = Chat
    _hidden_user: HiddenUser = HiddenUser
    _forward_user: ForwardUser = ForwardUser

    def __init__(self, message: OriginalMessage):
        self.message = message

    def _create_dto_sender_user(self, original: OriginalUser) -> SenderUser:
        return self._sender_user(
            id=original.id,
            is_bot=original.is_bot,
            first_name=original.first_name,
            last_name=original.last_name,
            username=original.username,
            is_premium=original.is_premium,
        )

    def _create_dto_channel(self, original: OriginalForwardMessage) -> Channel:
        return self._channel(
            id=original.chat.id,
            title=original.chat.title,
        )

    def _create_dto_chat(self, original: OriginalForwardMessage) -> Chat:
        return self._chat(
            id=original.sender_chat.id,
            title=original.sender_chat.title,
        )

    def _create_dto_hidden_user(self, original: OriginalForwardMessage) -> HiddenUser:
        return self._hidden_user(
            first_name=original.sender_user_name,
        )

    def _create_dto_forward_user(self, original: OriginalForwardMessage) -> ForwardUser:
        return self._forward_user(
            id=original.sender_user.id,
            is_bot=original.sender_user.is_bot,
            first_name=original.sender_user.first_name,
            last_name=original.sender_user.last_name,
            username=original.sender_user.username,
            is_premium=original.sender_user.is_premium,
        )

    def create(self) -> Union[AbstractPublicEntity, AbstractUser]:
        dto: Union[AbstractPublicEntity, AbstractUser] = None
        original_forward_message: OriginalForwardMessage = self.message.forward_origin
        original_user: OriginalUser = self.message.from_user

        if self.is_forward_user:
            dto: ForwardUser = self._create_dto_forward_user(original_forward_message)
        elif self.is_hidden_user:
            dto: HiddenUser = self._create_dto_hidden_user(original_forward_message)
        elif self.is_chat:
            dto: Chat = self._create_dto_chat(original_forward_message)
        elif self.is_channel:
            dto: Channel = self._create_dto_channel(original_forward_message)
        elif self.is_sender_user:
            dto: SenderUser = self._create_dto_sender_user(original_user)

        if not dto:
            raise MessageDefinitionError

        return dto

    @property
    def is_forward(self) -> bool:
        if self.message.forward_origin:
            return True

        return False

    @property
    def is_forward_user(self) -> bool:
        if self.is_forward:
            return self.message.forward_origin.type == MessageOriginType.USER.value

        return False

    @property
    def is_hidden_user(self) -> bool:
        if self.is_forward:
            return self.message.forward_origin.type == MessageOriginType.HIDDEN_USER.value

        return False

    @property
    def is_chat(self) -> bool:
        if self.is_forward:
            return self.message.forward_origin.type == MessageOriginType.CHAT.value

        return False

    @property
    def is_channel(self) -> bool:
        if self.is_forward:
            return self.message.forward_origin.type == MessageOriginType.CHANNEL.value

        return False

    @property
    def is_sender_user(self) -> bool:
        if not self.is_forward and hasattr(self.message, 'from_user'):
            return isinstance(self.message.from_user, OriginalUser)

        return False
