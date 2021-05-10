from __future__ import annotations

from fastapi import Request
from fastapi.security.base import SecurityBase

from rook.core.exceptions import AuthenticationFailed, NotAuthenticated


class BearerAuth(SecurityBase):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(self, request: Request) -> str:
        auth_header: str | None = request.headers.get("Authorization")
        if not auth_header:
            raise NotAuthenticated()

        authorization = auth_header.split()
        if authorization[0].lower() != "bearer":
            raise NotAuthenticated()

        if len(authorization) == 1:
            raise AuthenticationFailed("Invalid Authorization header. No credentials provided.")
        elif len(authorization) > 2:
            raise AuthenticationFailed(
                "Invalid Authorization header. Malformed credentials provided."
            )

        return authorization[1]
