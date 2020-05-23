# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import Screen
import random
from math import sin, cos, sqrt, atan2, radians, ceil
from api_call import get_places_in_radius
import timeit
import urllib.request
import json
import sys
import itertools
from kivymd.toast import toast
import time

class RoutePage(Screen):

    user_info = None
    interest_places = None
    food_places = None
    def generate_trip(self): 
        app = App.get_running_app()

        app.root.windows.return_homepage()

        print("george")
        time.sleep(2)
        print("mike")
        self.user_info = app.user_info

        print("entering first api call", file=sys.stderr)
        self.interest_places = get_places_in_radius(self.user_info, self.user_info.interests)
        self.food_places     = get_places_in_radius(self.user_info, self.user_info.food)
        print("exiting first api call", file=sys.stderr)
        
        if not self.interest_places and not self.food_places:
            toast("No places found nearby. Please expand your options.")
            return False
        
        print("adding waypoints", file=sys.stderr)

        waypoints = []
        self.populate_waypoints(waypoints)

        print("find directions", file=sys.stderr)

        route_details = self.optimize_route(waypoints)
        route = route_details[0]
        time_spent = route_details[1]
        print("while loops", file=sys.stderr)

        print("ordered:")
        for i in route['waypoint_order']:
            print(waypoints[i]['name'])

        print("Time spent: ", time_spent/60, file=sys.stderr)
        
    def populate_waypoints(self, waypoints):
        place_number_hint = ceil(self.user_info.trip_length / 60 * 1.3)
         # approximately 1.4 places per hour

        for key in self.food_places:
            while True:
                place = random.choice(self.food_places[key])    
                if all(point['name'] != place['name'] for point in waypoints):
                    waypoints.append(place)
                    place_number_hint -= 1
                    break
        print("adding interests", file=sys.stderr)

        for _ in range(place_number_hint):
            added = self.add_waypoint(waypoints)
            if not added:
                break


    def optimize_route(self, waypoints):

        time_spent = 100000           # arbitrarily large number for comparison
        for point in waypoints:
            temp_route = self.find_directions(waypoints, point)
            time = self.calculate_time(temp_route)
            if time < time_spent:
                route = temp_route
                time_spent = time

        entered = False
        while time_spent > self.user_info.trip_length + 15:
            removed = self.remove_waypoint(waypoints)
            if not removed:
                break
            else:
                route_details = self.optimize_route(waypoints)
                route = route_details[0]
                time_spent = route_details[1]
            entered = True
            print("trip length too long", file=sys.stderr)

        if not entered:
            while time_spent < self.user_info.trip_length - 40:
                added = self.add_waypoint(waypoints)
                if not added:
                    break
                else:
                    route_details = self.optimize_route(waypoints)
                    route = route_details[0]
                    time_spent = route_details[1]
                   
                print("trip length too short", file=sys.stderr)

        return (route, time_spent)

    def calculate_time(self, route):
        leg_duration = 0
        for route_index in range(len(route["legs"]) - 1):
            leg_duration += route["legs"][route_index]["duration"]["value"]/60

        return leg_duration + len(route["waypoint_order"]) * 40

    # If successfully removed a waypoint, returns True
    # If cannot remove any more waypoints, returns False
    def remove_waypoint(self, waypoints):
        if not waypoints:
            return False
        food_count = len(self.food_places)
        if waypoints[food_count:] != []:
            waypoint = random.choice(waypoints[food_count:])
        else:
            waypoint = random.choice(waypoints)
        waypoints.remove(waypoint)
        return True
        
    # If successfully added a waypoint, returns True
    # If cannot add any more waypoints, returns False
    def add_waypoint(self, waypoints):
        while True:
            if not self.interest_places:
                return False
            else:
                key = random.choice(list(self.interest_places))
                place = random.choice(list(self.interest_places[key]))
                self.interest_places[key].remove(place)
                if not self.interest_places[key]:
                    del self.interest_places[key]
                if all(point['name'] != place['name'] for point in waypoints) and \
                    'restaurant' not in place['types']:
                    waypoints.append(place)
                    return True                    

    def find_directions(self, waypoints, destination):
        
        user_loc = str(self.user_info.lat) + ',' + str(self.user_info.lon)
        
        transportation = self.user_info.transportation
        
        if transportation == 'cycling' or transportation == 'walking':
            avoid = "&avoid=highways"
        else:
            avoid = ''

        api_waypoints = ''
        for point in waypoints:
            api_waypoints += 'place_id:' + point['place_id'] + '|'
            
        endpoint       = 'https://maps.googleapis.com/maps/api/directions/json?'
        key            = 'AIzaSyA4H5RbPwYejTlXVI1hjio_4q4XYS_Ubts'
        nav_request    = 'origin={}&destination=place_id:{}&mode={}{}&waypoints=optimize:true|{}&key={}'\
                            .format(user_loc, destination['place_id'], \
                                    transportation, avoid, api_waypoints, key)

        response = json.loads(urllib.request.urlopen(endpoint + nav_request).read())

        if response['status'] == 'OK':
            route = response['routes'][0]
            return route
        else:
            print("no route found")


    # def remove_duplicates(self, dict_raw):
    #     filtered_dict = {}
    #     for key in dict_raw:
    #         # print("key is: ", key, file=)
    #         filtered_list = []
    #         for p in dict_raw[key]:
    #             duplicate = False
    #             if p in itertools.chain(*filtered_dict.values()):
    #                     duplicate = True
    #                     break
    #             if not duplicate:
    #                 if 'restaurant' not in p['types'] or p in itertools.chain(*self.food_places.values()):
    #                     filtered_list.append(p)
    #         if filtered_list:
    #             filtered_dict[key] = filtered_list

    #     dict_raw = filtered_dict