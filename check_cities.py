import json

# Load GeoJSON
with open('geojson/district/india_district.geojson', 'r') as f:
    geojson = json.load(f)

# Extract city names
geojson_cities = set()
for feature in geojson['features']:
    if 'properties' in feature and 'NAME_2' in feature['properties']:
        geojson_cities.add(feature['properties']['NAME_2'])

# Load user data
with open('parsed_city_counts_normalized.json', 'r') as f:
    user_data = json.load(f)

user_cities = set(user_data.keys())

# Find missing cities
missing_cities = user_cities - geojson_cities

print(f"GeoJSON cities: {len(geojson_cities)}")
print(f"User data cities: {len(user_cities)}")
print(f"Missing cities: {len(missing_cities)}")

if missing_cities:
    missing_sorted = sorted(missing_cities, key=lambda x: user_data[x], reverse=True)
    print(f"\nTop 30 missing cities:")
    for i, city in enumerate(missing_sorted[:30], 1):
        print(f"{i:3d}. {city:30s} - {user_data[city]:5d} users")
