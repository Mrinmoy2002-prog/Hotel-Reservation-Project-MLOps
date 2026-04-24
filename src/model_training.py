############ File for model training and experiment tracking using mlflow. This file will contain the code for training the model and tracking the experiments using mlflow  #######################

import os
import sys
from xml.parsers.expat import model
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import *
from src.logger import get_logger
from src.custom_exception import CustomException    
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint

logger = get_logger(__name__)


class ModelTraining:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.param_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS


    def load_and_split_data(self):
        try:
            logger.info("Loading the train and test data")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            x_train = train_df.drop(columns=["booking_status"], axis=1)
            y_train = train_df["booking_status"]

            x_test = test_df.drop(columns=["booking_status"], axis=1)
            y_test = test_df["booking_status"]

            logger.info("Data loaded and split into features and target variable successfully")
            return x_train, y_train, x_test, y_test
        
        except Exception as e:
            logger.error(f"Error while loading and splitting the data : {e}")
            raise CustomException("Failed to load and split the data", sys)
        

    def train_lgm(self, x_train, y_train):
        try:
            logger.info("Starting the training of LightGBM model")
            lgm = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])
            random_search = RandomizedSearchCV(estimator=lgm, 
                                               param_distributions=self.param_dist,
                                               n_iter=self.random_search_params["n_iter"], 
                                               cv=self.random_search_params["cv"], 
                                               verbose=2, 
                                               random_state=self.random_search_params["random_state"], 
                                               n_jobs=self.random_search_params["n_jobs"])
            logger.info("Starting RandomizedSearchCV for LightGBM model")
            random_search.fit(x_train, y_train)
            logger.info("Starting hyperparmater tuning using RandomizedSearchCV for LightGBM model")
            best_params = random_search.best_params_
            logger.info(f"Best parameters found by RandomizedSearchCV: {best_params}")
            best_model = random_search.best_estimator_
            logger.info("Model trained successfully with best parameters found by RandomizedSearchCV")
            return best_model
        
        except Exception as e:
            logger.error(f"Error while training the LightGBM model : {e}")
            raise CustomException("Failed to train the LightGBM model", sys)
        

    
    def evaluate_model(self, model, x_test, y_test):
        try:
            logger.info("Starting the evaluation of the model")
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            logger.info(f"Model evaluation completed successfully with Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")
            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }
        
        except Exception as e:
            logger.error(f"Error while evaluating the model : {e}")
            raise CustomException("Failed to evaluate the model", sys)
        

    
    def save_model(self, model):
        try:
            logger.info(f"Saving the model to {self.model_output_path}")
            if not os.path.exists(os.path.dirname(self.model_output_path)):
                os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
                joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved successfully to {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error while saving the model : {e}")
            raise CustomException("Failed to save the model", sys)
        


    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting the model training process")

                logger.info("Starting ML Flow experiment tracking for model training")

                logger.info("Logging the training and test data for model training")
                mlflow.log_artifact(self.train_path,artifact_path="train_data")
                mlflow.log_artifact(self.test_path,artifact_path="test_data")

                x_train, y_train, x_test, y_test = self.load_and_split_data()
                model = self.train_lgm(x_train, y_train)
                evaluation_metrics = self.evaluate_model(model, x_test, y_test)
                logger.info(f"Model evaluation metrics: {evaluation_metrics}")
                self.save_model(model)

                logger.info("Logging the model and evaluation metrics to ML Flow")
                mlflow.log_artifact(self.model_output_path, artifact_path="model")

                logger.info("Logging the evaluation metrics and model parameters to ML Flow")
                mlflow.log_metrics(evaluation_metrics)
                mlflow.log_params(model.get_params())
            logger.info("Model training process completed successfully")
        except Exception as e:
            logger.error(f"Error while running the model training process : {e}")
            raise CustomException("Failed to run the model training process", sys)
        

    
if __name__ == "__main__":
    model_training = ModelTraining(train_path=PROCESSED_TRAIN_FILE_PATH, 
                                   test_path=PROCESSED_TEST_FILE_PATH, 
                                   model_output_path=MODEL_OUTPUT_PATH)
    model_training.run()