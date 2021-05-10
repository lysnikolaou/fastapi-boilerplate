import typing

from fastapi.responses import JSONResponse


class CustomJSONResponse(JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        return super().render({"data": content})
