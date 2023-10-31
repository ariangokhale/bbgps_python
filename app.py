import pandas as pd
from haversine import haversine, Unit
import requests
import os
import geocoder
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup


# Cleaning Bluebike station data from https://www.bluebikes.com/system-data
file_path = "current_bluebikes_stations.csv"
bike_df = pd.read_csv(file_path, header=None)
bike_df = bike_df.drop(0)
bike_df.columns = bike_df.iloc[0]
bike_df = bike_df[1:]
bike_stations = bike_df.to_dict(orient='records')




API_KEY = "YOUR_API_KEY"

app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('index.html')

@app.route("/direction_home", methods=['POST'])
def directions_app():

    
    # Get the location of the nearest blubike station to the destination
    destination = request.form['input_variable']
    destination_nearest_bike = find_nearest_bluebike(get_destination_coord(destination))
    
    # Get user's current location and the BB station closest to them currently
    current_location = get_user_location(API_KEY)
    current_nearest_bike = find_nearest_bluebike(current_location)

    # Get the directions between the two stations
    biking_directions = get_biking_directions(current_nearest_bike, destination_nearest_bike, "bicycling")

    # render a template that shows the directions and the map
    return render_template('directions.html', 
                           biking_directions=biking_directions, 
                           destination=destination,
                           origin=current_nearest_bike, 
                           bike_location=destination_nearest_bike)


# Get a user's current location
def get_user_location(api_key):

    location = geocoder.ip('me')
    if location.latlng:
        latitude, longitude = location.latlng
        return latitude, longitude
    else:
        return None


# Get destination in Lat, Long form
def get_destination_coord(destination):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={destination}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        results = data['results']
        if len(results) > 0:
            location = results[0]['geometry']['location']
            latitude, longitude = location['lat'], location['lng']
            return (latitude, longitude)
        else:
            print('No results found')
    else:
        print(data['status'])


"""Location is in the form of (latitude, longitude)"""
# Find the nearest bluebike station from an input location
@app.route("/nearest_bb_to_destination")
def find_nearest_bluebike(location):
    nearest_station = None
    town = ""
    min_distance = float('inf')  # arbitrary large number to begin comparisons

    for station in bike_stations:
        bike_location = (float(station['Latitude']),
                         float(station['Longitude']))

        distance = haversine(location, bike_location, unit=Unit.MILES)

        if distance < min_distance:
            nearest_station = station['Name']
            min_distance = distance
            town = station['District']

    return nearest_station + ", " + town


# Get the directions between two locations, change method as needed (driving, walking, bicycling)
@app.route("/directions")
def get_biking_directions(origin, destination, method):

    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={method}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    directions_data = []

    if data['status'] == 'OK':
        routes = data['routes']
        if len(routes) > 0:
            legs = routes[0]['legs']

            for leg in legs:
                print('Start Address:', leg['start_address'])
                print('End Address:', leg['end_address'])
                print('Distance:', leg['distance']['text'])
                print('Duration:', leg['duration']['text'])
                print('Steps:')

                for step in leg['steps']:
                    #print('  -', step['html_instructions'])
                    #print('    Distance:', step['distance']['text'])
                    #print('    Duration:', step['duration']['text'])
                    #print()

                    step_dict = {}
                    step_dict["html_instruction"] = remove_html_tags(step['html_instructions'])
                    step_dict['distance'] = step['distance']['text']
                    step_dict['duration'] = step['duration']['text']

                    directions_data.append(step_dict)
                    
        else:
            print('No routes found.')
    else:
        print('Directions request failed. Error:', data['status'])

    return directions_data

# Create HTML parsing code
def remove_html_tags(input_string):
    soup = BeautifulSoup(input_string, "html.parser")
    clean_text = soup.get_text()
    return clean_text



if __name__ == "__main__":
    app.run(debug=True)