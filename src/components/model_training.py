import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object, evaluate_model, save_object
from dataclasses import dataclass

from sklearn.metrics import accuracy_score, classification_report, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor,GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import RandomizedSearchCV,train_test_split
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import warnings

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig):
        self.model_trainer_config=model_trainer_config
    
    def initiate_model_training(self,train_arr,test_arr,preprocessor_obj_path:str):        
        try:
            logging.info("Training")
            x_train, y_train, x_test, y_test = (train_arr[:,:-1], 
                                                train_arr[:,-1], 
                                                test_arr[:,:-1], 
                                                test_arr[:,-1])
            
            models={
                "RandomForestRegressor":RandomForestRegressor(),
                "XGBRegressor":XGBRegressor(),
                "CatBoostRegressor":CatBoostRegressor(),
                "DecisionTreeRegressor":DecisionTreeRegressor(),
                "GradientBoostingRegressor":GradientBoostingRegressor(),
                "AdaBoostRegressor":AdaBoostRegressor(),
                "KNeighborsRegressor":KNeighborsRegressor(),
                "SVR":SVR(),
                "LinearRegression":LinearRegression(),
                "Ridge":Ridge(),
                "Lasso":Lasso()
            }

            model_report:dict= evaluate_model(
                x_train=x_train,y_train=y_train,
                x_test=x_test,y_test=y_test,
                models=models
            )

            # Pick model with best (highest) score — assumes higher is better (r2/accuracy)
            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = models[best_model_name]

            # Use a metric-aware threshold, not a magic 0.6
            MIN_ACCEPTABLE_SCORE = 0.6   # only valid for r2 / accuracy / f1

            if best_model_score < MIN_ACCEPTABLE_SCORE:
                raise CustomException(
                    f"No acceptable model found (best={best_model_score:.4f} < {MIN_ACCEPTABLE_SCORE})",
                    sys
                )

            logging.info(f"Best model name found on both train and test data")

            # preprocessing_obj=load_object(preprocessor_obj_path)

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(x_test)

            r2_scores= r2_score(y_test,predicted)

            logging.info(f"R2 Score: {r2_scores}")
            return r2_scores
            
                      
        except Exception as e:
            raise CustomException(e,sys)

    
