import enum
from compiler import compile
import kafka_cli as kcli


while True:
    try:
        data = kcli.get_message()
        event = compile(data['code_id'], data['language'])
        kcli.push_event(event)
    except Exception as e:
        print(e)
