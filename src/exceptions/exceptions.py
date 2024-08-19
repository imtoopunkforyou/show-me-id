class RenderDTOError(TypeError):
    detail = 'Wrong DTO selected.'

    def __init__(self, *args, **kwargs):
        if not args:
            args = (self.detail, )
        super().__init__(*args, **kwargs)


class MessageDefinitionError(TypeError):
    detail = 'Failed to classify the incoming message.'

    def __init__(self, *args, **kwargs):
        if not args:
            args = (self.detail, )
        super().__init__(*args, **kwargs)
