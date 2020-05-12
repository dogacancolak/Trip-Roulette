from kivy.app import App
from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd import images_path
from kivymd.toast import toast

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
            user_info.trip_length = value

        elif id == 'budget':
            user_info.budget = value - 1    # our range 1-5 to Google's 0-4

class PopupDialog(Popup):
    pass

class HomePage(Screen):
    map = ObjectProperty(None)
    dialog = None

    def update_transport(self, instance):
        selection = instance.icon
        
        if selection == 'bicycle':
            transport = 'cycling'
        elif selection == 'car':
            transport = 'driving'
        elif selection == 'bus':
            transport = 'transit'
        elif selection == 'walk':
            transport = 'walking'

        instance.parent.icon = selection
        App.get_running_app().user_info.transportation = transport
        
        print(App.get_running_app().user_info.transportation)

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = PopupDialog(
                title='Trip Details',
                content=DialogContent(),
                )
            # self.dialog = PopupDialog(
            #     title="Details:",
            #     type="custom",
            #     content_cls= DialogContent(),
            #     buttons=[
            #         MDFlatButton(
            #             text="CANCEL", text_color= App.get_running_app().theme_cls.primary_color
            #         ),
            #         MDFlatButton(
            #             text="OK", text_color= App.get_running_app().theme_cls.primary_color
            #         ),
            #     ],
            # )
        self.dialog.open()