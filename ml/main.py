from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

model = joblib.load("model.pkl")

class UserInput(BaseModel):
    emotional_manipulation_index: float
    high_ai_influence: float
    ai_influence_score: float
    filter_bubble_score: float

@app.get("/")
def home():
    return {"message": "AI Addiction Predictor API"}

@app.post("/predict")
def predict(data: UserInput):

    input_df = pd.DataFrame([{
        "emotional_manipulation_index": data.emotional_manipulation_index,
        "high_ai_influence": data.high_ai_influence,
        "ai_influence_score": data.ai_influence_score,
        "filter_bubble_score": data.filter_bubble_score
    }])

    prediction = model.predict(input_df)[0]

    return {
        "prediction": float(prediction)
    }
