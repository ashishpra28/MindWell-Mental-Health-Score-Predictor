# Import Libraries 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schema.structured_schema import UserInput, ChatInput, group_country
from src.predict import model, MODEL_VERSION, predict_score
from src.chat import generate_response

from langchain_core.messages import HumanMessage 
from agent import workflow


# Define fastapi object
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
# Create home endpoint 
@app.get('/')
def home(): 
    return {
        "message":"Welcome to MindWell - A Mental Health Score Predictor",
        "description":"This API predicts the mental health score by calculating some predifined fields"
    }

# Create health endpoint 
@app.get('/health')
def health_check(): 
     return {
          "status" : "OK",
          "version": MODEL_VERSION,
          "model_loaded": model is not None
     }


# Create predict endpoint 
@app.post('/predict')
def predict(data: UserInput):

    grouped_country = group_country(data.Country)

    user_input = {
        'Age'                       : data.Age,
        'Gender'                    : data.Gender, 
        'Academic_Level'            : data.Academic_Level, 
        'Most_Used_Platform'        : data.Most_Used_Platform,
        'Purpose_Of_Use'            : data.Purpose_Of_Use,
        'Avg_Daily_Usage_Hours'     : data.Avg_Daily_Usage_Hours,
        'Daily_Unlocks'             : data.Daily_Unlocks,
        'Study_Hours'               : data.Study_Hours,
        'Physical_Activity_Hours'   : data.Physical_Activity_Hours,
        'Sleep_Hours_Per_Night'     : data.Sleep_Hours_Per_Night,
        'Stress_Level'              : data.Stress_Level,
        'Grouped_country'           : grouped_country
    }

    try: 
        prediction = predict_score(user_input=user_input)

        return {"predicted_mental_health_score": round(float(prediction),2)}
    
    except Exception as e:
        return str(e)

# Create chat endpoint 
@app.post("/chat")
def chat(data: ChatInput):

    try: 
        return StreamingResponse(generate_response(data), media_type="text/plain")
    except Exception as e: 
        return str(e)