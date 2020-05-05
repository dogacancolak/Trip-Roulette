import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.dropdown import DropDown
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle,Color

kivy.require('1.11.1')

class TimeOptionButton(Button):
    pass

class TimeDropDown(BoxLayout):
    pass

class LoginScreen(Widget):
    dropdown = ObjectProperty(DropDown)
    trip_duration = NumericProperty(0)

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.addTimeOptions()

    def addTimeOptions(self):
        for i in range(13):
            item = TimeOptionButton(text=(str(i) + " hours"))
            item.value = i
            self.dropdown.ids.dropdown.add_widget(item)

        for child in self.dropdown.children:
            print(child)
            for i in child.children:
                print(i)
            # child.canvas.add(Color(rgba=(1, 0, 0, 0.5)))
            # child.canvas.add(Rectangle(pos=self.pos, size=self.size))

class TripRouletteApp(App):
    def build(self):
        loginscreen = LoginScreen()
        return loginscreen

if __name__ == "__main__":
    TripRouletteApp().run()