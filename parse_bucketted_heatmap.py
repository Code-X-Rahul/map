# import pandas as pd
# import json
# import os

# # 1. Load the CSV file
# # Replace with your actual filename if different
# # file_name = 'events_by_city_location.csv' 
# # file_name = 'events_dec2_full_day.csv' 
# file_name = 'events_dec2_615am_715am_ist.csv' 

# if not os.path.exists(file_name):
#     # Fallback for testing if specific file isn't found
#     print(f"Warning: '{file_name}' not found. Looking for 'events_by_city_location.csv'...")
#     file_name = 'events_by_city_location.csv'

# try:
#     df = pd.read_csv(file_name)
#     print(f"Successfully loaded {file_name}")
# except FileNotFoundError:
#     print("Error: No CSV file found. Please check the file name.")
#     exit()

# # 2. Define the Buckets and Fixed Intensities
# # Format: 'name': (min_val, max_val, fixed_intensity)
# buckets_config = [
#     {
#         'name': 'bucket1', 
#         'range': (1, 10), 
#         'intensity': 0.6 
#     },
#     {
#         'name': 'bucket2', 
#         'range': (11, 50), 
#         'intensity': 0.8 
#     },
#     {
#         'name': 'bucket3', 
#         'range': (51, float('inf')), 
#         'intensity': 1.0 
#     },

# ]

# output_data = {}

# # 3. Process each bucket
# print("\nProcessing buckets...")
# for b in buckets_config:
#     r_min, r_max = b['range']
#     intensity = b['intensity']
#     name = b['name']
    
#     # Filter the DataFrame for this range
#     subset = df[(df['event_count'] >= r_min) & (df['event_count'] <= r_max)]
    
#     # Create the list: [latitude, longitude, intensity]
#     data_list = []
#     for _, row in subset.iterrows():
#         # Ensure we have valid coordinates
#         if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
#             data_list.append([
#                 row['latitude'], 
#                 row['longitude'], 
#                 intensity
#             ])
            
#     # Add to output dictionary
#     output_data[name] = data_list
#     print(f" - {name} (Count {r_min}-{str(r_max).replace('inf', 'max')}): Found {len(data_list)} cities")

# # 4. Save to JSON
# # output_filename = 'heatmap_buckets_stepped.json'
# output_filename = 'demo-4.json'
# with open(output_filename, 'w') as f:
#     json.dump(output_data, f)

# print(f"\nDone! Saved output to '{output_filename}'")



import pandas as pd
import json
import os

# 1. Load the CSV file
file_name = 'events_dec2_615am_715am_ist.csv' 

if not os.path.exists(file_name):
    print(f"Warning: '{file_name}' not found. Looking for 'events_by_city_location.csv'...")
    file_name = 'events_by_city_location.csv'

try:
    df = pd.read_csv(file_name)
    print(f"Successfully loaded {file_name}")
except FileNotFoundError:
    print("Error: No CSV file found. Please check the file name.")
    exit()

# --- NEW CALCULATIONS ---
# Calculate Total Events
total_events = int(df['event_count'].sum())


# Identify city column
city_column = 'city' if 'city' in df.columns else df.columns[0] 

# Calculate Total Cities Count (Unique cities)
total_cities = int(df[city_column].nunique())

# Get Top 5 Cities (Assumes you have a 'city' or 'city_name' column)
# If your column name is different, change 'city' below
city_column = 'city' if 'city' in df.columns else df.columns[0] 
top_5_df = df.sort_values(by='event_count', ascending=False).head(5)
top_5_cities = top_5_df[[city_column, 'event_count']].to_dict(orient='records')
# ------------------------

# 2. Define the Buckets
buckets_config = [
    {'name': 'bucket1', 'range': (1, 10), 'intensity': 0.6},
    {'name': 'bucket2', 'range': (11, 50), 'intensity': 0.8},
    {'name': 'bucket3', 'range': (51, float('inf')), 'intensity': 1.0},
]

output_data = {
    "metadata": {
        "total_event_count": total_events,
        "top_5_cities": top_5_cities,
        "total_cities_count": total_cities,
    },
    "buckets": {}
}

# 3. Process each bucket
print("\nProcessing buckets...")
for b in buckets_config:
    r_min, r_max = b['range']
    intensity = b['intensity']
    name = b['name']
    
    subset = df[(df['event_count'] >= r_min) & (df['event_count'] <= r_max)]
    
    data_list = []
    for _, row in subset.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            data_list.append([row['latitude'], row['longitude'], intensity])
            
    output_data["buckets"][name] = data_list
    print(f" - {name} ({r_min}-{r_max}): Found {len(data_list)} cities")

# 4. Save to JSON
output_filename = 'demo-6.json'
with open(output_filename, 'w') as f:
    json.dump(output_data, f, indent=4) # Added indent for readability

print(f"\n--- Statistics ---")
print(f"Total Events: {total_events}")
print(f"Top City: {top_5_cities[0][city_column]} ({top_5_cities[0]['event_count']})")
print(f"Total Cities: {total_cities}") # Added to print output
print(f"\nDone! Saved output to '{output_filename}'")