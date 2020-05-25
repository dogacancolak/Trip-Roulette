import urllib.request
import json
import time
import timeit

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

def get_places_in_radius(user_info, place_types):
    lat       = user_info.lat
    lon       = user_info.lon
    radius    = user_info.radius
    max_price = user_info.budget
    
    key            = 'AIzaSyA4H5RbPwYejTlXVI1hjio_4q4XYS_Ubts'
    endpoint       = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    location       = str(lat) + ',' + str(lon)
    
    requests = []
    tokens   = []
    results  = {}
    places_with_results = []

    for place in place_types:        if place in valid_location_types:
            place_search_word = 'type'      # to be inserted in the API request
        else:
            place_search_word = 'keyword'

        #&opennow
        nav_request =  'location={}&maxprice={}&radius={}&{}={}&rankby=prominence&key={}'\
                        .format(str(location), str(max_price), str(radius), place_search_word, place, key)
        response = json.loads(urllib.request.urlopen(endpoint + nav_request).read())
       
        if response["results"] != []:
            if 'next_page_token' in response:
                tokens.append(response["next_page_token"])
            else:
                tokens.append(0)
            requests.append(endpoint + nav_request)
            results[place] = response["results"]
            places_with_results.append(place)


    tokens_left = True
    min_loop = min(len(tokens), len(requests), len(results.keys()))
    while tokens_left:
        tokens_left = False
        i = 0
        
        while i < min_loop:
            if tokens[i] != 0:
                tokens_left = True
                next_page_token = tokens[i]

                new_request = requests[i] + '&pagetoken=' + next_page_token
                new_response = json.loads(urllib.request.urlopen(new_request).read())

                if new_response["status"] == 'OK':
                    results[places_with_results[i]].extend(new_response["results"])
                    if 'next_page_token' in new_response:
                        tokens[i] = new_response["next_page_token"]
                    else:
                        tokens[i] = 0
            i += 1

    return results