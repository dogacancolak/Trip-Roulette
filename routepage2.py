from kivy.app import App
from kivy.uix.screenmanager import Screen
import random
from math import sin, cos, sqrt, atan2, radians
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
       

        # self.crop_list(self.interest_places, user_info.trip_length)
        # self.crop_list(self.food_places, user_info.trip_length)

        for key in self.interest_places:
            for p in self.interest_places[key]:
                if 'restaurant' not in p['types']:
                    print(key, ": ", p['name'])

        for key in self.food_places:
            for p in self.food_places[key]:
                if 'restaurant' not in p['types'] or key == 'restaurant':
                    print(key, ": ", p['name'])
    
        # all_places = []
        # for key in self.interest_places:
        #     all_places += self.interest_places[key]
            
        # restaurants = []
        # for key in self.food_places:
        #     if key != 'restaurant':
        #         all_places += self.food_places[key]
        #     else:
        #         restaurants = self.food_places[key]

        # all_places = list({ each['name'] : each for each in all_places }.values())
        # restaurants = list({ each['name'] : each for each in restaurants }.values())

        # # print(len(all_places))
        # route = self.find_optimal_route(all_places, restaurants, user_info.trip_length, user_info.lat, user_info.lon)

        # for p in all_places:
        #     print(p["name"])
               
        # for key in self.food_places:
        #     print("KEY: ", key)
        #     for place in self.food_places[key]:
        #             print("Name: ", place["name"])

    def crop_list(self, places_dict, trip_duration):
        duration_weight = round(trip_duration / 60) * 5  # 5 options to choose from per hour
        for place_key in places_dict:
            if len(places_dict[place_key]) > duration_weight:
                places_sample = random.sample(places_dict[place_key], k = duration_weight)
                places_dict[place_key] = places_sample

    def find_optimal_route(self, all_places, restaurants, time_left, curr_lat, curr_lon):
        complete_places = all_places + restaurants

        if not complete_places: # if complete_places is empty, end route
            return []

        random.shuffle(complete_places)
        
        fitting_direction_not_found = True
        while fitting_direction_not_found:
            min_distance = 1000000
            all_distances = []
            for i in range(len(complete_places)):
                new_lat = complete_places[i]["geometry"]["location"]["lat"]
                new_lon = complete_places[i]["geometry"]["location"]["lng"]
                distance = self.measure_distance(curr_lat, curr_lon, new_lat, new_lon)
                all_distances += [distance]
                if distance < min_distance and distance != 0:
                    min_distance = distance
                    dest_index = i

            destination = complete_places[dest_index]
            route = self.find_directions(curr_lat, curr_lon, destination)
            if self.route_fits_in_radius(route):
                fitting_direction_not_found = False
            
        time_left -= self.calculate_time_spent(route, destination)

        if time_left > 0:
            if destination in restaurants:
                restaurants.clear()
                for p in all_places:
                    if 'restaurant' in p['types']:
                        all_places.remove(p)
            else:
                all_places.remove(destination)
            new_lat = destination["geometry"]["location"]["lat"]
            new_lon = destination["geometry"]["location"]["lng"]
            return [destination] + self.find_optimal_route(all_places, restaurants, time_left, new_lat, new_lon)
        else:
            return []

    def measure_distance(self, lat1, lon1, lat2, lon2):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
    
    def route_fits_in_radius(self, route):

        user_info =  App.get_running_app().user_info
        user_lat  = user_info.lat
        user_lng  = user_info.lon
        radius    = user_info.radius * 0.001    # in km

        # print(route['routes'], file=sys.stderr)
        ne_lat = route['routes'][0]['bounds']['northeast']['lat']
        ne_lng = route['routes'][0]['bounds']['northeast']['lng']
        sw_lat = route['routes'][0]['bounds']['southwest']['lat']
        sw_lng = route['routes'][0]['bounds']['southwest']['lng']

        ne_distance = self.measure_distance(user_lat, user_lng, ne_lat, ne_lng)
        sw_distance = self.measure_distance(user_lat, user_lng, sw_lat, sw_lng)

        if ne_distance > radius or sw_distance > radius:
            return False
        else:
            return True
        
    def find_directions(self, origin_lat, origin_lon, destination):
        
        user_info =  App.get_running_app().user_info
        
        key            = 'AIzaSyA4H5RbPwYejTlXVI1hjio_4q4XYS_Ubts'
        endpoint       = 'https://maps.googleapis.com/maps/api/directions/json?'
        
        avoid = ''
        transportation = user_info.transportation
        if transportation == 'cycling' or transportation == 'walking':
            avoid = "&avoid=highways"
      
      
        origin_loc = str(origin_lat) + ',' + str(origin_lon)
        dest_lat = destination["geometry"]["location"]["lat"]
        dest_lon = destination["geometry"]["location"]["lng"]
        dest_loc = str(dest_lat) + ',' + str(dest_lon)

        nav_request    = "origin={}&destination={}&mode={}{}&key={}"\
                            .format(origin_loc, dest_loc, \
                                    transportation, avoid, key)

        response = json.loads(urllib.request.urlopen(endpoint + nav_request).read())

        return response

    def calculate_time_spent(self, response, destination):
        
        for key in self.interest_places:
            if destination in self.interest_places[key]:
                time_spent_in_destination = 50
        for key in self.food_places:
            if destination in self.food_places[key]:
                time_spent_in_destination = 40

        return response["routes"][0]["legs"][0]["duration"]["value"] / 60 + time_spent_in_destination