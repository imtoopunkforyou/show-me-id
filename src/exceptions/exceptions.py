class RenderDTOError(TypeError):
    """Error rendering answer."""

    detail = 'Wrong DTO selected.'

    def __init__(self, *args, **kwargs):
        if not args:
            args = (self.detail, )
        super().__init__(*args, **kwargs)


class MessageDefinitionError(TypeError):
    """Error identifying message."""

    detail = 'Failed to classify the incoming message.'

    def __init__(self, *args, **kwargs):
        if not args:
            args = (self.detail, )
        super().__init__(*args, **kwargs)
