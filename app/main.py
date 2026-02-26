import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.utils.config import get_settings
from app.utils.logger import setup_logging
from app.api.routes import monitoring   # ✅ Monitoring route

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.log_level)
    logging.getLogger(__name__).info(
        f"Starting {settings.app_name} | env={settings.environment}"
    )
    yield
    logging.getLogger(__name__).info("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# ✅ Register APIs
app.include_router(monitoring.router)


@app.get("/health", tags=["system"])
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }
