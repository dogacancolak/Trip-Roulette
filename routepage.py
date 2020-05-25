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
import threading
import concurrent.futures
from kivy.clock import Clock, mainthread
import time
from itertools import repeat
import urllib

loading_label_texts = ["Selecting locations...", "Optimizing route..."]

class RoutePage(Screen):

    interest_places = {}
    food_places = {}
    user_info = None

    def show_route_page(self):

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        f1 = executor.submit(self.show_loading_page)
        f2 = executor.submit(self.generate_trip)
        
        def done_callback(self, *args):
            app = App.get_running_app()
            app.root.windows.current = app.root.routepage.name

        f2.add_done_callback(done_callback)

    def show_loading_page(self):
        app = App.get_running_app()

        app.root.homepage.dialog.dismiss()
        app.root.windows.current = app.root.loadingpage.name

    def change_loading_label(self, *args):
        app = App.get_running_app()
        if loading_label_texts:
            text = loading_label_texts[0]
            app.root.loadingpage.ids.loading_label.text = text
            loading_label_texts.remove(text)
         
    def generate_trip(self): 
        app = App.get_running_app()
        user_info = app.user_info
        self.user_info = user_info

        trigger = Clock.create_trigger(self.change_loading_label)
        results = []
        start = time.time()
        print("entering api", file=sys.stderr)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            combined_locations = user_info.interests + user_info.food
            results = executor.map(get_places_in_radius, repeat(user_info), combined_locations)

            for dictionary in results:
                if dictionary:
                    key = next(iter(dictionary))
                    if key in user_info.food:
                        self.food_places.update(dictionary)
                    elif key in user_info.interests:
                        self.interest_places.update(dictionary)
                    else:
                        print("sicmisiniz")

        data_pop_time = time.time() - start
        count = 0
        for value in self.food_places.values():
            count += len(value)
        for value in self.interest_places.values():
            count += len(value)          

        print("number of interest + food: ", count)
        
        
        if not self.interest_places and not self.food_places:
            toast("No places found nearby. Please expand your options.")
            return False
        
        print("adding waypoints", file=sys.stderr)

        waypoints = []
        self.populate_waypoints(waypoints)

        print("find directions", file=sys.stderr)

        trigger()
        route_start_time = time.time()

       
        route_details = self.optimize_route(waypoints)
        route = route_details[0]
        time_spent = route_details[1]

        entered = False
        while time_spent > user_info.trip_length + 15:
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
            while time_spent < user_info.trip_length - 40:
                added = self.add_waypoint(waypoints)
                if not added:
                    
                    break
                else:
                    route_details = self.optimize_route(waypoints)
                    route = route_details[0]
                    time_spent = route_details[1]
                   
                print("trip length too short", file=sys.stderr)

        route_time = time.time() - route_start_time
        print("while loops", file=sys.stderr)

        waypoints = [waypoints[i] for i in route['waypoint_order']]
        for p in waypoints:
            print(p['name'])
            
        url = 'https://www.google.com/maps/dir/?api=1&'
        
        user_loc = str(self.user_info.lat) + ',' + str(self.user_info.lon)
        # dest_loc = str(waypoints[-1]['geometry']['location']['lat']) + ',' + str(waypoints[-1]['geometry']['location']['lat'])
        waypoint_ids = ''
        url_waypoints = ''
        
        for point in waypoints[:-1]:
            waypoint_ids += point['place_id'] + '|'
            # point_loc = str(point['geometry']['location']['lat']) + ',' + str(point['geometry']['location']['lat'])
            url_waypoints += point['name'] + '|'

        extension = {'origin': user_loc, 'destination': waypoints[-1]['name'], 'destination_place_id': waypoints[-1]["place_id"],\
                     'waypoints': url_waypoints, 'waypoint_place_ids': waypoint_ids, 'travelmode': user_info.transportation} 

        extension = urllib.parse.urlencode(extension)

        url += extension
        print(url)   

        print("Time spent: ", time_spent/60, file=sys.stderr)
        
        all_time = time.time() - start
        print("Data population took: " , data_pop_time , "seconds")
        print("Route Optimization took: ", route_time)
        print("Runtime is: " , all_time)
        
    def populate_waypoints(self, waypoints):
    
        place_number_hint = ceil(self.user_info.trip_length / 60 * 1.25)
         # approximately 1.3 places per hour    
        
        for key in self.food_places:
            while True:
                place = random.choice(self.food_places[key])    
                if all(point['name'] != place['name'] for point in waypoints):
                    waypoints.append(place)
                    place_number_hint -= 1
                    break

        for _ in range(place_number_hint):
            added = self.add_waypoint(waypoints)
            if not added:
                break

    def optimize_route(self, waypoints):
        time_spent = 100000           # arbitrarily large number for comparison
        route = None
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.find_directions, repeat(waypoints), waypoints)
            
            for temp_route in results:
                time = self.calculate_time(temp_route)
                if time < time_spent:
                    route = temp_route
                    time_spent = time

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
                print("No interests left, could not add waypoint", file=sys.stderr)
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