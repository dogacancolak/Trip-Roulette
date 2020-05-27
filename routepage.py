# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from amciks import waypoints, url, route

from kivy.garden.mapview import MapMarkerPopup, MapMarker

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

        f2 = executor.submit(self.test_function)

        trip_details = []
        # f2 = executor.submit(trip.generate_trip, trip_details)
        
        def callback(future, *args):
            self.show_route_page(trip_details)


        f2.add_done_callback(callback) 

    def show_route_page(self, trip_details):
        app = App.get_running_app()
        app.root.windows.current = app.root.routepage.name
        self.map.center_on(app.user_info.lat, app.user_info.lon)

        # waypoints = trip_details[0]
        # url       = trip_details[1]
        # route     = trip_details[2]
        
        print(waypoints, '\n')
        print(url, '\n')
        print(route, '\n')

        if not route:
            app.root.windows.return_homepage()
            return

        self.add_waypoint_markers(waypoints)

        self.center_map_on_route(route)
            
        # webbrowser.open(url)

    def add_waypoint_markers(self, waypoints):
        for point in waypoints:             # a 'point' is e.g. {'restaurant': json_place}
            place_type = next(iter(point))
            point = point[place_type]
            lat = point['geometry']['location']['lat']
            lon = point['geometry']['location']['lng']
            m   = Waypoint(lat=lat, lon=lon)
            if place_type in waypoint_logos:
                m.ids.logo.icon = waypoint_logos[place_type]
            self.map.add_marker(m)

        # app = App.get_running_app()
        # print('hes')
        # m = MapMarkerPopup(lat=app.user_info.lat, lon=app.user_info.lon)

        # # m = Waypoint(lat=app.user_info.lat, lon=app.user_info.lon)
        # self.map.add_widget(m)

    def center_map_on_route(self, route):
        sw_bounds = route['bounds']['southwest']
        ne_bounds = route['bounds']['northeast']

        route_area_center_lat = (sw_bounds['lat'] + ne_bounds['lat']) / 2
        route_area_center_lon = (sw_bounds['lng'] + ne_bounds['lng']) / 2

        # zoom out until route fits on the map
        for zoom in reversed(range(18)):    # max zoom is 17
            self.map.zoom = zoom
            self.map.center_on(route_area_center_lat, route_area_center_lon)
            x1, y1, x2, y2 = self.map.get_bbox()
            if x1 < sw_bounds['lat'] and y1 < sw_bounds['lng'] and x2 > ne_bounds['lat'] and y2 > ne_bounds['lng']:
                break

    def show_loading_page(self, *args):
        app = App.get_running_app()

        app.root.homepage.dialog.dismiss()
        app.root.windows.current = app.root.loadingpage.name

    def test_function(self):
        time.sleep(1)


