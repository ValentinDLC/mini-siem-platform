"""
Core configuration for Mini SIEM Platform
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Mini SIEM Platform"
    version: str = "1.0.0"
    database_url: str = "sqlite:///./siem.db"
    elasticsearch_url: str = "http://localhost:9200"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
