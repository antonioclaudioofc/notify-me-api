from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str

    MAIL_TO: str
    MAIL_FROM_ANTONIOCLAUDIODEV: str
    MAIL_FROM_ARENAMANAGER: str
    FRONTEND_URL: str

    API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
