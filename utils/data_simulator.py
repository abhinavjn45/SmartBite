import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

CANTEENS = ["Main Canteen", "Fresherteria", "Gourmet Extension", "Mingos", "Kiosk"]
WEATHER_CONDITIONS = ["Sunny", "Cloudy", "Rainy"]

def generate_simulated_data(num_days=30):
    """
    Generate realistic campus canteen data.
    """
    records = []
    
    # Start date 30 days ago
    start_date = datetime.now() - timedelta(days=num_days)
    start_date = start_date.replace(hour=8, minute=0, second=0, microsecond=0)
    
    for day_offset in range(num_days):
        current_date = start_date + timedelta(days=day_offset)
        
        # Determine day level attributes
        day_of_week = current_date.weekday() # 0 = Monday, 6 = Sunday
        is_weekend = day_of_week >= 5
        exam_week = 1 if np.random.rand() < 0.2 else 0 # 20% chance of being exam week
        event_day = 1 if np.random.rand() < 0.1 else 0 # 10% chance of being event day
        daily_temp = random.randint(22, 35) # Temp in Celsius
        daily_weather = random.choice(WEATHER_CONDITIONS)
        
        # Simulate hours from 8 AM to 6 PM (8 to 18)
        for hour in range(8, 19):
            for canteen in CANTEENS:
                timestamp = current_date.replace(hour=hour, minute=0)
                
                # Base crowd logic
                # Higher crowd on weekdays, lower on weekends
                base_crowd = random.randint(5, 30) if not is_weekend else random.randint(0, 10)
                
                # Rush hour multipliers
                rush_multiplier = 1.0
                if 12 <= hour <= 14: # Lunch peak
                    rush_multiplier = 3.5
                elif 8 <= hour <= 9: # Breakfast peak
                    rush_multiplier = 2.0
                elif 16 <= hour <= 17: # Evening snacks
                    rush_multiplier = 1.8
                
                # Canteen specific popularity
                popularity_factors = {
                    "Main Canteen": 1.5,
                    "Fresherteria": 1.2,
                    "Gourmet Extension": 1.1,
                    "Mingos": 0.8,
                    "Kiosk": 0.7
                }
                canteen_multiplier = popularity_factors.get(canteen, 1.0)
                
                # Other factors
                exam_multiplier = 1.3 if exam_week else 1.0 # More students stay on campus during exams
                event_multiplier = 1.5 if event_day else 1.0
                
                weather_multiplier = 1.0
                if daily_weather == "Rainy":
                    weather_multiplier = 1.4 # People crowd nearby internal canteens
                elif daily_weather == "Sunny":
                    weather_multiplier = 0.9 # People might go outside
                    
                # Calculate final crowd count
                crowd_count = int(base_crowd * rush_multiplier * canteen_multiplier * \
                                  exam_multiplier * event_multiplier * weather_multiplier)
                                  
                # Add some noise
                crowd_count += random.randint(-5, 10)
                crowd_count = max(0, crowd_count) # Ensure it's not negative
                
                # Specific logic: During lunch at Main Canteen on a rainy exam day, it gets very crowded
                if canteen == "Main Canteen" and (12 <= hour <= 14) and not is_weekend:
                    crowd_count += random.randint(20, 50)
                
                records.append({
                    "timestamp": timestamp,
                    "canteen_name": canteen,
                    "day_of_week": day_of_week,
                    "temperature": daily_temp,
                    "weather_condition": daily_weather,
                    "exam_week": exam_week,
                    "event_day": event_day,
                    "crowd_count": crowd_count
                })
                
    df = pd.DataFrame(records)
    
    # Save the simulated data to CSV
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'canteen_data.csv')
    df.to_csv(file_path, index=False)
    print(f"✅ Generated {len(df)} records of simulated canteen data.")
    print(f"📁 Data saved to {file_path}")
    
    return df

if __name__ == "__main__":
    generate_simulated_data()
