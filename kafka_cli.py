import enum
from kafka import KafkaConsumer, KafkaProducer
from os import getenv
import json
import logging

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s - %(levelname)s:%(message)s')
KAFKA_ENDPOINT = getenv('KAFKA_ENDPOINT')
KAFKA_CONSUMER_GP = getenv('KAFKA_CONSUMER_GP')


class Topics(enum.Enum):
    STORE_CODE = getenv('KAFKA_TOPIC_STORE_CODE')
    EVENTS = getenv('KAFKA_TOPIC_EVENTS')


consumer = KafkaConsumer(
    Topics.STORE_CODE.value,
    bootstrap_servers=KAFKA_ENDPOINT,
    group_id=KAFKA_CONSUMER_GP,
    auto_offset_reset='latest',
    enable_auto_commit=False,
)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_ENDPOINT,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


def get_consumer():
    return consumer


def get_message():
    for message in consumer:
        data = json.loads(message.value.decode("utf-8"))
        yield data
        consumer.commit()


def push_event(key,value) -> bool:
    try:
        producer.send(topic=Topics.EVENTS.value,key=key ,value=value)
        producer.flush()
        return True
    except Exception as e:
        logging.warning(e)
        return False
