from fastapi import FastAPI
from database.database import SessionLocal, Base, engine
from sqlalchemy.orm import Session

from models.dto_models import TextAnalysisRequestDTO, AppSettingsShow
from services.analyse_jira_comments import analyse_comments_in_issue
from settings.app_settings import settings
from services.analyse_text import analyse_text_service
from fastapi import Depends


app = FastAPI()

if settings.INIT_DATABASE:   # create tables if need
    Base.metadata.drop_all(bind=engine)     # drop old tables
    Base.metadata.create_all(bind=engine)   # create new tables


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/analysis/jira")
def jira_analysis(db: Session = Depends(get_db)):
    return analyse_comments_in_issue(settings.JIRA_ISSUE_KEY, db)


@app.post("/analysis/text")
def text_analysis(request_dto: TextAnalysisRequestDTO, db: Session = Depends(get_db)):
    return analyse_text_service(request_dto, db)


@app.get("/settings")
def get_settings() -> AppSettingsShow:
    return settings


# # TODO: remove later
# @app.get("/get_task")
# def get_task_by_id(task_id: str, db: Session = Depends(get_db)):
#     return get_task_by_task_id(db, task_id) is None

