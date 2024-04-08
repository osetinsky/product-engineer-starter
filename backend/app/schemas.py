from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Evidence(BaseModel):
    content: str
    page_number: int
    pdf_name: str
    event_datetime: Optional[datetime] = None

class StepOption(BaseModel):
    key: str
    text: str
    selected: bool

class StepLogic(BaseModel):
    text: str
    selected: bool

class CaseStep(BaseModel):
    key: str
    question: str
    options: List[StepOption]
    reasoning: Optional[str] = None
    decision: Optional[str] = None
    next_step: Optional[str] = None
    is_met: Optional[bool] = None
    is_final: Optional[bool] = None
    evidence: Optional[List[Evidence]] = None
    logic: Optional[List[StepLogic]] = None

class Case(BaseModel):
    id: str = Field(..., alias='case_id') # Use 'case_id' for serialization
    status: str
    procedure_name: str
    cpt_codes: List[str]
    summary: Optional[str] = None
    is_met: bool
    is_complete: bool
    steps: List[CaseStep]
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "case_id": "example_id",
                "status": "submitted",
                "procedure_name": "Example Procedure",
                "cpt_codes": ["12345"],
                "summary": "An example summary.",
                "is_met": False,
                "is_complete": False,
                "steps": [],
                "created_at": "2023-01-01T00:00:00"
            }
        }
