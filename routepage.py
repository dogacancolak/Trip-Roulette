from kivy.app import App
from kivy.uix.screenmanager import Screen
import random
from math import sin, cos, sqrt, atan2, radians
from api_call import get_places_in_radius
import timeit

class RoutePage(Screen):

    def generate_trip(self): 
        print("amcik")       
        user_info =  App.get_running_app().user_info

        interest_places = get_places_in_radius(user_info, user_info.interests)
        food_places     = get_places_in_radius(user_info, user_info.food)
    
        self.crop_list(interest_places, user_info.trip_length)
        self.crop_list(food_places, user_info.trip_length)

        all_places = []
        for key in interest_places:
            all_places += interest_places[key]
            
        restaurants = []
        for key in food_places:
            if key != 'restaurant':
                all_places += food_places[key]
            else:
                restaurants = food_places[key]

        all_places = list({ each['name'] : each for each in all_places }.values())

        route = self.find_optimal_route(all_places, restaurants, user_info.trip_length, user_info.lat, user_info.lon)

        for p in route:
            print(p["name"])     
   
        # for key in food_places:
        #     print("KEY: ", key)
        #     for place in food_places[key]:
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
        
        min_distance = 1000000
        dest_index = 0
        for i in range(round(len(complete_places))):
            new_lat = complete_places[i]["geometry"]["location"]["lat"]
            new_lon = complete_places[i]["geometry"]["location"]["lng"]
            distance = self.measure_distance(curr_lat, curr_lon, new_lat, new_lon)
            if distance < min_distance:
                min_distance = distance
                dest_index = i

        # print("len: ", len(complete_places))
        # print("index: ", dest_index)
        destination = complete_places[dest_index]

        time_left -= self.calculate_time_spent()

        if time_left > 0:
            if destination in restaurants:
                restaurants.clear()
            try:
                all_places.remove(destination)
            except ValueError:
                pass  # do nothing!
            new_lat = destination["geometry"]["location"]["lat"]
            new_lon = destination["geometry"]["location"]["lng"]
            return [destination] + self.find_optimal_route(all_places, restaurants, time_left, new_lat, new_lon)
        else:
            return []

    def measure_distance(self, lat1, lon1, lat2, lon2):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(52.2296756)
        lon1 = radians(21.0122287)
        lat2 = radians(52.406374)
        lon2 = radians(16.9251681)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
    
    def calculate_time_spent(self):
        return 40