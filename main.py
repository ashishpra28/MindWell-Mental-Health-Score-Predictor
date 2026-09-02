# Import Libraries 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field 
from typing import Annotated, Literal 
import pandas as pd 
import joblib 

from langchain_core.messages import HumanMessage 
from graph import workflow

# Load model 
model = joblib.load('artifacts/model.pkl')

# Define fastapi object
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # restrict to your actual frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create pydantic model to validate input data 
class UserInput(BaseModel):
    Age                        : Annotated[int, Field(...,ge=10, le=120, description="Age of the Student")]
    Gender                     : Annotated[Literal['Male','Female'], Field(..., description="Gender of the Student")] 
    Country                    : Annotated[Literal['Other', 'Canada', 'USA', 'India', 'Australia', 'UK', 'Germany', 'Bangladesh', 'Brazil', 'Japan', 'South Korea', 'France', 'Spain', 'Italy', 'Mexico', 'Russia', 'China', 'Sweden', 'Norway', 'Denmark', 'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Portugal', 'Greece', 'Ireland', 'New Zealand', 'Singapore', 'Malaysia', 'Thailand', 'Vietnam', 'Philippines', 'Indonesia', 'Taiwan', 'Hong Kong', 'Turkey', 'Israel', 'UAE', 'Egypt', 'Morocco', 'South Africa', 'Nigeria', 'Kenya', 'Ghana', 'Argentina', 'Chile', 'Colombia', 'Peru', 'Venezuela', 'Ecuador', 'Uruguay', 'Paraguay', 'Bolivia', 'Costa Rica', 'Panama', 'Jamaica', 'Trinidad', 'Bahamas', 'Iceland', 'Finland', 'Poland', 'Romania', 'Hungary', 'Czech Republic', 'Slovakia', 'Croatia', 'Serbia', 'Slovenia', 'Bulgaria', 'Estonia', 'Latvia', 'Lithuania', 'Ukraine', 'Moldova', 'Belarus', 'Kazakhstan', 'Uzbekistan', 'Kyrgyzstan', 'Tajikistan', 'Armenia', 'Georgia', 'Azerbaijan', 'Cyprus', 'Malta', 'Luxembourg', 'Monaco', 'Andorra', 'San Marino', 'Vatican City', 'Liechtenstein', 'Montenegro', 'Albania', 'North Macedonia', 'Kosovo', 'Bosnia', 'Qatar', 'Kuwait', 'Bahrain', 'Oman', 'Jordan', 'Lebanon', 'Iraq', 'Yemen', 'Syria', 'Afghanistan', 'Pakistan', 'Nepal', 'Bhutan', 'Sri Lanka', 'Maldives'], Field(..., description="Country of the Student")]  
    Academic_Level             : Annotated[Literal['Undergraduate', 'Graduate', 'High School'], Field(..., description="Academic level of a Student")]
    Most_Used_Platform         : Annotated[Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter', 'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp', 'WeChat'], Field(..., description="Most used platform by a Student")] 
    Purpose_Of_Use             : Annotated[Literal['Networking', 'Education', 'Entertainment', 'News'], Field(..., description="Purpose of use of the platform by a Student")]
    Avg_Daily_Usage_Hours      : Annotated[float, Field(...,ge=1, le=24, description="Platform average daily uses hour by a Student")] 
    Daily_Unlocks              : Annotated[int, Field(...,gt=0, description="Daily unlocks number of the Student")] 
    Study_Hours                : Annotated[float, Field(...,ge=0, le=24, description="Study hours of the Student")] 
    Physical_Activity_Hours    : Annotated[float, Field(...,ge=0, le=10, description="Physical activity hours of the Student")] 
    Sleep_Hours_Per_Night      : Annotated[float, Field(...,ge=0, le=24, description="Sleep hours of the Student")]
    Stress_Level               : Annotated[Literal['Medium', 'Low', 'Very High', 'High'], Field(..., description="Stress level of the Student")] 

    
# Create home endpoint 
@app.get('/')
def home(): 
    return {
        "message":"Welcome to MindWell - A Mental Health Score Predictor",
        "description":"This API predicts the mental health score by calculating some predifined fields"
    }

# Define top counties 
top_countries = ['Other', 'India', 'USA', 'Canada', 'Australia', 'UK', 'Germany', 'Mexico', 'Turkey', 'France']

# Create a function to get only countries from top_countries 
def group_country(country):
    if country in top_countries:
        return country 
    else: 
        return "Other"

# Create predict endpoint 
@app.post('/predict')
def predict(data: UserInput):

    grouped_country = group_country(data.Country)

    input_df = pd.DataFrame([{
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
    }])

    prediction = model.predict(input_df)[0]

    return {"predicted_mental_health_score": round(float(prediction),2)}


# Create pydantic model to validate Agent input data
class ChatRequest(BaseModel):
    messages: str
    mental_health_score: float
    user_data: dict
    thread_id: str = "1"

# Create chat endpoint 
@app.post("/chat")
def chat(data: ChatRequest):

    def generate():
            for chunk, metadata in workflow.stream({
                "messages"                   :[HumanMessage(content=data.messages)],
                "mental_health_score"        : data.mental_health_score,
                "user_data"                  : data.user_data,
                "question_category"          : "general advice",
                "score_analysis"             : "",
                "advisor_context"            : "",
                "response"                   : ""
                },
                config={"configurable":{'thread_id':data.thread_id}},stream_mode="messages"):
                            if chunk.content:
                                yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")