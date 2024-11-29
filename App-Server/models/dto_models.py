# data transfer objects classes
# objects which we get from api or try to pass to api

from pydantic import BaseModel, Field
from datetime import datetime


# create dto's:
class TaskCreateDTO(BaseModel):
    task_name: str = Field(min_length=1)
    task_id: str = Field(min_length=1)
    creation_date: datetime


class MessageCreateDTO(BaseModel):
    text: str = Field(min_length=1)
    publication_date: datetime = None
    user_id: str = None
    message_id: str = None


class PredictionCreateDTO(BaseModel):
    positive_prob: float
    negative_prob: float
    neutral_prob: float
    conclusion: str = Field(min_length=1)


# jira dto's:
class JiraTaskMessageDTO(BaseModel):
    message_id: str
    publication_date: str = Field(min_length=1)
    user_id: str
    text: str = Field(min_length=1)


class JiraTaskMessageAnalyzed(JiraTaskMessageDTO):
    negative_prob: float = 0
    positive_prob: float = 0
    neutral_prob: float = 0
    conclusion: str = ""


class JiraTaskCommentsDTO(BaseModel):
    task_id: str
    task_name: str = Field(min_length=1)
    creation_date: str = Field(min_length=1)
    messages: list[JiraTaskMessageDTO] = []


# ml service dto's:
class MLServiceResponseDTO(BaseModel):
    text: str = Field(min_length=1)
    negative_prob: float = Field(ge=0, le=1)
    positive_prob: float = Field(ge=0, le=1)
    neutral_prob: float = Field(ge=0, le=1)
    conclusion: str


class ServiceErrorResponse(BaseModel):
    code: int
    message: str = Field(min_length=1)


class TextAnalysisRequestDTO(BaseModel):
    text: str = Field(min_length=1)


# settings dto:
class AppSettingsShow(BaseModel):
    INIT_DATABASE: bool
    DATABASE_URL: str
    JIRA_SERVER: str
    JIRA_ISSUE_KEY: str
    JIRA_SERVER: str
    ML_SERVICE_URL: str
