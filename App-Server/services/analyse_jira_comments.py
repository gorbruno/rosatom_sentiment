from requests_tools import jira_tools
from requests_tools.ml_service_tools import *
from models.dto_models import JiraTaskCommentsDTO, ServiceErrorResponse, \
    MLServiceResponseDTO, JiraTaskMessageDTO, JiraTaskMessageAnalyzed, TaskCreateDTO
from settings.app_settings import settings
import requests
from database.repos_utils import *


def analyse_comments_in_issue(issue_key, db: Session):
    issue_comments_dict = jira_tools.search_all_comments_in_issue(issue_key)
    # check on error response
    jira_task_comments_dto = JiraTaskCommentsDTO.model_validate(issue_comments_dict)

    # analyse messages
    messages = jira_task_comments_dto.messages
    analysed_messages = []

    for message in messages:
        jira_task_message = JiraTaskMessageDTO.model_validate(message)
        response = requests.post(settings.ML_SERVICE_URL + ANALYSIS, json={'text': message.text})

        if response.status_code != SUCCESS_CODE:
            return ServiceErrorResponse.model_validate({'code': response.status_code,
                                                        'message': "ml server error with http code - " +
                                                                   str(response.status_code)
                                                        })
        ml_service_response = MLServiceResponseDTO.model_validate(response.json())
        jira_task_message_analyzed = JiraTaskMessageAnalyzed(**jira_task_message.model_dump())

        # add analysis labels:
        jira_task_message_analyzed.positive_prob = ml_service_response.positive_prob
        jira_task_message_analyzed.negative_prob = ml_service_response.negative_prob
        jira_task_message_analyzed.neutral_prob = ml_service_response.neutral_prob
        jira_task_message_analyzed.conclusion = ml_service_response.conclusion

        # add to result list:
        analysed_messages.append(jira_task_message_analyzed)

    # save results to database
    task_saved_db = get_issue_by_id(jira_task_comments_dto, db)

    if task_saved_db is None:
        # save not existing task
        task_saved_db = save_issue_to_db(jira_task_comments_dto, db)
    else:
        # update existing task
        task_saved_db = update_issue(jira_task_comments_dto, task_saved_db.id, db)

    save_messages_analysis(analysed_messages, task_saved_db.id, db)

    return analysed_messages


def get_issue_by_id(jiraTaskCommentsDTO: JiraTaskCommentsDTO, db: Session):
    taskCreateDTO = TaskCreateDTO(**jiraTaskCommentsDTO.model_dump())
    return get_task_by_task_id(db, taskCreateDTO.task_id)


def save_issue_to_db(jiraTaskCommentsDTO: JiraTaskCommentsDTO, db: Session):
    taskCreateDTO = TaskCreateDTO(**jiraTaskCommentsDTO.model_dump())
    return save_task(db, taskCreateDTO)


def update_issue(jiraTaskCommentsDTO: JiraTaskCommentsDTO, task_id: int, db: Session):
    taskCreateDTO = TaskCreateDTO(**jiraTaskCommentsDTO.model_dump())
    return update_task(db, task_id, taskCreateDTO)


def save_messages_analysis(analysed_messages: list[JiraTaskMessageAnalyzed], task_id: int, db: Session):
    for analysed_message in analysed_messages:
        messageCreateDTO = MessageCreateDTO(**analysed_message.model_dump())

        message_saved_db = get_message_by_message_id(db, messageCreateDTO.message_id)

        if message_saved_db is None:
            message_saved_db = save_message(db, messageCreateDTO, task_id)

            message_id = message_saved_db.id
            predictionCreateDTO = PredictionCreateDTO(**analysed_message.model_dump())
            save_prediction(db, predictionCreateDTO, message_id)
        else:
            message_saved_db = update_message(db, message_saved_db.id, messageCreateDTO)

            message_id = message_saved_db.id
            predictionCreateDTO = PredictionCreateDTO(**analysed_message.model_dump())
            update_prediction(db, predictionCreateDTO, message_id)

