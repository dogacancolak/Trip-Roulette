from kivy.app import App
from kivy.uix.screenmanager import Screen
import random
from math import sin, cos, sqrt, atan2, radians, ceil
from api_call import get_places_in_radius
import timeit
import urllib.request
import json
import sys

class RoutePage(Screen):

    interest_places = None
    food_places = None
    def generate_trip(self): 
        
        user_info =  App.get_running_app().user_info

        self.interest_places = get_places_in_radius(user_info, user_info.interests)
        self.food_places     = get_places_in_radius(user_info, user_info.food)
       
        self.interest_places = self.remove_duplicates(self.interest_places)
        self.food_places     = self.remove_duplicates(self.food_places)

        place_number_hint = ceil(user_info.trip_length / 60 * 1.4)
         # approximately 1.4 places per hour
        
        waypoints = []
        for key in self.food_places:
            place = random.choice(self.food_places[key])
            waypoints.append(place)
            place_number_hint -= 1

        for _ in range(place_number_hint):
            successful = False
            while not successful:
                key = random.choice(list(self.interest_places))
                place = random.choice(list(self.interest_places[key]))
                if place not in waypoints or 'restaurant' not in place['types']:
                    waypoints.append(place) 
                    successful = True
        
        waypoints = list({ each['place_id'] : each for each in waypoints }.values())

        directions = self.find_directions(waypoints)

        if directions['status'] == 'OK':
            route = directions['routes'][0]
        else:
            print("no route found")

        print("unordered:")
        for p in waypoints:
            print(p['name'])
        print("\nordered:")
        for i in route['waypoint_order']:
            print(waypoints[i]['name'])

    def remove_duplicates(self, dict_raw):
        filtered = {}

        for key, value in dict_raw.items():
            if value not in filtered.values():
                filtered[key] = value

        return filtered

    def find_directions(self, waypoints):
        
        user_info =  App.get_running_app().user_info
        user_loc = str(user_info.lat) + ',' + str(user_info.lon)
        
        transportation = user_info.transportation
        
        if transportation == 'cycling' or transportation == 'walking':
            avoid = "&avoid=highways"
        else:
            avoid = ''

        api_waypoints = ''
        for point in waypoints:
            api_waypoints += 'place_id:' + point['place_id'] + '|'
            
        endpoint       = 'https://maps.googleapis.com/maps/api/directions/json?'
        key            = 'AIzaSyA4H5RbPwYejTlXVI1hjio_4q4XYS_Ubts'
        nav_request    = 'origin={}&destination={}&mode={}{}&waypoints=optimize:true|{}&key={}'\
                            .format(user_loc, user_loc, \
                                    transportation, avoid, api_waypoints, key)

        response = json.loads(urllib.request.urlopen(endpoint + nav_request).read())

        return response