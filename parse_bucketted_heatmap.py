import pandas as pd
import json
import os

# 1. Load the CSV file
# Replace with your actual filename if different
# file_name = 'events_by_city_location.csv' 
# file_name = 'events_dec2_full_day.csv' 
file_name = 'events_dec2_615am_715am_ist.csv' 

if not os.path.exists(file_name):
    # Fallback for testing if specific file isn't found
    print(f"Warning: '{file_name}' not found. Looking for 'events_by_city_location.csv'...")
    file_name = 'events_by_city_location.csv'

try:
    df = pd.read_csv(file_name)
    print(f"Successfully loaded {file_name}")
except FileNotFoundError:
    print("Error: No CSV file found. Please check the file name.")
    exit()

# 2. Define the Buckets and Fixed Intensities
# Format: 'name': (min_val, max_val, fixed_intensity)
buckets_config = [
    {
        'name': 'bucket1', 
        'range': (1, 50), 
        'intensity': 0.25 
    },
    {
        'name': 'bucket2', 
        'range': (51, 500), 
        'intensity': 0.50 
    },
    {
        'name': 'bucket3', 
        'range': (501, 2500), 
        'intensity': 0.75 
    },
    {
        'name': 'bucket4', 
        'range': (2501, float('inf')), # 'inf' means anything above 2501
        'intensity': 1.0 
    }
]

output_data = {}

# 3. Process each bucket
print("\nProcessing buckets...")
for b in buckets_config:
    r_min, r_max = b['range']
    intensity = b['intensity']
    name = b['name']
    
    # Filter the DataFrame for this range
    subset = df[(df['event_count'] >= r_min) & (df['event_count'] <= r_max)]
    
    # Create the list: [latitude, longitude, intensity]
    data_list = []
    for _, row in subset.iterrows():
        # Ensure we have valid coordinates
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            data_list.append([
                row['latitude'], 
                row['longitude'], 
                intensity
            ])
            
    # Add to output dictionary
    output_data[name] = data_list
    print(f" - {name} (Count {r_min}-{str(r_max).replace('inf', 'max')}): Found {len(data_list)} cities")

# 4. Save to JSON
# output_filename = 'heatmap_buckets_stepped.json'
output_filename = 'heatmap_buckets_stepped_dec2_615am_715am_ist.json'
with open(output_filename, 'w') as f:
    json.dump(output_data, f)

print(f"\nDone! Saved output to '{output_filename}'")