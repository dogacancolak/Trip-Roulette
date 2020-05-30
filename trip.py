from kivy.app import App
from kivy.clock import Clock
from kivymd.toast import toast

from api_call import get_places_in_radius

import random
import urllib
import json
import sys
import concurrent.futures
import time
import math
from itertools import repeat

interest_places = {}
food_places = {}
user_info = None

loading_label_texts = ["Selecting locations...", "Optimizing route..."]

def generate_trip(trip_details): 
    global interest_places
    global food_places
    global user_info

    app = App.get_running_app()
    user_info = app.user_info


    def change_loading_label(*args):
        app = App.get_running_app()
        if loading_label_texts:
            text = loading_label_texts[0]
            app.root.loadingpage.ids.loading_label.text = text
            loading_label_texts.remove(text)

    trigger = Clock.create_trigger(change_loading_label)
    results = []
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        combined_locations = user_info.interests + user_info.food
        results = executor.map(get_places_in_radius, repeat(user_info), combined_locations)

        for dictionary in results:
            if dictionary:
                key = next(iter(dictionary))
                print(key, ": ", len(dictionary[key]))
                if key in user_info.food:
                    food_places.update(dictionary)
                elif key in user_info.interests:
                    interest_places.update(dictionary)
                else:
                    toast("Key Error")
                    trip_details.append([])
                    trip_details.append('')
                    trip_details.append({})
                    return trip_details    #return empty waypoints and empty url and empty route json

    data_pop_time = time.time() - start
    count = 0
    for value in food_places.values():
        count += len(value)
    for value in interest_places.values():
        count += len(value)          

    print("number of interest + food: ", count)
    
    if not interest_places and not food_places:
        toast("No places found nearby. Please expand your options.")
        trip_details.append([])
        trip_details.append('')
        trip_details.append({})
        return trip_details    #return empty waypoints and empty url    
    # print("adding waypoints", file=sys.stderr)

    trigger()

    waypoints = []
    populate_waypoints(waypoints)

    # print("find directions", file=sys.stderr)

    route_start_time = time.time()

    route_details = optimize_route(waypoints)

    route = route_details[0]
    if not route:
        trip_details.append([])
        trip_details.append('')
        trip_details.append({})
        return trip_details    #return empty waypoints and empty url and empty route json

    time_spent = route_details[1]

    trigger()

    entered = False
    while time_spent > user_info.trip_length + 15:
        removed = remove_waypoint(waypoints)
        if not removed:
            break
        else:
            route_details = optimize_route(waypoints)
            route = route_details[0]
            time_spent = route_details[1]
        entered = True
        print("trip length too long", file=sys.stderr)

    if not entered:
        while time_spent < user_info.trip_length - 40:
            added = add_waypoint(waypoints)
            if not added:
                
                break
            else:
                route_details = optimize_route(waypoints)
                route = route_details[0]
                time_spent = route_details[1]
                
            print("trip length too short", file=sys.stderr)

    route_time = time.time() - route_start_time
    # print("while loops", file=sys.stderr)

    waypoints = [waypoints[i] for i in route['waypoint_order']]

    for p in waypoints:
        print(list(p.values())[0]['name'])
        
    url = generate_url(waypoints)

    print("Time spent: ", time_spent/60, file=sys.stderr)
    
    all_time = time.time() - start
    print("Data population took: " , data_pop_time , "seconds")
    print("Route Optimization took: ", route_time)
    print("Runtime is: " , all_time)
    
    trip_details.append(waypoints)
    trip_details.append(url)
    trip_details.append(route)
    return trip_details    #return waypoints and url   

def generate_url(waypoints):
    url = 'https://www.google.com/maps/dir/?api=1&'
    
    waypoint_ids = ''
    url_waypoints = ''
    
    for point in waypoints[:-1]:
        waypoint_ids += list(point.values())[0]['place_id'] + '|'
        # point_loc = str(point['geometry']['location']['lat']) + ',' + str(point['geometry']['location']['lat'])
        url_waypoints += list(point.values())[0]['name'] + '|'

    user_loc = str(user_info.lat) + ',' + str(user_info.lon)
    destination = list(waypoints[-1].values())[0]

    extension = {'origin': user_loc, 'destination': destination['name'], 'destination_place_id': destination["place_id"],\
                    'waypoints': url_waypoints, 'waypoint_place_ids': waypoint_ids, 'travelmode': user_info.transportation} 

    extension = urllib.parse.urlencode(extension)
    url += extension
    
    return url

def populate_waypoints(waypoints):
    global interest_places
    global food_places
    global user_info

    place_number_hint = math.ceil(user_info.trip_length / 60 * 1.25)
        # approximately 1.3 places per hour    

    for key in food_places:
        while True:
            place = random.choice(food_places[key])
            food_places[key].remove(place)
            if all(list(point.values())[0]['name'] != place['name'] for point in waypoints):
                waypoints.append({key: place})
                place_number_hint -= 1
                break

    for _ in range(place_number_hint):
        added = add_waypoint(waypoints)
        if not added:
            break

def optimize_route(waypoints):
    global interest_places
    global food_places
    global user_info

    time_spent = 100000           # arbitrarily large number for comparison
    route = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(find_directions, repeat(waypoints), waypoints)
        
        for temp_route in results:
            if not temp_route:
                return ({}, 0)
            time = calculate_time(temp_route)
            if time < time_spent:
                route = temp_route
                time_spent = time

    return (route, time_spent)

def calculate_time(route):
    global interest_places
    global food_places
    global user_info

    leg_duration = 0
    for route_index in range(len(route["legs"]) - 1):
        leg_duration += route["legs"][route_index]["duration"]["value"]/60

    return leg_duration + len(route["waypoint_order"]) * 40

# If successfully removed a waypoint, returns True
# If cannot remove any more waypoints, returns False
def remove_waypoint(waypoints):
    global interest_places
    global food_places
    global user_info

    if not waypoints:
        return False
    food_count = len(food_places)
    if waypoints[food_count:] != []:
        waypoint = random.choice(waypoints[food_count:])
    else:
        waypoint = random.choice(waypoints)
    waypoints.remove(waypoint)
    return True
    
# If successfully added a waypoint, returns True
# If cannot add any more waypoints, returns False
def add_waypoint(waypoints):
    global interest_places
    global food_places
    global user_info

    while True:
        if not interest_places:
            print("No interests left, could not add waypoint", file=sys.stderr)
            return False
        else:
            key = random.choice(list(interest_places))
            place = random.choice(list(interest_places[key]))
            interest_places[key].remove(place)
            if not interest_places[key]:
                del interest_places[key]
            if all(list(point.values())[0]['name'] != place['name'] for point in waypoints) and \
                'restaurant' not in place['types']:
                waypoints.append({key: place})
                return True                    

def find_directions(waypoints, destination):
    global interest_places
    global food_places
    global user_info

    user_loc = str(user_info.lat) + ',' + str(user_info.lon)
    
    transportation = user_info.transportation
    
    if transportation == 'cycling' or transportation == 'walking':
        avoid = "&avoid=highways"
    else:
        avoid = ''

    api_waypoints = ''
    for point in waypoints:
        api_waypoints += 'place_id:' + list(point.values())[0]['place_id'] + '|'
        
    endpoint       = 'https://maps.googleapis.com/maps/api/directions/json?'
    key            = 'AIzaSyDnNL7QG3n7CDhT1OfX4CCzbOW3KkudlVY'
    nav_request    = 'origin={}&destination=place_id:{}&mode={}{}&waypoints=optimize:true|{}&key={}'\
                        .format(user_loc, list(destination.values())[0]['place_id'], \
                                transportation, avoid, api_waypoints, key)

    response = json.loads(urllib.request.urlopen(endpoint + nav_request).read())

    if response['status'] == 'OK':
        route = response['routes'][0]
        return route
    else:
        toast("No Route Found")
        return {}    #return empty route