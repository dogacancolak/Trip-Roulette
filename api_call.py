import urllib.request
import json
import time

valid_location_types = {"airport", "library", \
                        "amusement_park", "aquarium",\
                        "liquor_store", "art_gallery",\
                        "atm", "bakery", "lodging", "bar", \
                        "mosque", "shopping_mall"\
                        "book_store", "movie_theater",\
                        "museum", "cafe",\
                        "campground", "painter", "park", \
                        "parking", "car_wash", "pharmacy", \
                        "casino", "church", \
                        "restaurant", "spa", "florist",\
                        "stadium", "store", "gym", "tourist_attraction", \
                        "university", "zoo" \
                        }

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
    results  = []
    for place in place_types:
        if place in valid_location_types:
            place_search_word = 'type'      # to be inserted in the API request
        else:
            place_search_word = 'keyword'
            
        #&opennow
        nav_request =  'location={}&maxprice={}&radius={}&{}={}&rankby=prominence&key={}'\
                        .format(str(location), str(max_price), str(radius), place_search_word, place, key)
        response = json.loads(urllib.request.urlopen(endpoint + nav_request).read())

        if not response["results"] == []:
            if 'next_page_token' in response:
                tokens.append(response["next_page_token"])
            else:
                tokens.append(0)
        
            requests.append(endpoint + nav_request)
            results.append(response["results"])

    tokens_left = True
    while tokens_left:
        tokens_left = False
        i = 0 
        while i < min(len(tokens), len(requests), len(results)):
            if tokens[i] != 0:
                tokens_left = True
                next_page_token = tokens[i]

                new_request = requests[i] + '&pagetoken=' + next_page_token
                new_response = json.loads(urllib.request.urlopen(new_request).read())

                if new_response["status"] == 'OK':
                    results[i].extend(new_response["results"])
                    if 'next_page_token' in new_response:
                        tokens[i] = new_response["next_page_token"]
                    else:
                        tokens[i] = 0  
            i += 1
           
    return results


# class Amcik():
#     pass

# amcik = Amcik()
# amcik.lat = 42.406722   # Tufts location as default (easter egg lol)
# amcik.lon = -71.116469
# amcik.radius = 10000
# amcik.interests = ['attraction', 'museum', 'shopping_mall', 'monument', 'hiking']
# amcik.food = ['restaurant', 'bar', 'cafe']
# amcik.trip_length = 4
# amcik.budget = 4
# amcik.transportation = 'walking'

# results = get_places_in_radius(amcik, amcik.interests)

# for p in results:
#     print("\nResult AMK")
#     for res in p:
#         print("Name: ", res["name"])
