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

kivy.require('1.11.1')

class LoginScreen(Widget):
    pass



class TripRouletteApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    TripRouletteApp().run()