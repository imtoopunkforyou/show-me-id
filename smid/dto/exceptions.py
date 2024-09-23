from typing import Self


class MessageDefinitionError(TypeError):
    """Error identifying message."""

    detail = 'Failed to classify the incoming message.'

    def __init__(self: Self, *args: object):
        if not args:
            args = (self.detail, )
        super().__init__(*args)
