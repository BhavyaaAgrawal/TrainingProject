import os
import logging
import time
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

# initiate the default env variables
ENV = os.getenv("ENV", 'local')
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", 30))
LOG_DIR = os.getenv("LOG_DIR", "./logs")

# os.dir(__name__).parent.resolve().mkdir(parents=True, exist_ok=True)
ENABLE_CONSOLE_LOG = ENV in ["local", 'dev', 'test', 'prod']

# current file ie logger>parent(core)>parent(app)>parent(main dir ie FastApiTrainingProject)-> inside this create base_dir for log dir
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_PATH = BASE_DIR / LOG_DIR
print('Base dir for logs =====', BASE_DIR)
APP_LOG_DIR = LOG_PATH / 'app'
ERROR_LOG_DIR = LOG_PATH / 'error'

# create these dir at the time of app start, if not exists
APP_LOG_DIR.mkdir(parents=True, exist_ok=True)
ERROR_LOG_DIR.mkdir(parents=True, exist_ok=True)

class MaxLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level

class CustomFormatter(logging.Formatter):
    def format(self, record):
        try:
            record.relative_path = os.path.relpath(record.pathname, BASE_DIR)
        except ValueError:
            record.relative_path = ""
        return super().format(record)

LOG_FORMAT = (
    "%(asctime)s | %(name)s |  %(levelname)s | %(relative_path)s:%(lineno)d | %(message)s"
)


def create_handler(log_file:Path, log_level:int):
    handler = TimedRotatingFileHandler(filename=log_file,when='midnight',
                                       backupCount=LOG_RETENTION_DAYS, encoding='utf-8')
    handler.setLevel(log_level)
    handler.suffix = ""
    formatter = CustomFormatter(LOG_FORMAT)
    formatter.converter=time.gmtime

    handler.setFormatter(formatter)
    return handler


def setup_logger():
    logger = logging.getLogger('app')
    logger.setLevel(LOG_LEVEL)
    # to stop pythons own logging we need to shut down propogation
    logger.propagate=False

    if logger.handlers:
        return logger
    # create handlers for each type
    app_handler = create_handler(APP_LOG_DIR/'app.log', logging.INFO)
    # below line is required to differentiate and let logger know to add logs other than info as well
    app_handler.addFilter(MaxLevelFilter(logging.ERROR))

    error_handler = create_handler(ERROR_LOG_DIR/'error.log', logging.ERROR)

    logger.addHandler(app_handler)
    logger.addHandler(error_handler)

    if ENABLE_CONSOLE_LOG:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_formatter = CustomFormatter(LOG_FORMAT)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # as fastapi runs on uvicorn server so there are some specific arguments to run logs on else we will get mixed logs
    for name in ('uvicorn', 'uvicorn.error', 'uvicorn.access', 'uvicorn.exception'):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate=False

    return logger