from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide_number(a,b):
    try:
        result = a/b
        logger.info("Dividing two numbers")
        return result
    except Exception as e:
        logger.error("Error occurred while dividing two numbers")
        raise CustomException(str(e), sys)
    
if __name__ == "__main__":
    logger.info("Starting the program")
    try:
        divide_number(10,0)
    except CustomException as e:
        logger.error(str(e))
