import math
import streamlit as st

railway_image_path = "image/railway.jpeg"
city_image_path = "image/city.jpg"
hill_image_path = "image/hill.jpg"
lake_image_path = "image/lake.jpg"
office_image_path = "image/office.jpg"
park_image_path = "image/park.jpg"
globe_image_path = "image/globe.png"

def process_geonames_file(search_input, file_path):
    locations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.split('\t')
            latitude = float(data[4])
            longitude = float(data[5])
            country = data[8]
            state_code = data[10]
            if "," in search_input:
                name = data[1]
            else:
                name = data[1] + ", " + data[2] + ", " + data[3]
            region = data[6]
            sub_region = data[7]
            approximate_population = data[14]
            approximate_elevation = data[15]
            locations.append((latitude, longitude, country, state_code, sub_region, region, approximate_elevation, approximate_population, name))  
    return locations

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def find_nearest_location(locations, search_input):
    if "," in search_input:
        latitude, longitude = map(float, search_input.split(","))
        is_coordinate = True
    else:
        place_name = search_input.lower()
        is_coordinate = False
        distance = None
    
    min_distance = float('inf')
    nearest_location = None
    nearest_ppl_location = None
    nearest_road_location = None
    nearest_mountain_location = None
    nearest_lake_location = None
    nearest_park_location = None
    nearest_building_location = None

    ppl_distance = float('inf')
    road_distance = float('inf')
    mountain_distance = float('inf')
    lake_distance = float('inf')
    park_distance = float('inf')
    building_distance = float('inf')

    try:
        from all_states_code import all_states
    except:
        print("\033[91mError finding all_states_code.py, run get_all_states-codes.py\033[0m")

    for loc in locations:
        loc_lat, loc_lon, country, state_code, sub_region, region, approximate_elevation, approximate_population, name = loc

        if is_coordinate:
            distance = haversine(latitude, longitude, loc_lat, loc_lon)
        else:
            if (place_name in country.lower() or
                place_name in state_code.lower() or
                place_name in sub_region.lower() or
                place_name in region.lower() or
                place_name in name.lower()):
                distance = 0
            else:
                distance = None

        if distance is not None:
            if sub_region.lower() == "adm2":
                if distance < min_distance:
                    min_distance = distance
                    nearest_location = loc
            elif sub_region.lower().startswith("ppl") and distance < ppl_distance:
                ppl_distance = distance
                nearest_ppl_location = loc
            elif region.lower() == "r" and distance < road_distance:
                road_distance = distance
                nearest_road_location = loc
            elif region.lower() == "t" and distance < mountain_distance:
                mountain_distance = distance
                nearest_mountain_location = loc
            elif region.lower() == "h" and distance < lake_distance:
                lake_distance = distance
                nearest_lake_location = loc
            elif region.lower() == "l" and distance < park_distance:
                park_distance = distance
                nearest_park_location = loc
            elif region.lower() == "s" and distance < building_distance:
                building_distance = distance
                nearest_building_location = loc
                
    if nearest_ppl_location:
        loc_lat, loc_lon, country, state_code, sub_region, region, approximate_elevation, approximate_population, name = nearest_ppl_location
        populated = name
        
    state_name = None
    for state_info in all_states:
        if state_info == state_code:
            state_name = state_info[-1]
            break

    return (nearest_location, min_distance), (nearest_ppl_location, ppl_distance), (nearest_road_location, road_distance), (nearest_mountain_location, mountain_distance), (nearest_lake_location, lake_distance), (nearest_park_location, park_distance), (nearest_building_location, building_distance), state_name, is_coordinate


def main():
    st.title("Geolocation Search")
    st.image(globe_image_path, use_column_width=True)
    st.write("Please enter the geographic coordinates in decimal format or the name of a place.")
    st.write("For latitude, positive numbers indicate north, and negative numbers indicate south.")
    st.write("For longitude, positive numbers indicate east, and negative numbers indicate west.")
    st.write("Example: Latitude 40.7128, Longitude -74.0060")

    search_input = st.text_input("Enter latitude and longitude separated by comma or the name of a place:")

    if st.button("Search"):
        with st.spinner("Searching..."):
            locations = process_geonames_file(search_input, "IN.txt")
            nearest_location, nearest_ppl_location, nearest_road_location, nearest_mountain_location, nearest_lake_location, nearest_park_location, nearest_building_location, state_name, is_coordinate = find_nearest_location(locations, search_input)

            if is_coordinate:
                display_coordinate_results(nearest_location, nearest_ppl_location, nearest_road_location, nearest_mountain_location, nearest_lake_location, nearest_park_location, nearest_building_location)
            else:
                display_place_results(nearest_ppl_location, state_name)

def display_coordinate_results(nearest_location, nearest_ppl_location, nearest_road_location, nearest_mountain_location, nearest_lake_location, nearest_park_location, nearest_building_location):
    st.write("\n**Closest coordinates found:**")
    loc_lat, loc_lon, country, state_code, sub_region, region, approximate_elevation, approximate_population, name = nearest_location[0]
    st.write(f"- Latitude: {loc_lat}")
    st.write(f"- Longitude: {loc_lon}")
    st.write(f"- Distance to found coordinates: {round(nearest_location[1], 2)} km")
    st.write(f"- Country: {country}")
    st.write(f"- State: {state_code}")
    st.write(f"- City: {name}")
    st.write(f"- Approximate elevation: {approximate_elevation} m")
    st.write(f"- Approximate population: {approximate_population}")

    st.write("\n**Closest points found from your provided point and the Distance:**")
    st.write(f"- Nearest populated place: {nearest_ppl_location[0][-1]}")
    st.write(f"- Distance to nearest populated place: {round(nearest_ppl_location[1], 2)} km")
    st.image(city_image_path, use_column_width=True)
    st.write(f"- Nearest road/railway: {nearest_road_location[0][-1]}")
    st.write(f"- Distance to nearest road/railway: {round(nearest_road_location[1], 2)} km")
    st.image(railway_image_path, use_column_width=True)
    st.write(f"- Nearest hill/mountain/rock: {nearest_mountain_location[0][-1]}")
    st.write(f"- Distance to nearest hill/mountain/rock: {round(nearest_mountain_location[1], 2)} km")
    st.image(hill_image_path, use_column_width=True)
    st.write(f"- Nearest lake: {nearest_lake_location[0][-1]}")
    st.write(f"- Distance to nearest lake: {round(nearest_lake_location[1], 2)} km")
    st.image(lake_image_path, use_column_width=True)
    st.write(f"- Nearest park: {nearest_park_location[0][-1]}")
    st.write(f"- Distance to nearest park: {round(nearest_park_location[1], 2)} km")
    st.image(park_image_path, use_column_width=True)
    st.write(f"- Nearest building: {nearest_building_location[0][-1]}")
    st.write(f"- Distance to nearest building: {round(nearest_building_location[1], 2)} km")
    st.image(office_image_path, use_column_width=True)


def display_place_results(nearest_ppl_location, state_name):
    st.write("\n**Found coordinates:**")
    for loc in nearest_ppl_location:
        loc_lat, loc_lon, country, state, sub_region, region, approximate_elevation, approximate_population, name = loc
        st.write(f"- Latitude: {loc_lat}")
        st.write(f"- Longitude: {loc_lon}")
        st.write(f"- Country: {country}")
        st.write(f"- State: {state}")
        st.write(f"- Location Type: {region}")
        st.write(f"- Location Name: {name}")
        st.write(f"- Approximate elevation: {approximate_elevation} m")
        st.write(f"- Approximate population: {approximate_population}")

if __name__ == "__main__":
    main()