from kivy.app import App
from kivy.uix.screenmanager import Screen
import random
import math
from api_call import get_places_in_radius
import timeit

class RoutePage(Screen):

    def generate_trip(self):        
        user_info =  App.get_running_app().user_info

        interest_places = get_places_in_radius(user_info, user_info.interests)
        food_places     = get_places_in_radius(user_info, user_info.food)
    
        self.crop_list(interest_places, user_info.trip_length)
        self.crop_list(food_places, user_info.trip_length)

        all_places = []
        for key in interest_places:
            all_places += interest_places[key]
            
        for key in food_places:
            if key != 'restaurant':
                all_places += food_places[key]

        restaurants = food_places['restaurant']

        all_places = list({ each['id'] : each for each in all_places }.values())

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
        random.shuffle(complete_places)
        
        min_distance = 10000

        for i in range(round(len(complete_places)*0.37)):
            distance_lat = abs(curr_lat - complete_places[i]["geometry"]["location"]["lat"])
            distance_lon = abs(curr_lon - complete_places[i]["geometry"]["location"]["lng"])
            distance = math.sqrt(distance_lat**2 + distance_lon**2)
            if distance < min_distance:
                min_distance = distance
                dest_index = i

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

    def calculate_time_spent(self):
        return 40