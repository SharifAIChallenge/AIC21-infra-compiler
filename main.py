import enum
from compiler import compile
import kafka_cli as kcli
import json

for message in kcli.get_consumer():
    try:
        code = json.loads(message.value.decode("utf-8"))
        print(f"got new record:{code}")
        event = compile(code['code_id'], code['language'])
        print(f"resulting event is:{event}")
        kcli.push_event(event)
    except Exception as e:
        print(e)
        