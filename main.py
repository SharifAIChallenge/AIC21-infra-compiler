import enum
from compiler import compile
import kafka_cli as kcli


while True:
    data = kcli.get_message()
    event = compile(data['code_id'], data['language'])
    kcli.push_event(event)
    
