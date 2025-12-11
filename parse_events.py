import pandas as pd
import json

# Load the data
# df = pd.read_csv('events_by_city_location.csv')
# df = pd.read_csv('events_dec2_full_day.csv')
df = pd.read_csv('events_dec2_615am_715am_ist.csv')

# Create the list of coordinates expanded by event count
output_data = []
for index, row in df.iterrows():
    coords = [row['latitude'], row['longitude']]
    count = row['event_count']
    output_data.extend([coords] * count)

# Save to JSON
with open('parsed_events_dec2_615am_715am_ist.json', 'w') as f:
    json.dump(output_data, f)