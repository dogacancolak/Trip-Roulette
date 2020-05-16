from kivy.app import App
from kivy.uix.screenmanager import Screen

from api_call import get_places_in_radius
import timeit

class RoutePage(Screen):

    def generate_trip(self):
        # start = timeit.default_timer()
        app = App.get_running_app()
        user_info = app.user_info
        
        interest_places = get_places_in_radius(user_info, user_info.interests)
        food_places     = get_places_in_radius(user_info, user_info.food)
        
        # stop = timeit.default_timer()
        # for p in interest_places:
        #     print("\nResult AMK")
        #     for res in p:
        #         print("Name: ", res["name"])
        
        # print("yemeks memeks")
        
        # for p in food_places:
        #     print("\nResult AMK")
        #     for res in p:
        #         print("Name: ", res["name"])        

        # print('Total Time: ', stop - start) 
      

# 4.5 + 6.4 + 5.4 

