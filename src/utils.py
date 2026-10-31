import os, sys
import pandas as pd
import numpy as np

from src.logger import logging
from src.exception import CustomException
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




