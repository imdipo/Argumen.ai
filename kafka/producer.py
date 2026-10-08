import json
from confluent_kafka import Producer

# producer, responsible for making the worker able to send the message to kafka

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def send_event(topic:str, key:str, payload:str, callback):
    producer.produce(
        topic,
        key,
        callback,
        value=json.dumps(payload).encode('utf-8'),
    )

    producer.flush
