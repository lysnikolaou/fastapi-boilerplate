from pathlib import Path

import firebase_admin
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from firebase_admin import credentials

from rook.api import api
from rook.core.exceptions import (
    AuthenticationFailed,
    AuthenticationTokenExpired,
    FirebaseException,
    NonUniqueEmailException,
    NotAuthenticated,
)
from rook.core.responses import CustomJSONResponse

ROOK_ROOT = Path(__file__).parent.parent

app = FastAPI(
    title="rook", openapi_url="/api/openapi.json", default_response_class=CustomJSONResponse
)
app.include_router(api.router)


@app.exception_handler(NotAuthenticated)
def not_authenticated_handler(req: Request, exc: NotAuthenticated) -> JSONResponse:
    return JSONResponse({"error": {"code": exc.code, "message": exc.detail, "params": []}})


@app.exception_handler(AuthenticationFailed)
def authentication_failed_handler(req: Request, exc: AuthenticationFailed) -> JSONResponse:
    return JSONResponse({"error": {"code": exc.code, "message": exc.detail, "params": []}})


@app.exception_handler(AuthenticationTokenExpired)
def authentication_token_expired_handler(
    req: Request, exc: AuthenticationTokenExpired
) -> JSONResponse:
    return JSONResponse({"error": {"code": exc.code, "message": exc.detail, "params": []}})


@app.exception_handler(FirebaseException)
def firebase_exception_handler(req: Request, exc: FirebaseException) -> JSONResponse:
    return JSONResponse({"error": {"code": exc.code, "message": exc.detail, "params": exc.args}})


@app.exception_handler(NonUniqueEmailException)
def non_unique_email_exception_handler(req: Request, exc: NonUniqueEmailException) -> JSONResponse:
    return JSONResponse({"error": {"code": exc.code, "message": exc.detail, "params": []}})


FIREBASE_CERTIFICATE_FILE = ROOK_ROOT / "rook" / "core" / "firebase.json"
cred = credentials.Certificate(FIREBASE_CERTIFICATE_FILE.resolve())
firebase_admin.initialize_app(cred)
