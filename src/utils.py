import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pandas as pd
import numpy as np

from src.logger import logging
from src.exception import CustomException
from sklearn.metrics import r2_score,accuracy_score
from sklearn.model_selection import GridSearchCV
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

def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param.get(list(models.keys())[i], {}) if param else {}
            if para:
                gs = GridSearchCV(model,para,cv=3)
                gs.fit(X_train,y_train)
                model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
    

