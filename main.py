import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

kivy.require('1.11.1')

class LoginScreen(Widget):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    email = ObjectProperty(None)


    def pressed(self):
        print(self.username.text, self.password.text, self.email.text)

        self.username.text = ""
        self.password.text = ""
        self.email.text    = ""

    # def __init__(self, **kwargs):
    #     super(LoginScreen, self).__init__(**kwargs)
    #     self.cols = 1

    #     self.topgrid = GridLayout()
    #     self.topgrid.cols = 2 

    #     self.topgrid.add_widget(Label(text='User Name:'))
    #     self.username = TextInput(multiline=False)
    #     self.topgrid.add_widget(self.username)

    #     self.topgrid.add_widget(Label(text='Password:'))
    #     self.password = TextInput(password=True, multiline=False)
    #     self.topgrid.add_widget(self.password)

    #     self.topgrid.add_widget(Label(text='Email:'))
    #     self.email = TextInput(multiline=False)
    #     self.topgrid.add_widget(self.username)

    #     self.add_widget(self.topgrid)
    #     self.submit = Button(text = 'Submit', font_size = 40)
    #     self.submit.bind(on_press = self.pressed)
    #     self.add_widget(self.submit)



class TripRouletteApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    TripRouletteApp().run()