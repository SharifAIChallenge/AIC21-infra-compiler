import logging

LOG_DIR='/var/log/compiler'
LOG_DIR='/home/kycilius/Documents/dev-null'
loggers=["compiler", "main", "kafka", "minio"]

def init():
    # setting logger
    stdout_h=logging.StreamHandler()
    filelg_h=logging.FileHandler(f"{LOG_DIR}/compiler.log")
    stdout_h.setLevel(logging.DEBUG)
    filelg_h.setLevel(logging.DEBUG)
    stdout_f = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    filelg_f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_h.setFormatter(stdout_f)
    filelg_h.setFormatter(filelg_f)

    for logger_name in loggers:
        logger=logging.getLogger(logger_name)
        logger.addHandler(stdout_h)
        logger.addHandler(filelg_h)
        


def new_token_logger(token):
    
    filelg_h=logging.FileHandler(f"{LOG_DIR}/{token}.log")
    filelg_h.setLevel(logging.DEBUG)
    
    filelg_f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filelg_h.setFormatter(filelg_f)

    for logger_name in loggers:
        logger=logging.getLogger(logger_name)
        logger.addHandler(filelg_h)

def remove_token_logger(token):
    for logger_name in loggers:
        logger=logging.getLogger(logger_name)
        filelg_h=[h for h in logger.handlers if h.baseFilename==f"{LOG_DIR}/{token}.log"]
        logger.removeHandler(filelg_h[0])
