# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.bubble import Bubble 
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage

# from amciks import waypoints, url, route
from waypoint_logos import waypoint_logos

from kivy.garden.mapview import MapMarkerPopup, MapMarker, MapView
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDIconButton
from kivymd.uix.toolbar import MDToolbar

import trip
import concurrent.futures
import time
import webbrowser
import threading
import urllib
import json
from functools import partial

class RouteMapView(MapView):
    pass
    
class WaypointDialog(Popup):
    pass

class Waypoint(MapMarker):
    pass

class PageToolbar(MDToolbar):
    pass

class RoutePage(Screen):
    map = ObjectProperty(None)
    waypoint_markers = []
    dialog = None

    def generate(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        executor.submit(self.show_loading_page)

        # f2 = executor.submit(self.test_function)

        trip_details = []
        f2 = executor.submit(trip.generate_trip, trip_details)
        
        def callback(future, *args):
            self.show_route_page(trip_details)


        f2.add_done_callback(callback) 

    def show_route_page(self, trip_details):
        app = App.get_running_app()
        app.root.windows.current = app.root.routepage.name
        self.map.center_on(app.user_info.lat, app.user_info.lon)

        gps_blinker = self.map.ids.blinker
        gps_blinker.blink()

        waypoints = trip_details[0]
        url       = trip_details[1]
        route     = trip_details[2]
        
        if not route:
            app.root.windows.return_homepage('right')
            return

        self.add_waypoint_markers(waypoints)

        self.center_map_on_route(route)
            
        self.ids.google_maps_button.url = url

    def add_waypoint_markers(self, waypoints):
        for index, point in enumerate(waypoints):             # a 'point' is e.g. {'restaurant': json_place}
            place_type = next(iter(point))
            point = point[place_type]
            lat = point['geometry']['location']['lat']
            lon = point['geometry']['location']['lng']
            m   = Waypoint(lat=lat, lon=lon)

            if place_type in waypoint_logos:
                outer_color = [color / 255 for color in waypoint_logos[place_type][2]] + [1]
                inner_color = [color / 255 for color in waypoint_logos[place_type][1]] + [1]
                m.ids.logo.icon = waypoint_logos[place_type][0]
                m.outer_color = outer_color
                m.inner_color = inner_color

            buttoncallback = partial(self.show_place_details, point, m)
            m.ids.logo.bind(on_press=buttoncallback)

            m.ids.waypoint_order.text = str(index + 1)

            self.map.add_marker(m)
            self.waypoint_markers.append(m)

    def remove_waypoint_markers(self):
        for m in self.waypoint_markers:
            self.map.remove_marker(m)
        self.waypoint_markers = []

    def center_map_on_route(self, route):
        sw_bounds = route['bounds']['southwest']
        ne_bounds = route['bounds']['northeast']

        route_area_center_lat = (sw_bounds['lat'] + ne_bounds['lat']) / 2
        route_area_center_lon = (sw_bounds['lng'] + ne_bounds['lng']) / 2

        # zoom out until route fits on the map
        for zoom in reversed(range(16)):    # max zoom is 15
            self.map.zoom = zoom
            self.map.center_on(route_area_center_lat, route_area_center_lon)
            x1, y1, x2, y2 = self.map.get_bbox()
            if x1 < sw_bounds['lat'] and y1 < sw_bounds['lng'] and x2 > ne_bounds['lat'] and y2 > ne_bounds['lng']:
                break

    def open_google_maps(self, url):
        webbrowser.open(url)

    def show_loading_page(self, *args):
        app = App.get_running_app()

        app.root.homepage.dialog.dismiss()
        app.root.windows.current = app.root.loadingpage.name

    def show_place_details(self, point, marker, instance):

        self.dialog = WaypointDialog(title=point['name'])

        request = 'https://maps.googleapis.com/maps/api/place/photo?'
        key     = 'key=AIzaSyDnNL7QG3n7CDhT1OfX4CCzbOW3KkudlVY'
        maxwidth = '&maxwidth=' + '1500'
        ref = '&photoreference=' + point['photos'][0]['photo_reference']
        source = request + key + ref + maxwidth + '&ext=.png'
        img = AsyncImage(source=source)
        self.dialog.add_widget(img)

        self.dialog.open()


    def test_function(self):
        time.sleep(1)