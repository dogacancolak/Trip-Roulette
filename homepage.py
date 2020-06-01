from kivy.app import App
from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd import images_path
from kivymd.toast import toast
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDIconButton, MDFloatingRootButton
from kivy.graphics import *

from kivy.utils import platform
if platform == "ios":
    from os.path import join, dirname
    import kivy.garden
    kivy.garden.garden_app_dir = join(dirname(__file__), "libs", "garden")
    
from kivy.garden.mapview import MapMarkerPopup, MapMarker, MapView

from geopy import distance

class HomeMapView(MapView):
    pass

class SettingsButton(MDIconButton):
    pass

class SearchCircle(Widget):
    def set_search_radius(self):
        app = App.get_running_app()
        search_circle = app.root.homepage.circle
        map = app.root.homepage.map

        outer_circle = search_circle.canvas.get_group('a')[0]
        radius_in_pixels = outer_circle.size[0] / 2

        outer_coords = map.get_latlon_at(search_circle.center_x - radius_in_pixels, search_circle.center_y)
        user_coords  = map.get_latlon_at(search_circle.center_x, search_circle.center_y)

        radius_in_meters = distance.distance(outer_coords, user_coords).km * 1000

        app.user_info.radius = radius_in_meters

class FoodOption(BoxLayout):
    def update_food_options(self, switch, value):
        food = App.get_running_app().user_info.food

        # Convert switch.title in the UI to index strings in our program
        # e.g. 'Restaurants' to 'restaurant'
        place_type = switch.title.lower()[:-1]

        if value:
            if place_type not in food:
                food.append(place_type)
        else:
            if place_type in food:
                food.remove(place_type)

class DialogContent(BoxLayout):
    def update_slider_values(self, slider, value, id):
        user_info = App.get_running_app().user_info
        value = round(value)

        if id == 'duration':
            user_info.trip_length = value * 60

        elif id == 'budget':
            user_info.budget = value - 1    # our range 1-5 to Google's 0-4

class PopupDialog(Popup):
    pass

class TransportOptions(MDFloatingActionButtonSpeedDial):

    def update_transport(self, instance):
        app = App.get_running_app()
        selection = instance.icon
        circle = app.root.homepage.circle
        map = app.root.homepage.map
        x = circle.center_x
        y = circle.center_y
        if selection == 'bicycle':
            transport = 'cycling'
            map.zoom = 14
        elif selection == 'car':
            transport = 'driving'
            map.zoom = 11
        elif selection == 'bus':
            transport = 'transit'
            map.zoom = 12
        elif selection == 'walk':
            transport = 'walking'
            map.zoom = 15

        self.icon = selection
        self.close_stack()
        app.user_info.transportation = transport

class HomePage(Screen):
    map = ObjectProperty(None)
    dialog = None
    circle = ObjectProperty(None)
    speed_dial = ObjectProperty(None)

    def get_speed_dial_root_button(self):
        for widget in self.speed_dial.children:
            if isinstance(widget, MDFloatingRootButton):
                return widget

    def toast_pop(self):
        toast("Please include at least one interest")

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = PopupDialog(
                title='Trip Details', 
                content=DialogContent(),
                )
        self.dialog.open()