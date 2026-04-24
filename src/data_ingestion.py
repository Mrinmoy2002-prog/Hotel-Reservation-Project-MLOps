import os
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
import config
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml
from config.paths_config import *

logger = get_logger(__name__)

class DataIngestion:

    def __init__(self,config): # Here config is the yaml file content's 
        
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion Started with {self.bucket_name} and file is {self.bucket_file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            # client = storage.Client(project="plasma-bison-458014-d0")
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Raw file is succesfully download to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error("Error while downloading the csv file")
            raise CustomException("Failed to download the csv file", sys)
        
    def split_data(self):
        try:
            logger.info("Starting the splitting of data into train and test")
            df = pd.read_csv(RAW_FILE_PATH)
            train_df, test_df = train_test_split(df, test_size=1-self.train_ratio, random_state=42)

            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")
        except Exception as e:
            logger.error("Error while splitting the data into train and test")
            raise CustomException("Failed to split the data into train and test", sys)

    def run(self): # combining the above two functions in one function to run the data ingestion process
        try:
            logger.info("Starting the data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data Ingestion completed successfully")
        except Exception as e:
            logger.error("Error while running the data ingestion process")
            raise CustomException("Failed to run the data ingestion process", sys)
        finally:
            logger.info("Data Ingestion process completed")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

