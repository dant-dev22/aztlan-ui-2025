from pydantic import BaseModel
from datetime import date

class ParticipantForm(BaseModel):
    name: str
    birth_date: date
    weight: float
    academy: str
    category: str
    email: str
    belt: str | None = "white"
    torneo: str