import enum
from compiler import Compiler
from kafka import KafkaConsumer,KafkaProducer
import json
import time
from os import getenv

KAFKA_ENDPOINT = getenv('KAFKA_ENDPOINT')

class Topics(enum.Enum):
    STORE_CODE = getenv('KAFKA_TOPIC_STORE_CODE')
    EVENTS = getenv('KAFKA_TOPIC_EVENTS')

consumer = KafkaConsumer(
    Topics.STORE_CODE,
    bootstrap_servers=KAFKA_ENDPOINT,
    group_id=None,
    auto_offset_reset='earliest',
    enable_auto_commit=False,
)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_ENDPOINT,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def get_message():
    for message in consumer:
        yield json.loads(message.value.decode("utf-8"))
        consumer.commit()

def push_event(event) -> bool:
    try:
        producer.send(topic=Topics.EVENTS, value=event)
        producer.flush()
        return True
    except Exception as e:
        print(e)
        return False
