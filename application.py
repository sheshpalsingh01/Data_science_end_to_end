import os, sys
import pickle
from flask import Flask, request, jsonify,render_template
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.pipeline.predict_pipeline import PredictPipeline,CustomData

from src.utils import load_object

app = Flask(__name__)

# create route for home page
@app.route("/")
def index():
    return render_template('index.html')


# create route for prediction
@app.route("/predict",methods=['GET','POST'])
def predict_datapoint():
    try:
        if request.method=="GET":
            return render_template('home.html') # Provide a path to the HTML file
        else:
            data = CustomData(
                gender=request.form.get("gender"),
                race_ethnicity=request.form.get("race_ethnicity"),
                parental_level_of_education=request.form.get("parental_level_of_education"),
                lunch=request.form.get("lunch"),
                test_preparation_course=request.form.get("test_preparation_course"),
                reading_score=int(request.form.get("reading_score")),
                writing_score=int(request.form.get("writing_score"))
            )
            pred_df=data.get_data_as_frame()
            
            predict_pipeline=PredictPipeline()
            result=predict_pipeline.predict(pred_df)
            
            return render_template("home.html",result=result)

           
    except Exception as e:
        raise CustomException(e, sys)
        

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8082)