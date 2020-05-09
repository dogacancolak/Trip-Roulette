from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix import MDAdaptiveWidget
from kivymd.theming import ThemeManager
from gpshelper import GpsHelper
from kivymd.toast import toast

class ContentNavigationDrawer(BoxLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.text_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.text_color

class TripRouletteApp(MDApp): 
    map = ObjectProperty(None)

    data = {
            'car':  'Car',
            'walk': 'Walk',
            'bus':  'Public Transport',
            }
    def toast_pop(self, instance):
            toast(instance.icon)
            pass
        
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        
    def on_start(self):
        icons_item = {
            "account": "Account Details",
            "city-variant-outline": "Preferences",
            "login": "Log Out/ Log In",
            "help": "Help",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )
        # Initialize GPS
        GpsHelper().run()


TripRouletteApp().run()