# config.py
api_key = 'AIzaSyDnNL7QG3n7CDhT1OfX4CCzbOW3KkudlVY'


# api_call.py

import urllib.request
import json
import time
import timeit
import ssl
import config
ssl._create_default_https_context = ssl._create_unverified_context

valid_location_types = {"airport", "hindu_temple", "library", \
                        "amusement_park", "aquarium",\
                        "liquor_store", "art_gallery",\
                        "atm", "bakery", "lodging", "bar", \
                        "mosque", "shopping_mall",\
                        "book_store", "movie_theater",\
                        "museum", "cafe", "shoe_store",\
                        "campground", "painter", "park", \
                        "parking", "car_wash", "pharmacy", \
                        "casino", "church", "night_club",\
                        "restaurant", "spa", "florist",\
                        "stadium", "store", "synagogue", "gym", "tourist_attraction", \
                        "university", "bowling_alley", "zoo" ,"clothing_store"}

def get_places_in_radius(user_info, place):
    lat       = user_info.lat
    lon       = user_info.lon
    radius    = user_info.radius
    max_price = user_info.budget
    
    key            = config.api_key
    endpoint       = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    location       = str(lat) + ',' + str(lon)
    
    token    = ''
    result  = {}
  
    if place in valid_location_types:
        place_search_word = 'type'      # to be inserted in the API request
    else:
        place_search_word = 'keyword'

    nav_request =  'location={}&opennow&maxprice={}&radius={}&{}={}&rankby=prominence&key={}'\
                    .format(str(location), str(max_price), str(radius), place_search_word, place, key)
    request = endpoint + nav_request

    response = json.loads(urllib.request.urlopen(endpoint + nav_request).read())
    
    if response["results"] != []:
        if 'next_page_token' in response:
            token = response["next_page_token"]

        result[place] = response["results"]

    while token:

        new_request = request + '&pagetoken=' + token
        new_response = json.loads(urllib.request.urlopen(new_request).read())

        if new_response["status"] == 'OK':
            result[place].extend(new_response["results"])
            if 'next_page_token' in new_response:
                token = new_response["next_page_token"]
            else:
                token = ''

    return result
