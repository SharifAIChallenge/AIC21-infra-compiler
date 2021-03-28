import enum
from compiler import Compiler
import kafka_cli as kcli

def push_event(event):
    

while True:
    data = kcli.get_message()
    event = Compiler.compile(data['code_id'], data['language'])
    push_event(event)
    
# for message in consumer:
#     data = json.loads(message.value.decode("utf-8"))
#     result = Compiler.compile(
#         code_id=data['code_id'], language=data['language'])
#     if result:
#         consumer.commit()
#     else:
#         try_count = 0
#         while not Compiler.compile(code_id=data['code_id'],
#                                    language=data['language']) and try_count < maximum_try_count:
#             try_count += 1
#             time.sleep(try_count)
#         consumer.commit()
