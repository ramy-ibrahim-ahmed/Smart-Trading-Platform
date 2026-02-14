from enum import Enum


class GeminiModel(Enum):
    LARGE = "gemini-2.5-pro"
    SMALL = "gemini-2.5-flash"


class OpenAIModel(Enum):
    LARGE = "gpt-4.1"
    SMALL = "gpt-4.1-mini"


class ModelSize(Enum):
    LARGE = "large"
    SMALL = "small"


class TaskModelConfig:
    BESTFIT_QUERY: ModelSize = ModelSize.SMALL
    BESTFIT_RESPOND: ModelSize = ModelSize.SMALL
    BESTFIT_DESCRIPE: ModelSize = ModelSize.SMALL
    DESCRIPE: ModelSize = ModelSize.SMALL
