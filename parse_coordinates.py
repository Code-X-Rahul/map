import pandas as pd
import json
from typing import List

def read_coords_from_csv(file_path: str) -> List[List[float]]:
    """
    Reads a CSV file containing 'latitude' and 'longitude' columns, 
    and returns a list of [latitude, longitude] pairs.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception:
        return []

    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        return []

    # Drop rows where latitude or longitude might be missing
    df_clean = df.dropna(subset=['latitude', 'longitude'])

    # Select the columns and convert to a list of lists
    coords_list = df_clean[['latitude', 'longitude']].values.tolist()
    
    return coords_list

# --- Execution Block ---
csv_file_name = 'bquxjob_7832f526_19ada0fdcc1.csv' 
json_output_file = 'parsed_coordinates.json' 

# 1. Get the parsed coordinate data
coordinates = read_coords_from_csv(csv_file_name)

# 2. Write the list to a JSON file
try:
    with open(json_output_file, 'w') as f:
        # json.dump() writes the Python list directly to the file object
        json.dump(coordinates, f, indent=2)
    # Success message would appear here
    
except Exception as e:
    # Error message would appear here
    pass