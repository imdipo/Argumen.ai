from confluent_kafka import Consumer
"""
i think da topic is for where this data comes from

group id is identifier for the consumer worker, it makes the same data could be sent to differenct purpose of workers
"""

def create_consumer(topic: str, group_id: str):
    c = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        'enable.auto.commit': False
    })

    c.subscribe([topic])

    return c




