SERVICE_RATE_FACTORS = {
    "Main Canteen": 0.5, # Takes 0.5 mins per person
    "Fresherteria": 0.8,
    "Gourmet Extension": 1.0,
    "Mingos": 1.2,
    "Kiosk": 0.3
}

def estimate_wait_time(canteen_name, crowd_count):
    """
    Formula: wait_time = crowd_count * service_rate_factor
    """
    factor = SERVICE_RATE_FACTORS.get(canteen_name, 1.0)
    return round(crowd_count * factor, 1)

def get_service_rate(canteen_name):
    return SERVICE_RATE_FACTORS.get(canteen_name, 1.0)
