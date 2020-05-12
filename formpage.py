from kivy.app import App

from kivy.uix.screenmanager import Screen

from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd import images_path

from kivymd.uix.list import IRightBodyTouch
from kivymd.uix import MDAdaptiveWidget
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.selectioncontrol import MDCheckbox

class PageToolbar(MDToolbar):
    pass

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    def update_interests(self, switch, value):
        interests = App.get_running_app().user_info.interests

        # Convert switch.title in the UI to index strings in our program
        # e.g. 'Restaurants' to 'restaurant'
        interest_type = switch.title
        
        if value:
            if interest_type not in interests:
                interests.append(interest_type)
        else:
            if interest_type in interests:
                interests.remove(interest_type)


class FormPage(Screen):
    pass