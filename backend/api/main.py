from fastapi import FastAPI
from .database import Base, engine
from .routers import users_router, books_router, loans_router
from .logging_config import setup_logging

def create_api() -> FastAPI:
    setup_logging()
    api = FastAPI(title="Digital Library API",
                  version="0.0.1")

    Base.metadata.create_all(bind=engine)

    @api.get("/health")
    def health():
        return {"status": "ok"}

    api.include_router(users_router)
    api.include_router(books_router)
    api.include_router(loans_router)

    return api

api = create_api()
