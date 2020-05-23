from kivy.app import App
from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd import images_path
from kivymd.toast import toast
from kivymd.uix.button import MDFloatingActionButtonSpeedDial

class FoodOption(BoxLayout):
    def update_food_options(self, switch, value):
        food = App.get_running_app().user_info.food

        # Convert switch.title in the UI to index strings in our program
        # e.g. 'Restaurants' to 'restaurant'
        place_type = switch.title.lower()[:-1]

        if value:
            if place_type not in food:
                food.append(place_type)
                if place_type == 'bar':
                    food.append('pub')
        else:
            if place_type in food:
                food.remove(place_type)
                if place_type == 'bar':
                    food.remove('pub')

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
        selection = instance.icon

        if selection == 'bicycle':
            transport = 'cycling'
            radius    =  800
        elif selection == 'car':
            transport = 'driving'
            radius    = 5000
        elif selection == 'bus':
            transport = 'transit'
            radius    = 3000
        elif selection == 'walk':
            transport = 'walking'
            radius    = 400

        self.icon = selection
        self.close_stack()
        App.get_running_app().user_info.transportation = transport
        App.get_running_app().user_info.radius = radius

class HomePage(Screen):
    map = ObjectProperty(None)
    dialog = None

    def call_toast(self):
        toast("Please include at least one interest")

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = PopupDialog(
                title='Trip Details', 
                content=DialogContent(),
                )
        self.dialog.open()