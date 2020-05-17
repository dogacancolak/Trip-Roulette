from kivy.app import App

from kivy.uix.screenmanager import Screen

from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd import images_path

from kivymd.uix.list import IRightBodyTouch
from kivymd.uix import MDAdaptiveWidget
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.properties import ListProperty

class PageToolbar(MDToolbar):
    pass

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    # places = ListProperty()

    def update_interests(self, switch, value):
        interests = App.get_running_app().user_info.interests

        # Convert switch.title in the UI to index strings in our program
        # e.g. 'Restaurants' to 'restaurant'
        interest_types = switch.title
        
        already_interested = all(elem in interests  for elem in interest_types)
        
        if value:
            if not already_interested:
                interests.extend(interest_types)
        else:
            if already_interested:
                interests = [x for x in interests if x not in interest_types]


class FormPage(Screen):
    pass