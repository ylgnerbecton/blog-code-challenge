from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.application.middlewares.response import ResponseMiddleware
from src.routers import router
from src.settings import settings


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            title=settings.PROJECT_NAME,
            version="0.1.0",
        )
        self._setup_application()

    def _setup_application(self):
        self.include_router(router, prefix=settings.ROOT_PATH)
        self._setup_middlewares()

    def _setup_middlewares(self):
        middlewares = [CorrelationIdMiddleware, ResponseMiddleware]

        if settings.BACKEND_CORS_ORIGINS:
            middlewares.append(CORSMiddleware)

        for middleware in middlewares:
            self.add_middleware(middleware)

        if CORSMiddleware in middlewares:
            self.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )


app = App()
