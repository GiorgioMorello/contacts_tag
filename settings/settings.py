from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    
    SSH_HOST: str
    SSH_PORT: int = 22
    SSH_USER: str
    SSH_PRIVATE_KEY: str
    SSH_PRIVATE_KEY_PASS: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    CORS_ORIGINS: list[str]
    
    model_config = SettingsConfigDict(
        validate_assignment=True,
        env_file='.env',
        env_file_encoding='utf-8'
    )
    
    
SETTINGS = Settings() # type: ignore
    