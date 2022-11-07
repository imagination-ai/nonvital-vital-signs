import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from signs.config import SignsAppSettings
from signs.customized_logging import configure_logging
from signs.middleware import add_middleware
from signs.routers import notion

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Nonvital Vital Signs")

app_settings = SignsAppSettings()
add_middleware(app)

origins = ["http://localhost:3000", "https://osmanbaskaya.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


# @app.exception_handler(Exception)
# def handle_exception(req, exc):
#     logger.error("Exception occured", exc_info=exc)  # This does not
#     return Response(...)


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


app.include_router(notion.router, prefix="/api/v1")

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
