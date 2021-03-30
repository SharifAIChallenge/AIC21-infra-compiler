import enum
from compiler import compile
import kafka_cli as kcli
import json
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s:%(message)s')


for message in kcli.get_consumer():
    try:
        code = json.loads(message.value.decode("utf-8"))
        logging.warning(f"got new record:{code}")
        event = compile(code['code_id'], code['language'])
        logging.warning(f"resulting event is:{event}")
        kcli.push_event(event.__dict__)
    except Exception as e:
        logging.warning(e)
    finally:
        kcli.get_consumer().commit()
