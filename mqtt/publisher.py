# mqtt/publisher.py

import json

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "smart_home_energy"

client = mqtt.Client()

client.connect(BROKER, PORT, 60)


def publish_reading(data):

    payload = json.dumps(data)

    client.publish(TOPIC, payload)
