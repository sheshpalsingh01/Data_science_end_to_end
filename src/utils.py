import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pandas as pd
import numpy as np

from src.logger import logging
from src.exception import CustomException
from sklearn.metrics import r2_score,accuracy_score
import dill

def save_object(file_path: str, obj):
    """
    This function is used to save the object
    Args:
        file_path (str): The path to save the object
        obj (object): The object to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info(f"Object saved at {file_path}")

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            obj=dill.load(file_obj)
            logging.info(f"Object loaded from {file_path}")
            return obj
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_model(x_train,y_train,x_test,y_test,models:dict):
    try:
        model_report:dict= {}
        for i in range(len(list(models.keys()))):
            model=list(models.values())[i]
            model.fit(x_train,y_train)
            x_train_pred =model.predict(x_train)
            y_test_pred=model.predict(x_test)
            test_model_score=r2_score(y_test,y_test_pred)
            train_model_score=r2_score(y_train,x_train_pred)
            
            model_report[list(models.keys())[i]]=test_model_score
        return model_report    
    except Exception as e:
        raise CustomException(e, sys)