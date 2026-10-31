import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformationConfig,DataTransformation
from src.components.model_training import ModelTrainerConfig,ModelTrainer


@dataclass
class DataIngestionConfig:
    train_data_path :str = os.path.join("artifacts", "train.csv")
    test_data_path :str = os.path.join("artifacts", "test.csv")
    raw_data_path :str = os.path.join("artifacts", "raw.csv")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.ingestion_config = data_ingestion_config


    def initiate_data_ingestion(self):
        logging.info("Data Ingestion start..........")
        try:
            dataset = pd.read_csv("notebook/data/stud.csv")
            logging.info("Read the dataset.......... ")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            dataset.to_csv(self.ingestion_config.raw_data_path, index=False)

            logging.info("Train test split............")
            train_set, test_set = train_test_split(dataset, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)

            logging.info("Ingestion of data is completed")

            return (
                self.ingestion_config.raw_data_path,
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)

    
if __name__ =="__main__":

    data_ingestion_config = DataIngestionConfig()
    data_ingestion = DataIngestion(data_ingestion_config)
    _,train_data,test_data = data_ingestion.initiate_data_ingestion()


    data_transformation_config = DataTransformationConfig()
    data_transformation = DataTransformation(data_transformation_config)
    train_arr,test_arr,preprocessor_obj = data_transformation.initiate_data_transformation(train_data,test_data)

    model_trainer_config = ModelTrainerConfig()
    model_trainer = ModelTrainer(model_trainer_config)
    model_trainer.initiate_model_training(train_arr,test_arr,preprocessor_obj)
