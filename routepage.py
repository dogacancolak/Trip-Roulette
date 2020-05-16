from kivy.app import App
from kivy.uix.screenmanager import Screen
import random

from api_call import get_places_in_radius
import timeit

class RoutePage(Screen):
    app = App.get_running_app()
    user_info = app.user_info

    def generate_trip(self):        
        user_info = self.user_info

        interest_places = get_places_in_radius(user_info, user_info.interests)
        food_places     = get_places_in_radius(user_info, user_info.food)
    
        crop_list(interest_places, user_info.trip_duration)
        crop_list(food_places, user_info.trip_duration)

        all_places = []
        for key in interest_places:
            all_places += interest_places[key]
            
        for key in food_places:
            if key != 'restaurant':
                all_places += food_places[key]

        restaurants = food_places['restaurant']

        find_optimal_route(all_places, restaurants, user_info.lat, user_info.lon)
        # for key in food_places:
        #     print("KEY: ", key)
        #     for place in food_places[key]:
        #             print("Name: ", place["name"])

    
    def crop_list(places_dict, trip_duration):
        duration_weight = trip_duration * 5  # 5 options to choose from per hour

        for place_key in places_dict:
            if len(places_dict[place_key]) > duration_weight:
                places_sample = random.sample(places_dict[place_key], k = duration_weight)
                places_dict[place_key] = places_sample


    def find_optimal_route(all_places, restaurants, curr_lat, curr_lon):
        user_info = self.user_info
        complete_places = all_places + restaurants
        random.shuffle(complete_places)
        
        min_distance = 10000
        len_so_far = 0
        
        route = [] 
        #We accumulate data on the set
        for i in round((len(complete_places)*37)/100):
            distance_lat = abs(curr_lat - complete_places[i]["geometry"]["location"]["lat"]])
            distance_lon = abs(curr_lon - comeplete_places[i]["geometry"]["location"]["lon"]])
            distance = sqrt(distance_lat^2 + distance_lon)
            if distance < min_distance[0]:
                min_distance = distance
            
        
        #We start deciding 
        while True:
            distance_lat = abs(curr_lat - complete_places[len_so_far]["geometry"]["location"]["lat"]])
            distance_lon = abs(curr_lon - complete_places[len_so_far]["geometry"]["location"]["lon"]])
            distance = sqrt(distance_lat^2 + distance_lon^2)

            if distance < min_distance[0]:
                route.add(complete_places[len_so_far])
                
                if comeplete_places[len_so_far] in restaurants:
                    complete_places = all_places
                    restaurants.clear()
                find_optimal_route(all_places, restaurants, distance_lat, distance_lon)
                break
            else:
                len_so_far = len_so_far + 1

        

        