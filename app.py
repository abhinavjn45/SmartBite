import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import os
import time
from datetime import datetime
from utils.wait_time import estimate_wait_time
from utils.recommendation import recommend_alternatives, CANTEEN_LOCATIONS
from utils.data_simulator import CANTEENS, WEATHER_CONDITIONS
from utils.rule_engine import predict_crowd

# --- Config & Setup ---
st.set_page_config(page_title="SmartBite AI", page_icon="🍔", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'canteen_data.csv')

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        return df
    return pd.DataFrame()

df = load_data()

# --- Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3448/3448057.png", width=100)
st.sidebar.title("SmartBite AI")
st.sidebar.caption("Simple Crowd flow & Wait-Time Estimation")

menu = ["Home", "Live Dashboard", "Map View", "Predict Crowd", "Insights & Analytics"]
choice = st.sidebar.radio("Navigation", menu)

# Helper function for colors
def get_color_for_level(level):
    return {"Low": "green", "Medium": "orange", "High": "red", "Critical surge": "darkred"}.get(level, "gray")

def get_hex_color(level):
    return {"Low": "#28a745", "Medium": "#ffc107", "High": "#fd7e14", "Critical surge": "#dc3545"}.get(level, "#6c757d")

# --- Views ---

if choice == "Home":
    st.title("Welcome to SmartBite AI")
    st.markdown("""
    **SmartBite AI** is an intelligent dashboard system designed to optimize the dining experience across CHRIST University campus canteens.
    
    ### Features:
    * **Live Dashboard:** Monitor real-time crowd predictions and wait times.
    * **Map View:** Geo-visualization of current campus canteen crowding.
    * **Predict Crowd:** Use a simple rule-based engine to estimate crowd density using weather and event inputs.
    * **Insights & Analytics:** Deep dive into historical crowd patterns.
    """)
    if not df.empty:
        st.info(f"System uses **{len(df)}** historical records.")
        st.metric("Historical Records", len(df))

elif choice == "Live Dashboard":
    st.title("Live Campus Dashboard")
    st.markdown("Auto-refreshing predictions (Simulated real-time)")

    now = datetime.now()
    hour = now.hour
    minute = now.minute
    day_of_week = now.weekday()
    temp = 26 + (now.day % 6)
    weather = WEATHER_CONDITIONS[now.day % len(WEATHER_CONDITIONS)]
    exam_week = 0
    event_day = 1 if now.weekday() == 4 else 0

    st.write(f"**Current Time:** {now.strftime('%H:%M')} | **Weather:** {weather} | **Temp:** {temp}°C")

    live_predictions = []
    for canteen in CANTEENS:
        pred_count, pred_level = predict_crowd(
            canteen_name=canteen,
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            temperature=temp,
            weather=weather,
            exam_week=exam_week,
            event_day=event_day,
            holiday=0,
        )
        live_predictions.append({
            "canteen": canteen,
            "crowd_count": pred_count,
            "level": pred_level
        })

    cols = st.columns(len(CANTEENS))
    for i, pred in enumerate(live_predictions):
        with cols[i]:
            st.markdown(f"### {pred['canteen']}")
            wait = estimate_wait_time(pred['canteen'], pred['crowd_count'])
            color = get_hex_color(pred['level'])
            st.markdown(f"<h1 style='color: {color};'>{pred['crowd_count']} pax</h1>", unsafe_allow_html=True)
            st.markdown(f"**Level:** {pred['level']}")
            st.markdown(f"**Wait time:** {wait} mins")

    st.divider()
    st.subheader("Smart Recommendation Engine")
    selected_canteen = st.selectbox("Select your preferred canteen to check alternatives:", CANTEENS)

    sel_pred = next(p for p in live_predictions if p['canteen'] == selected_canteen)
    if sel_pred['level'] in ["High", "Critical surge"]:
        st.warning(f"⚠️ {selected_canteen} is currently experiencing a {sel_pred['level']} crowd.")
        alts = recommend_alternatives(selected_canteen, live_predictions)
        st.markdown("#### Recommended Alternatives:")
        for alt in alts[:2]:
            st.success(f"🥘 **{alt['canteen']}** - {alt['level']} Crowd | Est. wait: {alt['wait_time']} mins | Distance score: {alt['distance_score']}")
    else:
        st.success(f"✅ {selected_canteen} is a good choice right now ({sel_pred['level']} crowd)!")

    time.sleep(30)
    st.rerun()

elif choice == "Map View":
    st.title("Campus Canteen Map")

    now = datetime.now()
    weather = WEATHER_CONDITIONS[now.day % len(WEATHER_CONDITIONS)]
    temp = 26 + (now.day % 6)

    live_preds = {}
    for canteen in CANTEENS:
        count, level = predict_crowd(
            canteen_name=canteen,
            day_of_week=now.weekday(),
            hour=now.hour,
            minute=now.minute,
            temperature=temp,
            weather=weather,
            exam_week=0,
            event_day=1 if now.weekday() == 4 else 0,
            holiday=0,
        )
        live_preds[canteen] = {"count": count, "level": level}

    m = folium.Map(location=[12.934335, 77.605802], zoom_start=18)

    for canteen, coords in CANTEEN_LOCATIONS.items():
        level = live_preds[canteen]["level"]
        count = live_preds[canteen]["count"]
        wait = estimate_wait_time(canteen, count)

        color = get_color_for_level(level)

        folium.Marker(
            location=coords,
            popup=f"<b>{canteen}</b><br>Crowd: {count}<br>Wait: {wait} min",
            tooltip=f"{canteen} ({level})",
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

        folium.Circle(
            radius=15 + (count * 0.5),
            location=coords,
            color=color,
            fill=True,
        ).add_to(m)

    st_folium(m, width=900, height=500)

elif choice == "Predict Crowd":
    st.title("Crowd Predictor")

    col1, col2 = st.columns(2)
    with col1:
        sel_canteen = st.selectbox("Canteen", CANTEENS)
        sel_day = st.selectbox("Day of Week", list(range(7)), format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])
        sel_hour = st.slider("Hour of Day (8 to 18)", 8, 18, 12)

    with col2:
        sel_temp = st.slider("Temperature (°C)", 20, 40, 25)
        sel_weather = st.selectbox("Weather", WEATHER_CONDITIONS)
        sel_exam = st.checkbox("Exam Week")
        sel_event = st.checkbox("Campus Event")
        sel_holiday = st.checkbox("Campus Holiday")

    if st.button("Predict 🚀"):
        pred_count, pred_level = predict_crowd(
            canteen_name=sel_canteen,
            day_of_week=sel_day,
            hour=sel_hour,
            temperature=sel_temp,
            weather=sel_weather,
            exam_week=int(sel_exam),
            event_day=int(sel_event),
            holiday=int(sel_holiday),
        )
        wait = estimate_wait_time(sel_canteen, pred_count)

        st.success("Prediction Complete!")

        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Crowd Count", pred_count)
        m2.metric("Crowd Risk Level", pred_level)
        m3.metric("Estimated Wait Time", f"{wait} mins")

elif choice == "Insights & Analytics":
    st.title("Insights & Analytics Dashboard")
    
    if df.empty:
        st.error("Data.csv not found!")
    else:
        st.markdown("Explore historical trends and patterns of campus dining.")
        
        # Hourly Trend
        st.subheader("Hourly Crowd Trend")
        hourly_avg = df.groupby(['hour', 'canteen_name'])['crowd_count'].mean().reset_index()
        fig1 = px.line(hourly_avg, x='hour', y='crowd_count', color='canteen_name', 
                       title='Average Crowd Count by Hour', markers=True)
        st.plotly_chart(fig1, width="stretch")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Weekly Pattern
            st.subheader("Weekly Pattern")
            weekly_avg = df.groupby('day_of_week')['crowd_count'].mean().reset_index()
            day_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
            weekly_avg['day_label'] = weekly_avg['day_of_week'].map(day_map)
            fig2 = px.bar(weekly_avg, x='day_label', y='crowd_count', title='Average Daily Crowd')
            st.plotly_chart(fig2, width="stretch")
            
            # Weather Impact
            st.subheader("Weather Impact")
            weather_avg = df.groupby('weather_condition')['crowd_count'].mean().reset_index()
            fig4 = px.pie(weather_avg, names='weather_condition', values='crowd_count', title='Crowd Distribution by Weather')
            st.plotly_chart(fig4, width="stretch")

        with col2:
            # Exam vs Non-exam
            st.subheader("Exam vs Non-Exam Weeks")
            exam_avg = df.groupby(['exam_week', 'canteen_name'])['crowd_count'].mean().reset_index()
            exam_avg['Period'] = exam_avg['exam_week'].map({0: 'Regular Week', 1: 'Exam Week'})
            fig3 = px.bar(exam_avg, x='canteen_name', y='crowd_count', color='Period', barmode='group', title='Impact of Exams on Canteens')
            st.plotly_chart(fig3, width="stretch")
