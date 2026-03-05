from .wait_time import estimate_wait_time

# Exact locations on campus (Latitude, Longitude) for Folium
CANTEEN_LOCATIONS = {
    "Main Canteen": (12.934335958305272, 77.6058026269377),
    "Fresherteria": (12.93476402563866, 77.60668373260971),
    "Gourmet Extension": (12.934621554456797, 77.60597831164888),
    "Mingos": (12.932145287682525, 77.60662807673751),
    "Kiosk": (12.93320598769562, 77.60657979701222)
}

def calculate_distance(coord1, coord2):
    """
    Calculate simple Euclidean distance for mock purposes (returns arbitrary units).
    """
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

def recommend_alternatives(canteen_name, current_predictions):
    """
    Recommend alternative canteens if the selected one is crowded.
    
    current_predictions: list of dicts 
    [{'canteen': 'Main Canteen', 'crowd_count': 50, 'level': 'High'}, ...]
    """
    selected_canteen_coords = CANTEEN_LOCATIONS.get(canteen_name, (0,0))
    alternatives = []
    
    for pred in current_predictions:
        name = pred['canteen']
        if name == canteen_name:
            continue
            
        wait_time = estimate_wait_time(name, pred['crowd_count'])
        distance = calculate_distance(selected_canteen_coords, CANTEEN_LOCATIONS.get(name, (0,0)))
        
        # We want to score them. Lower is better.
        # Wait time is most important, then distance, then risk
        risk_score = {"Low": 1, "Medium": 2, "High": 3, "Critical surge": 4}.get(pred['level'], 1)
        
        # Simple weighted score
        score = wait_time * 0.6 + (distance * 10000) * 0.2 + risk_score * 5
        
        alternatives.append({
            "canteen": name,
            "wait_time": wait_time,
            "distance_score": round(distance * 10000), # arbitrary units for display
            "level": pred['level'],
            "score": score,
            "coords": CANTEEN_LOCATIONS.get(name, (0,0))
        })
        
    # Sort by score ascending (lowest score is best)
    alternatives.sort(key=lambda x: x['score'])
    return alternatives
