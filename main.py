# Import Libraries 
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field 
from typing import List, Optional, Annotated, Literal 
import pandas as pd 
import joblib 

# Load model 
model = joblib.load('artifacts/model.pkl')

# Define fastapi object
app = FastAPI() 

# Create home endpoint 
@app.get('/')
def home(): 
    return {
        "message":"Welcome to MindWell - A Mental Health Score Predictor",
        "description":"This API predicts the mental health score by calculating some predifined fields"
    }