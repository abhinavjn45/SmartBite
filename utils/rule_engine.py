POPULARITY_FACTORS = {
    "Main Canteen": 1.5,
    "Fresherteria": 1.2,
    "Gourmet Extension": 1.1,
    "Mingos": 0.8,
    "Kiosk": 0.7,
}


def categorize_crowd(count):
    if count <= 20:
        return "Low"
    if count <= 50:
        return "Medium"
    if count <= 80:
        return "High"
    return "Critical surge"


def _hour_multiplier(hour, minute=0):
    multiplier = 1.0
    if 12 <= hour <= 14:
        multiplier = 3.5
    elif 8 <= hour <= 9:
        multiplier = 2.0
    elif 16 <= hour <= 17:
        multiplier = 1.8

    if (hour == 10 and minute >= 45) or (hour == 12 and minute >= 45):
        multiplier += 2.0
    return multiplier


def predict_crowd(canteen_name, day_of_week, hour, temperature, weather, exam_week, event_day, holiday, minute=0):
    is_weekend = day_of_week >= 5

    if holiday:
        count = 2
        return count, categorize_crowd(count)

    base = 24 if not is_weekend else 8
    popularity = POPULARITY_FACTORS.get(canteen_name, 1.0)
    rush = _hour_multiplier(hour, minute)

    weather_multiplier = 1.0
    if weather == "Rainy":
        weather_multiplier = 1.4 if canteen_name in ["Main Canteen", "Fresherteria"] else 0.5
    elif weather == "Sunny":
        weather_multiplier = 0.9

    exam_multiplier = 1.3 if exam_week else 1.0
    event_multiplier = 1.5 if event_day else 1.0
    temp_multiplier = max(0.8, min(1.2, 1 + ((temperature - 28) * 0.02)))

    count = int(base * popularity * rush * weather_multiplier * exam_multiplier * event_multiplier * temp_multiplier)
    count = max(0, count)
    return count, categorize_crowd(count)