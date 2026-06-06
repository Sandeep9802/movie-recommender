import streamlit as st
import joblib

# ------------------------
# Page Config
# ------------------------
st.set_page_config(
    page_title="Emotion Detection App",
    page_icon="🎭",
    layout="centered"
)

# ------------------------
# Load Model
# ------------------------
model = joblib.load("emotion_model.pkl")
tfidf = joblib.load("tfidf.pkl")

# ------------------------
# Emotion Mapping
# ------------------------
emotion_map = {
    0: "😢 Sadness",
    1: "😊 Joy",
    2: "❤️ Love",
    3: "😡 Anger",
    4: "😨 Fear",
    5: "😲 Surprise"
}

# ------------------------
# Custom CSS
# ------------------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

.stTextArea textarea {
    font-size: 18px;
    border-radius: 10px;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# Header
# ------------------------
st.markdown(
    '<div class="title">🎭 Emotion Detection App</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Detect emotions from text using Machine Learning</div>',
    unsafe_allow_html=True
)

# ------------------------
# Input
# ------------------------
text = st.text_area(
    "✍️ Enter Text",
    height=180,
    placeholder="Example: I am feeling very happy today!"
)

# ------------------------
# Predict Button
# ------------------------
if st.button("🔍 Detect Emotion", use_container_width=True):

    if text.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:

        vector = tfidf.transform([text])
        pred = model.predict(vector)[0]

        emotion = emotion_map.get(pred, str(pred))

        # Emotion Colors
        emotion_colors = {
            "😢 Sadness": "#3498db",
            "😊 Joy": "#2ecc71",
            "❤️ Love": "#e91e63",
            "😡 Anger": "#e74c3c",
            "😨 Fear": "#f39c12",
            "😲 Surprise": "#9b59b6"
        }

        color = emotion_colors.get(emotion, "#34495e")

        st.markdown(
            f"""
            <div style="
                background:{color};
                padding:25px;
                border-radius:15px;
                text-align:center;
                font-size:30px;
                font-weight:bold;
                color:white;
                margin-top:20px;
                box-shadow:0px 4px 15px rgba(0,0,0,0.3);
            ">
                Predicted Emotion <br><br>
                {emotion}
            </div>
            """,
            unsafe_allow_html=True
        )

# ------------------------
# Footer
# ------------------------
st.markdown("---")
st.markdown(
    '<div class="footer">❤️ Built with Machine Learning & Streamlit</div>',
    unsafe_allow_html=True
)