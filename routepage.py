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

        print("entering first api call", file=sys.stderr)
        self.interest_places = get_places_in_radius(user_info, user_info.interests)
        self.food_places     = get_places_in_radius(user_info, user_info.food)
        print("exiting first api call", file=sys.stderr)

        temp_dict = {}
        for key in self.interest_places:
            temp_list = []
            for p in self.interest_places[key]:
                if 'restaurant' not in p['types']:
                    temp_list.append(p)
            if temp_list:
                temp_dict[key] = temp_list
        self.interest_places = temp_dict
        
        self.interest_places = self.remove_duplicates(self.interest_places)
        self.food_places     = self.remove_duplicates(self.food_places)

        place_number_hint = ceil(user_info.trip_length / 60 * 1.4)
         # approximately 1.4 places per hour

        print("adding waypoints", file=sys.stderr)

        waypoints = []
        for key in self.food_places:
            place = random.choice(self.food_places[key])
            waypoints.append(place)
            place_number_hint -= 1

        print("adding interests", file=sys.stderr)

        for _ in range(place_number_hint):
            added = self.add_waypoint(waypoints)
            if not added:
                break
        print("find directions", file=sys.stderr)

        route = self.find_directions(waypoints)
        time_spent = self.calculate_time(route)
        print("while loops", file=sys.stderr)

        entered = False
        while time_spent > user_info.trip_length + 15:
            self.remove_waypoint(waypoints)
            route = self.find_directions(waypoints)
            time_spent = self.calculate_time(route)
            entered = True

            print("trip length too long", file=sys.stderr)

        if not entered:
            while time_spent < user_info.trip_length - 40:
                added = self.add_waypoint(waypoints)
                if not added:
                    break
                else:
                    route = self.find_directions(waypoints)
                    time_spent = self.calculate_time(route)
                print("trip length too short", file=sys.stderr)

        print("unordered:")
        for p in waypoints:
            print(p['name'])
        print("\nordered:")
        for i in route['waypoint_order']:
            print(waypoints[i]['name'])

    def calculate_time(self, route):
        leg_duration = 0
        for route_index in range(len(route["legs"]) - 1):
            leg_duration += route["legs"][route_index]["duration"]["value"]/60

        return leg_duration + len(route["waypoint_order"]) * 40

    def remove_waypoint(self, waypoints):
        food_count = len(self.food_places)
        if waypoints[food_count:] != []:
            waypoint = random.choice(waypoints[food_count:])
        elif waypoints != []:
            waypoint = random.choice(waypoints)
        else:
            print("no interests/food", file=sys.stderr)
        waypoints.remove(waypoint)
        
    # If successfully added a waypoint, returns True
    # If cannot add any more wapoints, returns False
    def add_waypoint(self, waypoints):
        if not self.interest_places:
            return False
        else:
            successful = False
            while not successful:
                key = random.choice(list(self.interest_places))
                place = random.choice(list(self.interest_places[key]))
                if place not in waypoints:  # check if whole list is in the list
                    waypoints.append(place)
                    return True
        
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

        if response['status'] == 'OK':
            route = response['routes'][0]
            return route
        else:
            print("no route found")