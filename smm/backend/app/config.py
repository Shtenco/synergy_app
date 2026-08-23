from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SINERGY SMM API"
    env: str = "dev"
    database_url: str = "sqlite:///./sinergy_smm.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "dev-change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24
    cors_origins: str = "http://localhost:3000,http://localhost:8081"
    public_base_url: str = "http://localhost:8000"
    vault_addr: str = ""
    vault_token: str = ""
    vault_mount: str = "secret"
    vk_client_id: str = ""
    vk_client_secret: str = ""
    vk_api_version: str = "5.199"
    meta_app_id: str = ""
    meta_app_secret: str = ""
    meta_graph_version: str = "v26.0"
    telegram_webhook_secret: str = ""
    meta_webhook_verify_token: str = ""
    ai_base_url: str = ""
    ai_api_key: str = ""
    ai_model: str = ""
    ai_timeout_seconds: int = 45
    publish_max_attempts: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
