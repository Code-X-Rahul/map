import pandas as pd
import json
import unicodedata
from typing import Dict, List

def count_by_city_from_csv(file_path: str) -> Dict[str, int]:
    """
    Reads a CSV file containing a 'city' column and returns a dictionary
    with the count of occurrences (frequency) for each unique city.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return {}

    if 'city' not in df.columns:
        print("Error: CSV must contain a 'city' column.")
        return {}
    
    # Drop rows with missing city names
    df_clean = df.dropna(subset=['city'])
    
    # Count occurrences by city
    city_counts = df_clean['city'].value_counts().to_dict()
    
    return city_counts

def normalize_city_keys(data: Dict[str, int]) -> Dict[str, int]:
    """
    Normalizes city names in a dictionary by converting Unicode characters 
    with diacritics (accents) to their base ASCII equivalents (e.g., 'Thāne' -> 'Thane').
    
    Handles potential key collisions by summing values.
    """
    normalized_data = {}
    for key, value in data.items():
        # 1. Normalize the string to NFKD form (separates base characters and diacritics)
        normalized_key = unicodedata.normalize('NFKD', key)
        
        # 2. Encode to ASCII, ignoring the diacritics, and then decode back to a standard string
        ascii_key = normalized_key.encode('ascii', 'ignore').decode('utf-8')
        
        # 3. Aggregate counts in case two different Unicode keys normalize to the same ASCII key
        normalized_data[ascii_key] = normalized_data.get(ascii_key, 0) + value
        
    return normalized_data

# --- Main Execution Block ---

# Set file paths
csv_file_name = 'bquxjob_7832f526_19ada0fdcc1.csv' 
json_output_file = 'parsed_city_counts_normalized.json' 

# 1. Get the raw city count data
raw_city_data = count_by_city_from_csv(csv_file_name)

# 2. Normalize the city names
normalized_city_data = normalize_city_keys(raw_city_data)

# 3. Write the normalized dictionary to a JSON file
if normalized_city_data:
    try:
        with open(json_output_file, 'w') as f:
            json.dump(normalized_city_data, f, indent=2)
        
        print(f"Success: City count data saved to {json_output_file}")
        print(f"Total unique cities (normalized): {len(normalized_city_data)}")
    
    except Exception as e:
        print(f"Error saving JSON file: {e}")
else:
    print("Execution failed: No data processed.")