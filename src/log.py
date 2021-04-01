import logging

LOG_DIR='/var/log/compiler'
loggers = ["compiler", "main", "kafka", "minio"]
default_format = logging.Formatter('===[%(name)s]===[%(levelname)s]===\t %(message)s')
    

def init():

    # setting logger
    stdout_h = logging.StreamHandler()
    filelg_h = logging.FileHandler(f"{LOG_DIR}/compiler.log")
    stdout_h.setLevel(logging.INFO)
    filelg_h.setLevel(logging.INFO)
    stdout_h.setFormatter(default_format)
    filelg_h.setFormatter(default_format)

    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(stdout_h)
        logger.addHandler(filelg_h)


def new_token_logger(token):

    filelg_h = logging.FileHandler(f"{LOG_DIR}/{token}.log")
    filelg_h.setLevel(logging.INFO)

    filelg_h.setFormatter(default_format)

    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.addHandler(filelg_h)


def remove_token_logger(token):
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        filelg_h = [h for h in logger.handlers if h.baseFilename ==
                    f"{LOG_DIR}/{token}.log"]
        logger.removeHandler(filelg_h[0])
