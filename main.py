import enum
from compiler import compile
import kafka_cli as kcli

while True:
    try:
        data = kcli.get_message()
        print(f"got new record:{data}")
        event = compile(data['code_id'], data['language'])
        print(f"resulting event is:{event}")
        kcli.push_event(event)
    except Exception as e:
        print(e)
