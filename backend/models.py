# backend/models.py

# pyrefly: ignore [missing-import]
from sqlalchemy import Boolean

# pyrefly: ignore [missing-import]
from sqlalchemy import Column

# pyrefly: ignore [missing-import]
from sqlalchemy import Integer

# pyrefly: ignore [missing-import]
from sqlalchemy import Float

# pyrefly: ignore [missing-import]
from sqlalchemy import String

# pyrefly: ignore [missing-import]
from sqlalchemy import DateTime

from datetime import datetime

from .database import Base


class EnergyReading(Base):

    __tablename__ = "energy_readings"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    voltage = Column(Float)

    current = Column(Float)

    power = Column(Float)

    energy = Column(Float)

    cost = Column(Float)

    appliance = Column(String)

    state = Column(String, default="ON")

    alert = Column(String)


class SystemMetrics(Base):

    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, index=True)

    mqtt_connected = Column(Boolean, default=False)

    messages_received = Column(Integer, default=0)

    last_message_time = Column(DateTime, nullable=True)

    subscriber_started = Column(DateTime, default=datetime.utcnow)
