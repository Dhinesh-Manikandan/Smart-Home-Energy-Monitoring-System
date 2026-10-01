# Smart Home Energy Monitoring System

## Overview

The Smart Home Energy Monitoring System is an Industry-Oriented IoT project designed to monitor electrical energy consumption in real time using an ESP32 microcontroller, MQTT communication, FastAPI backend services, SQLite database storage, and a Streamlit analytics dashboard.

The system simulates a smart energy meter capable of collecting voltage and current readings, calculating power consumption, estimating energy usage, storing telemetry data, and visualizing consumption trends through an interactive dashboard.

This project demonstrates a complete end-to-end IoT architecture commonly used in smart homes, building automation systems, energy management platforms, and industrial monitoring solutions.

---

## Problem Statement

Electricity consumption is often invisible to users until the monthly utility bill arrives. Without real-time visibility into power usage, it becomes difficult to:

- Identify energy-intensive appliances
- Detect excessive energy consumption
- Monitor consumption patterns
- Estimate electricity costs
- Improve energy efficiency

This project addresses these challenges by providing a real-time energy monitoring platform that continuously tracks electrical parameters and presents actionable insights through a dashboard.

---

## Objectives

- Monitor voltage and current values in real time
- Calculate instantaneous power consumption
- Estimate cumulative energy consumption
- Estimate electricity cost
- Store telemetry data for historical analysis
- Visualize energy trends using interactive charts
- Implement MQTT-based IoT communication
- Demonstrate a complete Industry 4.0 style architecture

---

## System Architecture

The system follows a modern IoT architecture:

```text
Potentiometers (Virtual Sensors)
            │
            ▼
ESP32 (Wokwi Simulation)
            │
            ▼
MQTT Broker (HiveMQ)
            │
            ▼
MQTT Subscriber
            │
            ▼
FastAPI Backend
            │
            ▼
SQLite Database
            │
            ▼
Streamlit Dashboard
```

For architecture diagrams and implementation screenshots, refer to the images available inside the `images/` folder.

---

## Technologies Used

### Hardware Simulation

- ESP32 DevKit V4
- OLED SSD1306 Display
- Potentiometers (Voltage and Current Simulation)
- Wokwi Simulator

### Communication Layer

- MQTT Protocol
- HiveMQ Public Broker
- Paho MQTT Client

### Backend

- Python
- FastAPI
- SQLAlchemy
- Uvicorn

### Database

- SQLite

### Dashboard

- Streamlit
- Plotly

### Development Tools

- PlatformIO
- VS Code / Antigravity IDE
- Git
- GitHub

---

## Features

### Real-Time Monitoring

- Voltage Monitoring
- Current Monitoring
- Power Monitoring
- Energy Consumption Tracking
- Cost Estimation

### IoT Communication

- ESP32 MQTT Publisher
- MQTT Subscriber Service
- Real-Time Data Transfer

### Data Persistence

- SQLite Storage
- Historical Data Retrieval
- Telemetry Logging

### Analytics Dashboard

- Live Monitoring Panel
- Device Health Center
- Power Trend Visualization
- Energy Consumption Analysis
- Appliance Monitoring
- CSV Report Export

### Device Health Monitoring

- MQTT Connection Status
- Message Counter
- Last Message Timestamp
- System Uptime Tracking

---

## Project Structure

```text
Smart-Home-Energy-Monitoring-System/

│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── crud.py
│   ├── schemas.py
│   ├── metrics_crud.py
│   └── dependencies.py
│
├── dashboard/
│   ├── app.py
│   ├── api_client.py
│   ├── charts.py
│   └── analytics.py
│
├── mqtt/
│   └── subscriber.py
│
├── wokwi_simulation/
│   ├── src/
│   │   └── main.cpp
│   ├── diagram.json
│   ├── platformio.ini
│   └── wokwi.toml
│
├── images/
│
├── docs/
│
├── reports/
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

## Data Flow

### Step 1

Voltage and current values are generated using potentiometers connected to the ESP32 simulation.

### Step 2

ESP32 calculates:

```text
Power = Voltage × Current
```

### Step 3

ESP32 publishes telemetry data to the MQTT broker.

Example payload:

```json
{
  "voltage": 240,
  "current": 5,
  "power": 1200
}
```

### Step 4

The MQTT subscriber receives the message.

### Step 5

Additional metrics are calculated:

- Energy Consumption
- Cost Estimation
- Device Metrics

### Step 6

Data is stored in SQLite.

### Step 7

FastAPI serves data through REST APIs.

### Step 8

Streamlit retrieves data and displays analytics.

---

## Energy Calculation Logic

Instantaneous Power:

```text
Power (W) = Voltage × Current
```

Cumulative Energy:

```text
Energy += (Power × IntervalSeconds) / 3600000
```

Estimated Cost:

```text
Cost = Energy × ElectricityTariff
```

---

## API Endpoints

### Root

```http
GET /
```

Returns API status.

---

### Add Reading

```http
POST /api/readings
```

Stores a new energy reading.

---

### Get All Readings

```http
GET /api/readings
```

Returns all stored readings.

---

### Latest Reading

```http
GET /api/latest
```

Returns the most recent energy reading.

---

### Statistics

```http
GET /api/stats
```

Returns aggregated statistics.

---

### Device Health

```http
GET /api/device-health
```

Returns MQTT and system health information.

---

### System Health

```http
GET /api/system-health
```

Returns device telemetry health metrics.

---

### Reset Database

```http
DELETE /api/reset
```

Removes all stored readings.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Smart-Home-Energy-Monitoring-System.git

cd Smart-Home-Energy-Monitoring-System
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

The project requires four components to run simultaneously.

### Terminal 1 — FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Terminal 2 — MQTT Subscriber

```bash
python mqtt/subscriber.py
```

---

### Terminal 3 — Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard:

```text
http://localhost:8501
```

---

### Terminal 4 — ESP32 Simulation

Open the Wokwi simulation project:

```text
wokwi_simulation/
```

Run the simulation using PlatformIO and Wokwi.

The ESP32 will begin publishing MQTT messages automatically.

---

## Demonstration

The following workflow can be demonstrated:

1. Adjust voltage potentiometer.
2. Adjust current potentiometer.
3. Observe OLED display updates.
4. Observe MQTT messages being published.
5. Observe subscriber receiving messages.
6. Observe FastAPI storing readings.
7. Observe dashboard updating in real time.

Project screenshots are available inside the `images/` folder.

---

## Real-World Applications

- Smart Home Energy Monitoring
- Building Energy Management Systems
- Industrial Energy Auditing
- Smart Metering Solutions
- Facility Management Platforms
- IoT-Based Utility Monitoring
- Renewable Energy Monitoring

---

## Future Enhancements

- Real Hardware Integration
- Smart Meter Integration
- Solar Energy Monitoring
- Predictive Analytics
- Mobile Application
- Cloud Deployment
- Multi-Device Monitoring
- User Authentication
- Automated PDF Reporting

---

## Learning Outcomes

This project demonstrates practical experience with:

- IoT Architecture Design
- ESP32 Programming
- MQTT Communication
- FastAPI Development
- Database Design
- Streamlit Dashboards
- Real-Time Data Processing
- Telemetry Monitoring
- Industry-Oriented System Integration

---

## Author

Dhinesh Babu C M

Industry-Oriented IoT Project

Smart Home Energy Monitoring System
