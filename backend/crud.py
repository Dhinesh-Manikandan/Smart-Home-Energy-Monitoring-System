# backend/crud.py

from .models import EnergyReading


def create_reading(db, voltage, current, power, energy, cost, appliance, state, alert, temperature=None, humidity=None, occupancy="UNOCCUPIED"):

    reading = EnergyReading(
        voltage=voltage,
        current=current,
        power=power,
        energy=energy,
        cost=cost,
        appliance=appliance,
        state=state,
        alert=alert,
        temperature=temperature,
        humidity=humidity,
        occupancy=occupancy,
    )

    db.add(reading)

    db.commit()

    db.refresh(reading)

    return reading


def get_all_readings(db, limit=500):

    return db.query(EnergyReading).order_by(EnergyReading.id.desc()).limit(limit).all()


def get_latest_reading(db):

    return db.query(EnergyReading).order_by(EnergyReading.id.desc()).first()


def get_reading_count(db):

    return db.query(EnergyReading).count()


def delete_all_readings(db):

    deleted = db.query(EnergyReading).delete()

    db.commit()

    return deleted
