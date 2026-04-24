# Used for common utility functions in the project

#Function for reading yaml files : Library required : pyyaml
import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")
        else:
            with open(file_path,"r") as yaml_file:
                config = yaml.safe_load(yaml_file)
                logger.info("YAML file read successfully")
                return config
    except Exception as e:
        logger.error("Error occurred while reading YAML file")
        raise CustomException("Failed to read YAML file", e)
    

def load_data(path):  
    try:
        logger.info(f"Loading data from path: {path}")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error occurred while loading data from path: {path}")
        raise CustomException("Failed to load data", e)