# Import libraries
import pandas as pd 
import joblib 

# Load model 
model = joblib.load('artifacts/model.pkl')

# Define model version
MODEL_VERSION = "1.0.0"

# Create function for prediction
def predict_score(user_input:dict): 
    # take input
    input_df = pd.DataFrame([user_input])

    # prediction
    output = model.predict(input_df)[0]

    # return output 
    return output