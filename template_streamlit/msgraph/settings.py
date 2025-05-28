from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_client_id: str = ""
    azure_tenant_id: str = ""
    azure_client_secret: str = ""
    microsoft_graph_user_scopes: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
