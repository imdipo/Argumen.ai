import json
from confluent_kafka import Producer

# producer, responsible for making the worker able to send the message to kafka

def delivery_report(err, msg):
    """Callback buat ngecek apakah pesan beneran nyampe ke Kafka Broker"""
    if err is not None:
        print(f"[KAFKA ERROR] Pengiriman gagal: {err}")
    else:
        print(f"[KAFKA SUCCESS] Pesan terkirim ke {msg.topic()} [Partition: {msg.partition()}] pada Offset: {msg.offset()}")

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def send_event(topic:str, key:str, payload:str, callback=delivery_report):
    try:
        producer.produce(
            topic,
            key,
            value=json.dumps(payload).encode('utf-8'),
            on_delivery=callback,
        )

        producer.flush()
    except Exception as e:
        print(f"[ERROR] Gagal memproses event ke Kafka: {e}")
