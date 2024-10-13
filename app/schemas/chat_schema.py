from pydantic import BaseModel, field_validator
class ChatRequest(BaseModel):
    message: str
    language_model_name: str = "gemini"

    @field_validator("language_model_name")
    def validate_language_model_name(cls, v):
        valid_models = ["gemini", "langchain", "llamaindex"]
        if v not in valid_models:
            raise ValueError(f"Invalid language model: {v}. Must be one of {valid_models}.")
        return v
