import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def prepare_data(df):
    """
    Preprocess data for ML training.
    """
    # Extract hour from timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    
    # Create crowd_level target for classifier
    def categorize_crowd(count):
        if count <= 20:
            return 'Low'
        elif count <= 50:
            return 'Medium'
        elif count <= 80:
            return 'High'
        else:
            return 'Critical surge'
            
    df['crowd_level'] = df['crowd_count'].apply(categorize_crowd)
    
    # Encode categorical variables
    le_canteen = LabelEncoder()
    le_weather = LabelEncoder()
    
    df['canteen_encoded'] = le_canteen.fit_transform(df['canteen_name'])
    df['weather_encoded'] = le_weather.fit_transform(df['weather_condition'])
    
    features = ['canteen_encoded', 'day_of_week', 'hour', 'temperature', 
                'weather_encoded', 'exam_week', 'event_day', 'holiday']
                
    X = df[features]
    y_reg = df['crowd_count']
    y_clf = df['crowd_level']
    
    encoders = {
        'canteen': le_canteen,
        'weather': le_weather
    }
    
    return X, y_reg, y_clf, encoders

def train_models():
    """
    Train and save ML models.
    """
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'canteen_data.csv')
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}. Please run data_simulator.py first.")
        return
        
    df = pd.read_csv(data_path)
    X, y_reg, y_clf, encoders = prepare_data(df)
    
    # Split data
    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
        X, y_reg, y_clf, test_size=0.2, random_state=42
    )
    
    print("Training Random Forest Regressor...")
    regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    regressor.fit(X_train, y_reg_train)
    
    # Evaluate Regressor
    reg_preds = regressor.predict(X_test)
    r2 = r2_score(y_reg_test, reg_preds)
    mae = mean_absolute_error(y_reg_test, reg_preds)
    print(f"Regression Performance - R2 Score: {r2:.4f}, MAE: {mae:.2f}")
    
    print("Training Random Forest Classifier...")
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train, y_clf_train)
    
    # Evaluate Classifier
    clf_preds = classifier.predict(X_test)
    accuracy = accuracy_score(y_clf_test, clf_preds)
    print(f"Classification Accuracy: {accuracy:.4f}")
    
    # Save models and encoders
    models_dir = os.path.dirname(__file__)
    joblib.dump(regressor, os.path.join(models_dir, 'rf_regressor.pkl'))
    joblib.dump(classifier, os.path.join(models_dir, 'rf_classifier.pkl'))
    joblib.dump(encoders, os.path.join(models_dir, 'encoders.pkl'))
    
    # Also save metrics for display in app
    metrics = {'r2': r2, 'mae': mae, 'accuracy': accuracy}
    joblib.dump(metrics, os.path.join(models_dir, 'metrics.pkl'))
    
    print("✅ Models, encoders, and metrics saved successfully.")

if __name__ == "__main__":
    train_models()
