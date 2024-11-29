from fastapi import FastAPI

from entity_models.DTO import TextAnalysisRequestDTO, TextAnalysisResponseDTO
from services.tone_analysis_service import ml_service

app = FastAPI()


@app.post("/analysis")
async def analysis(analysis_dto: TextAnalysisRequestDTO) -> TextAnalysisResponseDTO:
    conclusion, probs_dict = ml_service.predict_probs(analysis_dto.text)

    return TextAnalysisResponseDTO(text=analysis_dto.text,
                                   negative_prob=probs_dict["NEGATIVE"],
                                   positive_prob=probs_dict["POSITIVE"],
                                   neutral_prob=probs_dict["NEUTRAL"],
                                   conclusion=conclusion
                                   )
