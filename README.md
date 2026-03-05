# SmartBite AI – Intelligent Crowd Flow & Wait-Time Prediction System

SmartBite AI is a real-time smart dashboard application that predicts crowd density, wait time, and recommends alternative canteens inside CHRIST University campus.

## Folder Structure

```
SmartBite-AI/
├── app.py                     # Main Streamlit application
├── data/
│   └── canteen_data.csv       # Simulated campus canteen data
├── models/
│   ├── ml_pipeline.py         # ML training script
│   ├── rf_regressor.pkl       # Saved RandomForest Regressor
│   ├── rf_classifier.pkl      # Saved RandomForest Classifier
│   ├── encoders.pkl           # Saved Label Encoders
│   └── metrics.pkl            # Model evaluation metrics
├── utils/
│   ├── data_simulator.py      # Script to generate realistic data
│   ├── wait_time.py           # Logic for estimating wait times
│   └── recommendation.py      # Smart recommendation engine logic
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Features

1. **Live Dashboard**: Auto-refreshing module simulating real-time crowding and wait times.
2. **Map View**: Interactive Folium campus map showing active crowd levels.
3. **Predict Crowd**: ML-driven prediction tool for customized scenarios.
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
4. **Train Models**:
   ```bash
   python models/ml_pipeline.py
   ```
5. **Run Streamlit App**:
   ```bash
   streamlit run app.py
   ```

## Deployment on Streamlit Cloud

1. Push this folder to a GitHub repository.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create a new app, select your repository, branch, and entry point (`app.py`).
4. Click **Deploy**. The platform will automatically install packages from `requirements.txt`.
