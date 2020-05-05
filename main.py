import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown


kivy.require('1.11.1')

class TimeOptionButton(Button):
    pass

class LoginScreen(Widget):
    dropdown = ObjectProperty(None)
    
    def addTimeOptions(self, hours):
        if hours <= 12:
            button = TimeOptionButton(text=(hours + " hours"))
            self.dropdown.addwidget(button)
            hours += 1
            self.addTimeOptions(self, hours)
        else:
            pass

class TripRouletteApp(App):
    def build(self):
        loginscreen = LoginScreen()
        loginscreen.addTimeOptions(0)
        return loginscreen

if __name__ == "__main__":
    TripRouletteApp().run()