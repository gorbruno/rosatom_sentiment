from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    INIT_DATABASE: bool
    DATABASE_URL: str
    JIRA_SERVER: str
    JIRA_ISSUE_KEY: str
    JIRA_LOGIN: str
    JIRA_PASSWORD: str
    JIRA_SERVER: str

    ML_SERVICE_URL: str
    # DBMS_name://user:password@server:port/database_name


settings = AppSettings(_env_file='settings/settings.env', _env_file_encoding='utf-8')
