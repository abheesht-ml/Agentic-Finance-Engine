from pydantic import BaseModel, Field
class InputFromUser(BaseModel):
    company_ticker_name : str = Field(..., min_length=1, max_length=5)
    years_of_files : int = Field(..., ge = 1)
    