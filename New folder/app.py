import streamlit as st
import joblib

model = joblib.load("model.pkl")

st.title("Airline Satisfaction Prediction")

# Dropdown Inputs
gender = st.selectbox("Gender", ["Male", "Female"])
customer_type = st.selectbox("Customer Type", ["Loyal Customer", "disloyal Customer"])
travel_type = st.selectbox("Type of Travel", ["Business travel", "Personal Travel"])
travel_class = st.selectbox("Class", ["Business", "Eco", "Eco Plus"])

# Numeric Inputs
Age = st.number_input("Age")
Flight_Distance = st.number_input("Flight Distance")

Inflight_wifi_service = st.slider("Inflight wifi service", 0, 5)
Departure_Arrival_time_convenient = st.slider("Departure/Arrival time convenient", 0, 5)
Ease_of_Online_booking = st.slider("Ease of Online booking", 0, 5)
Gate_location = st.slider("Gate location", 0, 5)
Food_and_drink = st.slider("Food and drink", 0, 5)
Online_boarding = st.slider("Online boarding", 0, 5)
Seat_comfort = st.slider("Seat comfort", 0, 5)
Inflight_entertainment = st.slider("Inflight entertainment", 0, 5)
On_board_service = st.slider("On-board service", 0, 5)
Leg_room_service = st.slider("Leg room service", 0, 5)
Baggage_handling = st.slider("Baggage handling", 0, 5)
Checkin_service = st.slider("Checkin service", 0, 5)
Inflight_service = st.slider("Inflight service", 0, 5)
Cleanliness = st.slider("Cleanliness", 0, 5)

Departure_Delay = st.number_input("Departure Delay in Minutes")
Arrival_Delay = st.number_input("Arrival Delay in Minutes")

# Encoding
Gender = 1 if gender == "Male" else 0

Customer_Type = 0 if customer_type == "Loyal Customer" else 1

Type_of_Travel = 0 if travel_type == "Business travel" else 1

Class = {
    "Business": 0,
    "Eco": 1,
    "Eco Plus": 2
}[travel_class]

if st.button("Predict"):

    data = [[
        Gender,
        Customer_Type,
        Age,
        Type_of_Travel,
        Class,
        Flight_Distance,
        Inflight_wifi_service,
        Departure_Arrival_time_convenient,
        Ease_of_Online_booking,
        Gate_location,
        Food_and_drink,
        Online_boarding,
        Seat_comfort,
        Inflight_entertainment,
        On_board_service,
        Leg_room_service,
        Baggage_handling,
        Checkin_service,
        Inflight_service,
        Cleanliness,
        Departure_Delay,
        Arrival_Delay
    ]]

    pred = model.predict(data)

    if pred[0] == 1:
        st.success("Satisfied Passenger")
    else:
        st.error("Neutral or Dissatisfied Passenger")