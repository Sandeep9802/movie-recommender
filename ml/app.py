import streamlit as st
import requests

st.title("AI Addiction Predictor")

emotion = st.slider(
    "Emotional Content Effect",
    0.0, 100.0
)

high_ai = st.slider(
    "AI Recommendation Control",
    0.0, 100.0
)

ai_score = st.slider(
    "Overall AI Impact",
    0.0, 100.0
)

bubble = st.slider(
    "Same Content Repetition",
    0.0, 100.0
)

if st.button("Predict"):

    payload = {
        "emotional_manipulation_index": emotion,
        "high_ai_influence": high_ai,
        "ai_influence_score": ai_score,
        "filter_bubble_score": bubble
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    result = response.json()

    st.success(
        f"Predicted Addiction Score: {result['prediction']:.2f}"
    )