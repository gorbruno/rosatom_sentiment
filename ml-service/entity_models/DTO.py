from pydantic import BaseModel, Field, model_validator


class TextAnalysisRequestDTO(BaseModel):
    text: str = Field(min_length=1)


class TextAnalysisResponseDTO(BaseModel):
    text: str = Field(min_length=1)
    negative_prob: float = Field(ge=0, le=1)
    positive_prob: float = Field(ge=0, le=1)
    neutral_prob: float = Field(ge=0, le=1)
    conclusion: str

    @model_validator(mode='after')
    def check_probs_sum(self):
        epsilon = 0.00001
        probs_sum = self.negative_prob + self.positive_prob + self.neutral_prob

        if probs_sum - 1 > epsilon:
            raise ValueError(f"probs sum should be equal to 1, but {probs_sum} got: "
                             f"positive={self.positive_prob} negative={self.negative_prob} neutral={self.neutral_prob}")

        return self

    @model_validator(mode='after')
    def check_conclusion(self):
        possible_conclusions = {"NEUTRAL", "POSITIVE", "NEGATIVE"}

        if self.conclusion not in possible_conclusions:
            raise ValueError(f"invalid conclusion, should be one of \"NEUTRAL\", \"POSITIVE\", \"NEGATIVE\"")

        return self
