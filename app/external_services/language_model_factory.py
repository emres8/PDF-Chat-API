from app.external_services.gemini import GeminiLanguageModel
from app.external_services.langchain import LangchainLanguageModel
from app.external_services.llama_index import LlamaIndexLanguageModel



class LanguageModelFactory:
    _model_cache = {}
    @staticmethod
    def get_model(language_model_name: str):
        if language_model_name in LanguageModelFactory._model_cache:
            return LanguageModelFactory._model_cache[language_model_name]

        if language_model_name == "gemini":
            model = GeminiLanguageModel()
        elif language_model_name == "langchain":
            model = LangchainLanguageModel()
        elif language_model_name == "llamaindex":
            model = LlamaIndexLanguageModel()
        else:
            raise ValueError(f"Unsupported model type: {language_model_name}")

        LanguageModelFactory._model_cache[language_model_name] = model
        return model
