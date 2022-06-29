from fastapi import FastAPI

from app.routers import user, transaction
from app.services.database.base import get_session, get_session_stub


def application_factory():
    application = FastAPI()

    application.dependency_overrides[get_session_stub] = get_session

    application.include_router(user.router)
    application.include_router(transaction.router)

    return application


app = application_factory()
