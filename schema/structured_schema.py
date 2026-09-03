from pydantic import BaseModel, Field 
from typing import Annotated, Literal 

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

# Define top counties 
top_countries = ['Other', 'India', 'USA', 'Canada', 'Australia', 'UK', 'Germany', 'Mexico', 'Turkey', 'France']

# Create a function to get only countries from top_countries 
def group_country(country):
    if country in top_countries:
        return country 
    else: 
        return "Other"

# Create pydantic model to validate Agent input data
class ChatInput(BaseModel):
    messages: str
    mental_health_score: float
    user_data: dict
    thread_id: str = "1"