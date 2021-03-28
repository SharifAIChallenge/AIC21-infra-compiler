import enum
from compiler import compile
import kafka_cli as kcli

codes=kcli.get_message();

for code in codes:
    try:
        code = codes.__next__();
        print(f"got new record:{code}")
        event = compile(code['code_id'], code['language'])
        print(f"resulting event is:{event}")
        kcli.push_event(event)
    except Exception as e:
        print(e)
