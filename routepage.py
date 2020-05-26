# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from kivy.garden.mapview import MapMarker

import trip
import concurrent.futures
import time

class Waypoint(MapMarker):
    pass

class RoutePage(Screen):
    map = ObjectProperty(None)

    def show_route_page(self):

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        executor.submit(self.show_loading_page)
        f2 = executor.submit(trip.generate_trip)
        # f2 = executor.submit(self.test_function)

        def done_callback(future_obj, *args):
            app = App.get_running_app()
            app.root.windows.current = app.root.routepage.name
            self.map.center_on(app.user_info.lat, app.user_info.lon)
            

        f2.add_done_callback(done_callback)
  
    def show_loading_page(self):
        app = App.get_running_app()

        app.root.homepage.dialog.dismiss()
        app.root.windows.current = app.root.loadingpage.name

    def test_function(self):
        time.sleep(1)