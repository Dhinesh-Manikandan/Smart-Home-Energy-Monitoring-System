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

    temperature: float | None = None

    humidity: float | None = None

    occupancy: str = "UNOCCUPIED"


class EnergyReadingResponse(
    EnergyReadingCreate
):

    id: int

    timestamp: datetime

    class Config:

        from_attributes = True