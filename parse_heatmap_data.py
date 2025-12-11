import pandas as pd
import json

# 1. Load the CSV
# df = pd.read_csv('events_by_city_location.csv')
df = pd.read_csv('events_dec2_full_day.csv')

# 2. Find the max value to normalize intensity (0.0 to 1.0)
max_events = df['event_count'].max()

# 3. Create a list of [lat, lon, intensity]
# Intensity is event_count / max_events
heatmap_data = []
for index, row in df.iterrows():
    intensity = round(row['event_count'] / max_events, 4)
    heatmap_data.append([row['latitude'], row['longitude'], intensity])

# 4. Save to JSON
with open('heatmap_data-2-dec.json', 'w') as f:
    json.dump(heatmap_data, f)

print("Done! Saved heatmap_data.json")