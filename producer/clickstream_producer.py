"""
Clickstream Event Producer for Kafka
Simulates user activity events for recommendation pipeline.
"""
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
TOPIC = "clickstream"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

users = [f"user_{i}" for i in range(1, 101)]
products = [f"product_{i}" for i in range(1, 51)]
actions = ["view", "click", "purchase"]

def generate_event():
    return {
        "user_id": random.choice(users),
        "product_id": random.choice(products),
        "action": random.choice(actions),
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    print("Starting clickstream producer...")
    while True:
        event = generate_event()
        producer.send(TOPIC, event)
        print(f"Sent: {event}")
        time.sleep(0.5)
