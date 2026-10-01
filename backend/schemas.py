from pydantic import BaseModel
from datetime import datetime


class EnergyReadingCreate(BaseModel):

    voltage: float

    current: float

    power: float

    energy: float

    cost: float

    appliance: str

    state: str = "ON"

    alert: str


class EnergyReadingResponse(
    EnergyReadingCreate
):

    id: int

    timestamp: datetime

    class Config:

        from_attributes = True