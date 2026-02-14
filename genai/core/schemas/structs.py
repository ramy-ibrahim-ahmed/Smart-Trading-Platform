from pydantic import BaseModel, Field


class SemanticDescription(BaseModel):
    text: str = Field(..., description="The semantic description")
