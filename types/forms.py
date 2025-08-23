from pydantic import BaseModel
from datetime import date

class ParticipantForm(BaseModel):
    name: str
    birth_date: date
    weight: float
    academy: str
    height: float
    category: str
    email: str
    grade: str | None = None
    belt: str | None = "white"
    torneo: str