import logging
import os #Creating directories
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR,exist_ok=True)

# storing log records on specific time interval
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%y-%m-%d')}.log")    # inside LOG_FILE a file will look like this "log_2026-05-01.log"

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',  # timeoflog - info,error,warning - messagedescription
    level = logging.INFO #only info,warning and error message will be shown
    
)

def get_logger(name):
    logger = logging.getLogger(name) #logger with the given name is created
    logger.setLevel(logging.INFO) #level is set here
    return logger