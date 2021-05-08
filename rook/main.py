from fastapi import FastAPI

from rook.api import api

app = FastAPI(title="rook", openapi_url="/api/openapi.json")

app.include_router(api.router)
