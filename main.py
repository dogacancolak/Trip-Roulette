from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd import images_path
from kivymd.toast import toast

from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix import MDAdaptiveWidget
from kivymd.uix.button import MDIconButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd.uix.dropdownitem import MDDropDownItem

from gpshelper import GpsHelper

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

class SettingsButton(MDIconButton):
    pass

class PageToolbar(MDToolbar):
    pass

class FormPage(Screen):
    pass

class LogPage(Screen):
    pass

class HelpPage(Screen):
    pass


class DetailsPage(Screen):
    pass

class DialogContent(BoxLayout):
    dietary_restrictions = None
    def on_switch_active(self, switch, value):
        if value:
            App.get_running_app().food = True
            self.dietary_restrictions = MDDropDownItem(
                id="dietary",
                pos_hint= {'right': 1, 'top': 1}
            )
            self.dietary_restrictions.set_item("None")
            self.dietary_restrictions.set_item("Vegetarian/Vegan")
            self.ids.content_layout.add_widget(self.dietary_restrictions)
        else:
            App.get_running_app().food = False
            if self.dietary_restrictions:
                self.ids.content_layout.remove_widget(self.dietary_restrictions)

class PopupDialog(Popup):
    pass

class HomePage(Screen):
    map = ObjectProperty(None)
    dialog = None

    def toast_pop(self, instance):
        toast(instance.icon)

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

class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    nav_drawer = ObjectProperty(None)
    windows = ObjectProperty(None)
    homepage = ObjectProperty(None)

class TripRouletteApp(MDApp): 
    data = {
            'car':  'Car',
            'walk': 'Walk',
            'bus':  'Public Transport',
            }

    food = BooleanProperty()
            
    def return_homepage(self):
            self.root.windows.current = "HomePage"
            self.root.windows.current_screen.manager.transition.direction = "left"

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"

    def on_start(self):
        icons_item = {
            "account": "Account Details",
            "city-variant-outline": "Form",
            "login": "Log Out/Log In",
            "help": "Help",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )
    
        # Initialize GPS
        GpsHelper().run()


TripRouletteApp().run()