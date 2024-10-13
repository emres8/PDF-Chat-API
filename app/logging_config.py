import logging
import sys
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def process_log_record(self, log_record):
        log_record.pop('taskName', None)
        return super().process_log_record(log_record)

def setup_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    formatter = CustomJsonFormatter('%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger

logger = setup_logger()
