from pydantic import BaseSettings, validator


class SignsAppSettings(BaseSettings):
    APP_PORT: int = 8080
    APP_HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "local"

    NOTION_SECRET_OB: str

    @validator("ENVIRONMENT", pre=True)
    def validate_env(cls, v):
        if v in {"local", "docker", "dev", "prod", "test"}:
            return v

    class Config:
        case_sensitive = True


app_settings = SignsAppSettings(_env_file=".env")
