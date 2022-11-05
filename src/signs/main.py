import logging
import os

from fastapi import FastAPI

from signs.config import SignsAppSettings
from signs.customized_logging import configure_logging
from signs.routers import notion

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

app_settings = SignsAppSettings()


def create_directory(dirs):
    for directory in dirs:
        try:
            os.mkdir(directory)
            logger.info(f"{directory} is created")
        except OSError:
            logger.info(f"Skipping creating {directory} since it exists.")


@app.on_event("startup")
async def startup_event():
    print(app_settings)


@app.get("/", tags=["Index"])
async def index():
    message = "Vital Signs is working! See the docs at /api/v1/docs"
    return {"success": True, "message": message}


if __name__ == "__main__":
    import uvicorn

    logger.warning("Friendly Warning: Local Development...")
    uvicorn.run(
        "signs.main:app",
        host=app_settings.APP_HOST,
        port=app_settings.APP_PORT,
        reload=True,
        workers=1,
    )


app.include_router(notion.router)
