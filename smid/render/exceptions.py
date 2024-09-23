from typing import Self


class RenderDTOError(TypeError):
    """Error rendering answer."""

    detail = 'Wrong DTO selected.'

    def __init__(self: Self, *args: object) -> None:
        if not args:
            args = (self.detail, )
        super().__init__(*args)
