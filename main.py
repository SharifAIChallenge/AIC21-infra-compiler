import enum
from compiler import Compiler
import kafka_cli as kcli


while True:
    data = kcli.get_message()
    event = Compiler.compile(data['code_id'], data['language'])
    kcli.push_event(event)
    
