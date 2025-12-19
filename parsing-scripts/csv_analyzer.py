import pandas as pd
import json
from typing import Dict

def count_by_state_from_csv(file_path: str) -> Dict[str, int]:
    """
    Reads a CSV file containing a 'city' column, infers the state for each city 
    using a predefined mapping, and returns a dictionary with the count of 
    occurrences for each state.
    """
    
    # Mapping of major Indian cities to their states
    city_to_state = {
        "Mumbai": "Maharashtra", "Pune": "Maharashtra", "Thāne": "Maharashtra", "Nagpur": "Maharashtra",
        "Bengaluru": "Karnataka",
        "Hyderabad": "Telangana",
        "New Delhi": "Delhi", "Delhi": "Delhi",
        "Chennai": "Tamil Nadu", "Coimbatore": "Tamil Nadu",
        "Ahmedabad": "Gujarat", "Surat": "Gujarat", "Vadodara": "Gujarat", "Jamnagar": "Gujarat", "Bhavnagar": "Gujarat",
        "Kolkata": "West Bengal",
        "Jaipur": "Rajasthan",
        "Lucknow": "Uttar Pradesh", "Noida": "Uttar Pradesh",
        "Kochi": "Kerala",
        "Indore": "Madhya Pradesh",
        "Chandigarh": "Chandigarh",
    }
    
    try:
        # 1. Read the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except Exception as e:
        print(f"An error occurred while reading the CSV: {e}")
        return {}

    # 2. Clean data and map cities to states
    df_clean = df.dropna(subset=['city'])
    df_clean.loc[:, 'state'] = df_clean['city'].map(city_to_state)
    df_with_state = df_clean.dropna(subset=['state'])
    
    # 3. Count occurrences by state and convert to dictionary
    state_counts = df_with_state['state'].value_counts().to_dict()
    
    return state_counts

# --- Execution Block ---
csv_file_name = 'bquxjob_7832f526_19ada0fdcc1.csv' 
json_output_file = 'parsed_data.json' # <-- File name you requested

# 1. Get the parsed data
state_data = count_by_state_from_csv(csv_file_name)

# 2. Write the dictionary to a JSON file
try:
    with open(json_output_file, 'w') as f:
        # json.dump() writes the Python dictionary directly to the file object
        # indent=2 makes the JSON human-readable (pretty-printed)
        json.dump(state_data, f, indent=2)
    print(f"✅ Data successfully written to {json_output_file}")
    
except Exception as e:
    print(f"❌ An error occurred while writing the file: {e}")