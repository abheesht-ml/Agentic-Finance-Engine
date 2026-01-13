from pydantic import BaseModel, Field
class InputfromUser(BaseModel):
    company_ticker: str = Field(..., min_length=1, max_length=6)
    years: int = Field(ge=1)
class ProcessedDocument(BaseModel):
    content: str
    metadata: dict