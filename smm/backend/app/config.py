from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SINERGY SMM API"
    env: str = "dev"
    database_url: str = "sqlite:///./sinergy_smm.db"
    jwt_secret: str = "dev-change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 1440
    cors_origins: str = "http://localhost:3000,http://localhost:8081"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
