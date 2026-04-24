# List all the paths used in the project in this file. This will help us to manage the paths easily and avoid hardcoding the paths in the code.
import os

####################### DATA INGESTION PATHS #######################

RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR,"raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR,"train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR,"test.csv")

CONFIG_PATH = "config/config.yaml"


####################### DATA PROCESSING PATHS #######################

PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_FILE_PATH = os.path.join(PROCESSED_DIR,"processed_train.csv")
PROCESSED_TEST_FILE_PATH = os.path.join(PROCESSED_DIR,"processed_test.csv")


######################## MODEL TRAINING PATHS #######################
MODEL_OUTPUT_PATH = "artifacts/models/lgmb_model.pkl"