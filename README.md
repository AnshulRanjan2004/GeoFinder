# GeoFinder

## Scripts

### gps.py

This script provides a comprehensive functionality to locate the nearest geographic locations based on given latitude and longitude coordinates (in decimal format). It calculates distances to the closest populated place, road/railway, hill/mountain, lake, park, and building. Additionally, it can determine the nearest administrative location (e.g., city, state) based on the provided coordinates.

### get_all_states-codes.py

This utility script extracts state information from geonames data and generates a Python file named `all_states_code.py`. It is employed internally by `gps.py`, `city-gps-location.py` and `state-gps-location.py` to retrieve corresponding name of a state based on its code.

### city-gps-location.py

This script enables users to find the coordinates of a specific city based on its name. It leverages geonames data to perform the city search.

### state-gps-location.py

This script enables users to find the coordinates of a specific state based on its name.

### country-gps-location.py

Users can utilize this script to find the coordinates of a specific country (it makes more sense using allCountries.txt of Geonames).

### all.py

To search for anything in the database, use the following input format: `<x,y>` for coordinates (in decimal format) or `<any-string>` for a string. If you search for a coordinate, the script will retrieve the nearest coordinate's location and its information. If the search is for a string, the script will retrieve all locations and their information from the database that contain this string.

### convert.py

This code provides functions to convert between decimal and sexagesimal representations of geographic coordinates (latitude and longitude).

To use it correctly:
1. Run the script.
3. Choose the desired conversion:
   - Enter '1' for decimal to sexagesimal conversion.
   - Enter '2' for sexagesimal to decimal conversion.
4. Follow the prompts:
   - For decimal to sexagesimal conversion, input latitude and longitude in decimal format (In the Southern hemisphere, use negative values for latitude, and in the Western hemisphere, use negative values for longitude).
   - For sexagesimal to decimal conversion, input latitude and longitude in the specified sexagesimal format (N/S for latitude, and E/W for longitude).
5. The script will output the converted coordinates.

## Usage

1. Ensure that you have Python installed on your system.
2. Download the geonames text files from [Geonames](https://www.geonames.org/export/dump) and place them in the repository directory, and change the .txt name file for your own country .txt database in each code you will use.
3. Run the desired Python script according to your location search requirements.

## Requirements

- Python 3.x
- Geonames text files (downloaded from the Geonames website)

## Notes

- Remember, to use geographic coordinates in these python codes, decimal format is required. I made ```convert.py``` precisely for type compatibility issues, as my codes do not accept the sexagesimal system (XXº XX' XX'' N/S/E/W). Then use ```convert.py``` for testing and conversions.
