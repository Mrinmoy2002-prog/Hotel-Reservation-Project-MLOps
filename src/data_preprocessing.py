import os
import sys
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataPreprocessing:

    def __init__(self, train_file_path, test_file_path, processed_dir,config_path):
        self.train_file_path = train_file_path
        self.test_file_path = test_file_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"Created directory for processed data at {self.processed_dir}")
    
    def preprocess_data(self,df):
        try:
            logger.info("Starting data preprocessing")
            # Drop unnecessary columns
            logger.info("Dropping unnecessary columns")
            df.drop(columns=["Booking_ID"], inplace=True, errors='ignore')

            # Drop Duplicate rows
            logger.info("Dropping duplicate rows")
            df.drop_duplicates(inplace=True)

            # Specifying categorical and numerical columns
            logger.info("Specifying categorical and numerical columns")
            cat_columns = self.config["data_preprocessing"]["categorical_columns"]
            num_columns = self.config["data_preprocessing"]["numerical_columns"]    

            # Label Encoding for categorical columns
            logger.info("Applying Label Encoding for categorical columns")
            le = LabelEncoder()
            mapping_dict = {}
            for col in cat_columns:
                df[col] = le.fit_transform(df[col])
                mapping_dict[col] = dict(zip(le.classes_, le.transform(le.classes_)))
            
            logger.info("Label Mappings are : ")
            for col, mapping in mapping_dict.items():
                logger.info(f"{col}: {mapping}")
            
            logger.info("Skewness of numerical columns before handling imbalance: ")
            skewness_threshold = self.config["data_preprocessing"]["skewness_threshold"]
            skewness = df[num_columns].apply(lambda x: x.skew())
            for col in skewness[skewness > skewness_threshold].index:
                df[col] = np.log1p(df[col])

            return df
                
        except Exception as e:
            logger.error(f"Error occurred during data preprocessing : {e}")
            raise CustomException("Failed to preprocess data", sys)
        
    
    
    def balance_data(self, df):
        try:
            logger.info("Handling imbalance data using SMOTE")
            x = df.drop(columns=["booking_status"])
            y = df["booking_status"]
            smote = SMOTE(random_state=42)
            x_resampled, y_resampled = smote.fit_resample(x, y)
            balanced_df = pd.DataFrame(x_resampled, columns=x.columns)
            balanced_df["booking_status"] = y_resampled
            logger.info("Data balancing completed successfully")
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error occurred during data balancing : {e}")
            raise CustomException("Failed to balance data", sys)



    def feature_selection(self, df):
        try:
            logger.info("Performing feature selection using Random Forest")
            x = df.drop(columns=["booking_status"])
            y = df["booking_status"]
            rf = RandomForestClassifier(random_state=42)
            rf.fit(x, y)
            feature_importances = pd.Series(rf.feature_importances_, index=x.columns)
            num_features_to_select = self.config["data_preprocessing"]["no_of_features_to_select"]
            top_features = feature_importances.sort_values(ascending=False).head(num_features_to_select).index.tolist()
            logger.info(f"Top {num_features_to_select} features selected: {top_features}")
            return top_features
        
        except Exception as e:
            logger.error(f"Error occurred during feature selection : {e}")
            raise CustomException("Failed to perform feature selection", sys)
        

    def save_data(self, df, file_path):
        try:
            logger.info(f"Saving processed data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved successfully to {file_path}")

        except Exception as e:
            logger.error(f"Error occurred while saving data to {file_path} : {e}")
            raise CustomException(f"Failed to save data to {file_path}", sys)

    
    def process(self):
        try:
            # Combining all the steps of data preprocessing in one function to run the data processing pipeline
            logger.info("Loading training and test data from directory's") 
            train_df = load_data(self.train_file_path)
            test_df = load_data(self.test_file_path)

            logger.info("Preprocessing training data")
            train_df = self.preprocess_data(train_df)
            logger.info("Preprocessing test data")
            test_df = self.preprocess_data(test_df) 
            
            logger.info("Balancing training data")
            train_df = self.balance_data(train_df)

            logger.info("Performing feature selection on training data")
            selected_features = self.feature_selection(train_df)
            final_columns = selected_features + ["booking_status"]
            train_df = train_df[final_columns]
            test_df = test_df[final_columns]

            logger.info("Saving processed training and test data to directory's")
            self.save_data(train_df, PROCESSED_TRAIN_FILE_PATH)
            self.save_data(test_df, PROCESSED_TEST_FILE_PATH)
            logger.info("Data processing completed successfully")
                       
        except Exception as e:
            logger.error(f"Error occurred during data processing : {e}")
            raise CustomException("Failed to process data", sys)
        

if __name__ == "__main__":
    data_preprocessing = DataPreprocessing(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    data_preprocessing.process()