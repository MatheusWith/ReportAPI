from collections.abc import AsyncGenerator, Callable
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import Any

import anyio
import fastapi
from fastapi import APIRouter, Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from src.app.core.config import AppSettings, EnvironmentOption, EnvironmentSettings, FileLoggerSettings, ConsoleLoggerSettings, settings
from src.app.middleware.logger_middleware import LoggerMiddleware


# -------------- application --------------
async def set_threadpool_tokens(number_of_tokens: int = 100) -> None:
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = number_of_tokens


def lifespan_factory(
    settings:(
        AppSettings
    ),
) -> Callable[[FastAPI], _AsyncGeneratorContextManager[Any]]:
    """Factory to create a lifespan async context manager for a FastAPI app."""

    @asynccontextmanager
    async def lifespan(app:FastAPI) -> AsyncGenerator:
        from asyncio import Event

        initialization_complete = Event()
        app.state.initialization_complete = initialization_complete

        await set_threadpool_tokens()

        try:
            initialization_complete.set()
            yield
        finally:
            pass

    return lifespan

def create_application(
    router: APIRouter,
    settings: (AppSettings),
    lifespan: Callable[[FastAPI], _AsyncGeneratorContextManager[Any]],
    **kwargs: Any,
) -> FastAPI:
    """Creates and configures a FastAPI application based on the provided settings.

    This function initializes a FastAPI application and configures it with various settings
    and handlers based on the type of the `settings` object provided.

    Parameters
    ----------
    router : APIRouter
        The APIRouter object containing the routes to be included in the FastAPI application.

    settings
        An instance representing the settings for configuring the FastAPI application.
        It determines the configuration applied:

        - AppSettings: Configures basic app metadata like name, description, contact, and license info.
        **kwargs
        Additional keyword arguments passed directly to the FastAPI constructor.

    Returns
    -------
    FastAPI
        A fully configured FastAPI application instance.

    The function configures the FastAPI application with different features and behaviors
    based on the provided settings. It includes setting up database connections, Redis pools
    for caching, queue, and rate limiting, client-side caching, and customizing the API documentation
    based on the environment settings.
    """
    # --- before creating application ---
    if isinstance(settings, AppSettings):
        to_update = {
            "title": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION,
            "contact": {"name": settings.CONTACT_NAME, "email": settings.CONTACT_EMAIL},
            "license_info": {"name": settings.LICENSE_NAME},
        }
        kwargs.update(to_update)
    if isinstance(settings,EnvironmentSettings):
        kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

    if lifespan is None:
        lifespan = lifespan_factory(settings)

    application = FastAPI(lifespan=lifespan, **kwargs)
    application.include_router(router)

    # if isinstance(settings, CORSSettings):
        # application.add_middleware(
        #     CORSMiddleware,
        #     allow_origins=settings.CORS_ORIGINS,
        #     allow_credentials=True,
        #     allow_methods=settings.CORS_METHODS,
        #     allow_headers=settings.CORS_HEADERS,
        # )

    application.add_middleware(LoggerMiddleware)
    if isinstance(settings,EnvironmentSettings):
        if settings.ENVIRONMENT != EnvironmentOption.PRODUCTION:
            docs_router = APIRouter()

            @docs_router.get("/docs", include_in_schema=False)
            async def get_swagger_documentation() -> fastapi.responses.HTMLResponse:
                return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

            @docs_router.get("/redoc", include_in_schema=False)
            async def get_redoc_documentation() -> fastapi.responses.HTMLResponse:
                return get_redoc_html(openapi_url="/openapi.json", title="docs")

            @docs_router.get("/openapi.json", include_in_schema=False)
            async def openapi() -> dict[str, Any]:
                out: dict = get_openapi(title=application.title, version=application.version, routes=application.routes)
                return out

            application.include_router(docs_router)
    return application
