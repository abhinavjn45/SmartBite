# SmartBite AI – Simple Crowd Flow & Wait-Time Estimation System

SmartBite AI is a real-time smart dashboard application that estimates crowd density, wait time, and recommends alternative canteens inside CHRIST University campus using simple rule-based logic.

## Folder Structure

```
SmartBite-AI/
├── app.py                     # Main Streamlit application
├── data/
│   └── canteen_data.csv       # Simulated campus canteen data
├── utils/
│   ├── data_simulator.py      # Script to generate realistic data
│   ├── wait_time.py           # Logic for estimating wait times
│   ├── recommendation.py      # Smart recommendation engine logic
│   └── rule_engine.py         # Rule-based crowd estimation logic
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Features

1. **Live Dashboard**: Auto-refreshing module simulating real-time crowding and wait times.
2. **Map View**: Interactive Folium campus map showing active crowd levels.
3. **Predict Crowd**: Rule-based prediction tool for customized scenarios.
4. **Insights & Analytics**: Data visualizations for historical trends (hourly, weekly, weather patterns).
5. **Smart Recommendation**: Suggests alternative canteens with lowest wait times and distances when your selected canteen is crowded.

## How to Run Locally

1. **Clone the repository** (or navigate to the project directory)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Generate Data**: (Optional if already generated)
   ```bash
   python utils/data_simulator.py
   ```
4. **Run Streamlit App**:
   ```bash
   streamlit run app.py
   ```