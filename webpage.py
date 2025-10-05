import streamlit as st
import pandas as pd
import joblib
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, time


# Load model in the function
@st.cache_resource
def load_model():
    return joblib.load("xgb_model.joblib")

xgb_pipeline = load_model()


# CSS for app
st.markdown("""
    <style>
    /* Title */
    h1 {
        color: #4F46E5;
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #475569;
        font-size: 18px;
        margin-bottom: 30px;
    }
    /* Section headers */
    h2, h3 {
        color: #3730A3;
        border-left: 5px solid #4F46E5;
        padding-left: 10px;
        margin-top: 25px;
    }
    /* Inputs */
    .stNumberInput, .stSelectbox {
        background-color: #EEF2FF !important;
        border-radius: 10px !important;
    }
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        color: white;
        border-radius: 8px;
        font-size: 18px;
        height: 3em;
        width: 100%;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #6366F1, #22D3EE);
        transform: scale(1.03);
    }
    /* Pop-out card animation */
    @keyframes popout {
        0% {transform: scale(0.8); opacity: 0;}
        100% {transform: scale(1); opacity: 1;}
    }
    .result-card {
        background: linear-gradient(135deg, #4F46E5, #06B6D4);
        color: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        font-size: 22px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-top: 25px;
        animation: popout 0.5s ease-out;
    }
    .time-text {
        font-size: 36px;
        font-weight: 800;
        margin-top: 10px;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)


# --- Title ---
st.markdown("<h1>🚚 Smart Delivery Time Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Predict your delivery time with data-driven precision</p>", unsafe_allow_html=True)



# function to calculate distance in km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# function to calculate time difference 
def calculate_time_to_pickup(order_date, order_time, pickup_time):
    order_time_full = pd.Timestamp.combine(order_date, order_time)
    pickup_time_full = pd.Timestamp.combine(order_date, pickup_time)

    # If pickup earlier than order, add one day
    if pickup_time_full < order_time_full:
        pickup_time_full += pd.Timedelta(days=1)

    time_to_pickup_min = (pickup_time_full - order_time_full).total_seconds() / 60
    return time_to_pickup_min



# --- Inputs ---
st.header("Enter Delivery Details")

col1, col2 = st.columns(2)
Agent_Age = col1.number_input("Agent Age", min_value=15, max_value=50, value=25)
Agent_Rating = col2.number_input("Agent Rating", min_value=1.0, max_value=5.0, value=3.5)


col3,col4=st.columns(2)
Weather = col3.selectbox("Weather Condition", ['Sunny', 'Stormy', 'Sandstorms', 'Cloudy', 'Fog', 'Windy'])
Traffic = col4.selectbox("Traffic Condition",['High ', 'Jam ', 'Low ', 'Medium '])
col5,col6=st.columns(2)
Vehicle = col5.selectbox("Vehicle Type", ['motorcycle ', 'scooter ', 'van'])
Area = col6.selectbox("Delivery Area", ['Urban ', 'Metropolitian ', 'Semi-Urban ', 'Other'])
Category = st.selectbox("Order Category", ['Clothing', 'Electronics', 'Sports', 'Cosmetics', 'Toys', 'Snacks',
                        'Shoes', 'Apparel', 'Jewelry', 'Outdoors', 'Grocery', 'Books',
                        'Kitchen', 'Home', 'Pet Supplies', 'Skincare'])


st.subheader("Order & Pickup Details")
col7, col8 = st.columns(2)
Order_Date = col7.date_input("Order Date", datetime.now().date())
Order_Time = col7.time_input("Order Time", time(10, 0))
Pickup_Time = col8.time_input("Pickup Time", time(10, 30))



st.subheader("Location Details")
col5, col6 = st.columns(2)
Store_Latitude = col5.number_input("Store Latitude", value=19.0760)
Store_Longitude = col5.number_input("Store Longitude", value=72.8777)
Drop_Latitude = col6.number_input("Drop Latitude", value=19.2183)
Drop_Longitude = col6.number_input("Drop Longitude", value=72.9781)


# Calculated features 
Distance_km = haversine(Store_Latitude, Store_Longitude, Drop_Latitude, Drop_Longitude)
Time_to_Pickup_Min = calculate_time_to_pickup(Order_Date, Order_Time, Pickup_Time)

st.markdown(f"**Calculated Distance:** {Distance_km:.2f} km")
st.markdown(f"**Time to Pickup:** {Time_to_Pickup_Min:.2f} minutes")

# input dataframe
input_df = pd.DataFrame({
    "Agent_Age": [Agent_Age],
    "Agent_Rating": [Agent_Rating],
    "Distance_km": [Distance_km],
    "Time_to_Pickup_Min": [Time_to_Pickup_Min],
    "Weather": [Weather],
    "Traffic": [Traffic],
    "Vehicle": [Vehicle],
    "Area": [Area],
    "Category": [Category]
})


# Model prediction
if st.button("Predict Delivery Time"):
    with st.spinner("Predicting delivery time..."):
        from time import sleep
        sleep(1.5)
        predicted_time = xgb_pipeline.predict(input_df)[0]

    # Format the result
    if predicted_time < 60:
        delivery_display = f"{int(predicted_time)} minutes"
    elif predicted_time < 1440:
        hours = int(predicted_time // 60)
        minutes = int(predicted_time % 60)
        delivery_display = f"{hours} hours {minutes} minutes"
    else:
        days = predicted_time / 1440
        delivery_display = f"{days:.1f} days"

    # Display popout card
    st.markdown(
        f"""
        <div class="result-card">
            Predicted Delivery Time
            <div class="time-text">{delivery_display}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


