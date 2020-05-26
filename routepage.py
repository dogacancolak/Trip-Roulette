# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from kivy.garden.mapview import MapMarker

import trip
import concurrent.futures
import time
import webbrowser
import threading

waypoint_logos = {'restaurant': 'food-fork-drink', 'cafe': 'coffee', 'bar': 'glass-wine', 'bowling_alley': 'bowling', 'amusement_park': 'ferris-wheel', 'casino': 'cards-playing-outline', 'spa': 'spa-outline', 'night_club': 'party-popper', 'movie_theater': 'theater', 'tourist_attraction': 'camera-outline', 'art_gallery': 'image-frame', 'aquarium': 'jellyfish-outline'}

class Waypoint(MapMarker):
    pass

class RoutePage(Screen):
    map = ObjectProperty(None)

    def generate(self):

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        executor.submit(self.show_loading_page)

        # f2 = executor.submit(self.test_function)

        trip_details = []
        f2 = executor.submit(trip.generate_trip, trip_details)
        
        def callback(future, *args):
            self.show_route_page(trip_details)
            print("hes")

        f2.add_done_callback(callback)
            
            # trip_details   = f2.result()
            # self.waypoints = trip_details[0]
            # self.url       = trip_details[1]


    def show_route_page(self, trip_details):
        app = App.get_running_app()
        app.root.windows.current = app.root.routepage.name
        self.map.center_on(app.user_info.lat, app.user_info.lon)

        waypoints = trip_details[0]
        url       = trip_details[1]

        for point in waypoints:             # a 'point' is e.g. {'restaurant': json_place}
            place_type = next(iter(point))
            point = point[place_type]
            lat = point['geometry']['location']['lat']
            lon = point['geometry']['location']['lng']
            m   = Waypoint(lat=lat, lon=lon)

            if place_type in waypoint_logos:
                m.ids.logo.icon = waypoint_logos[place_type]

            self.map.add_marker(m)

        webbrowser.open(url)

    def show_loading_page(self, *args):
        app = App.get_running_app()

        app.root.homepage.dialog.dismiss()
        app.root.windows.current = app.root.loadingpage.name

    def test_function(self):
        time.sleep(1)