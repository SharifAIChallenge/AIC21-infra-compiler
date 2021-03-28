import enum
from compiler import Compiler
from kafka import KafkaConsumer
import json
import time
from os import getenv

KAFKA_ENDPOINT = getenv('KAFKA_ENDPOINT')


class Topics(enum.Enum):
    STORE_CODE = "store-code"


maximum_try_count = 10

consumer = KafkaConsumer(
    Topics.STORE_CODE.value,
    bootstrap_servers=KAFKA_ENDPOINT,
    group_id=None,
    auto_offset_reset='earliest',
    enable_auto_commit=False,
)

for message in consumer:
    data = json.loads(message.value.decode("utf-8"))
    result = Compiler.compile(code_id=data['code_id'], language=data['language'])
    if result:
        consumer.commit()
    else:
        try_count = 0
        while not Compiler.compile(code_id=data['code_id'],
                                   language=data['language']) and try_count < maximum_try_count:
            try_count += 1
            time.sleep(try_count)
        consumer.commit()
