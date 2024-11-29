from models.dto_models import TextAnalysisRequestDTO, ServiceErrorResponse, MLServiceResponseDTO
from settings.app_settings import settings
from requests_tools.ml_service_tools import *
from database.repos_utils import *
import requests


def analyse_text_service(request_dto: TextAnalysisRequestDTO, db: Session):
    text = request_dto.text

    response = requests.post(settings.ML_SERVICE_URL + ANALYSIS, json={'text': text})

    if response.status_code != SUCCESS_CODE:
        return ServiceErrorResponse.model_validate({'code': response.status_code,
                                                    'message': "ml server error with http code - " +
                                                               str(response.status_code)
                                                    })
    ml_service_response = MLServiceResponseDTO.model_validate(response.json())

    # save results to database
    save_text_analysis(db, ml_service_response)

    return ml_service_response


def save_text_analysis(db: Session, mlServiceResponseDTO: MLServiceResponseDTO):
    messageCreateDTO = MessageCreateDTO(**mlServiceResponseDTO.model_dump())
    message_saved_db = save_text(db, messageCreateDTO)

    message_id = message_saved_db.id
    predictionCreateDTO = PredictionCreateDTO(**mlServiceResponseDTO.model_dump())
    save_prediction(db, predictionCreateDTO, message_id)
