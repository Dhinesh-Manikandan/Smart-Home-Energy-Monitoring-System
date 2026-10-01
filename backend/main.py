from .metrics_crud import get_metrics

from datetime import datetime

# pyrefly: ignore [missing-import]
from fastapi import FastAPI

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

# pyrefly: ignore [missing-import]
from fastapi import Depends

from .database import engine

from .models import Base

from .dependencies import get_db

from .schemas import EnergyReadingCreate

from .crud import (
    create_reading,
    get_all_readings,
    get_latest_reading,
    get_reading_count,
    delete_all_readings,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Home Energy API")


@app.get("/")
def root():

    return {"message": "Smart Home Energy Monitoring API"}


@app.post("/api/readings")
def add_reading(reading: EnergyReadingCreate, db: Session = Depends(get_db)):

    return create_reading(
        db=db,
        voltage=reading.voltage,
        current=reading.current,
        power=reading.power,
        energy=reading.energy,
        cost=reading.cost,
        appliance=reading.appliance,
        state=reading.state,
        alert=reading.alert,
        temperature=reading.temperature,
        humidity=reading.humidity,
        occupancy=reading.occupancy,
    )


@app.get("/api/readings")
def fetch_readings(db: Session = Depends(get_db)):

    return get_all_readings(db)


@app.get("/api/latest")
def latest_reading(db: Session = Depends(get_db)):

    return get_latest_reading(db)


@app.get("/api/stats")
def stats(db: Session = Depends(get_db)):

    latest = get_latest_reading(db)

    total_records = get_reading_count(db)

    return {
        "total_records": total_records,
        "latest_power": latest.power if latest else 0,
        "latest_energy": latest.energy if latest else 0,
        "latest_cost": latest.cost if latest else 0,
    }


@app.delete("/api/reset")
def reset_database(db: Session = Depends(get_db)):

    deleted = delete_all_readings(db)

    return {"message": "Database cleared successfully", "records_deleted": deleted}


from datetime import datetime
from .metrics_crud import get_metrics


@app.get("/api/device-health")
def device_health(db: Session = Depends(get_db)):

    metrics = get_metrics(db)

    now = datetime.utcnow()

    seconds_since_last = None

    if metrics.last_message_time:
        seconds_since_last = int((now - metrics.last_message_time).total_seconds())

    uptime = 0

    if metrics.messages_received:
        uptime = metrics.messages_received * 5

    return {
        "mqtt_connected": metrics.mqtt_connected,
        "messages_received": metrics.messages_received,
        "seconds_since_last_message": seconds_since_last,
        "last_message_time": metrics.last_message_time,
        "uptime_seconds": uptime,
    }


@app.get("/api/system-health")
def system_health(db: Session = Depends(get_db)):

    metrics = get_metrics(db)

    now = datetime.utcnow()

    seconds_since_last = None

    if metrics.last_message_time:
        seconds_since_last = int((now - metrics.last_message_time).total_seconds())

    uptime = 0

    if metrics.messages_received:
        uptime = metrics.messages_received * 5

    return {
        "mqtt_connected": metrics.mqtt_connected,
        "messages_received": metrics.messages_received,
        "seconds_since_last_message": seconds_since_last,
        "last_message_time": metrics.last_message_time,
        "uptime_seconds": uptime,
    }
