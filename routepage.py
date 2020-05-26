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

class Waypoint(MapMarker):
    pass

class RoutePage(Screen):
    map = ObjectProperty(None)
    waypoints = None
    url = None

    def show_route_page(self):
        # threading.Thread(target=self.show_loading_page).start()
        # trip_details   = trip.generate_trip()
        # print(trip_details)

        # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        executor.submit(self.show_loading_page)
            
        # f2 = executor.submit(self.test_function)

        trip_details = []
        f2 = executor.submit(trip.generate_trip, trip_details)
        

            
        def done_callback(future, *args):
            app = App.get_running_app()
            app.root.windows.current = app.root.routepage.name
            self.map.center_on(app.user_info.lat, app.user_info.lon)
            print(trip_details)

        f2.add_done_callback(done_callback)
            
            # trip_details   = f2.result()
            # self.waypoints = trip_details[0]
            # self.url       = trip_details[1]

        # trip_details   = f2.result()
        # self.waypoints = trip_details[0]
        # self.url       = trip_details[1]

        # app = App.get_running_app()
        # app.root.windows.current = app.root.routepage.name
        # self.map.center_on(app.user_info.lat, app.user_info.lon)

        # webbrowser.open(url)

    def show_loading_page(self, *args):
        app = App.get_running_app()

        app.root.homepage.dialog.dismiss()
        app.root.windows.current = app.root.loadingpage.name

    def test_function(self):
        time.sleep(1)