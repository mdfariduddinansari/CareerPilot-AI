from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    app_name: str = 'CareerPilot AI API'
    environment: str = 'development'
    secret_key: str = 'change-this-in-production'
    access_token_expire_minutes: int = 1440
    database_url: str = 'sqlite:///./careerpilot.db'
    db_host: str | None = None
    db_port: int = 5432
    db_user: str | None = None
    db_password: str | None = None
    db_name: str | None = None
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    allowed_origins: str = 'http://localhost:5173'

    @property
    def effective_database_url(self) -> str:
        if self.database_url and self.database_url != 'sqlite:///./careerpilot.db':
            return self.database_url
        if self.db_host and self.db_user and self.db_password and self.db_name:
            return (
                f'postgresql+psycopg2://{self.db_user}:{self.db_password}'
                f'@{self.db_host}:{self.db_port}/{self.db_name}'
            )
        return self.database_url


settings = Settings()
