from kivy.app import App
from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd import images_path
from kivymd.toast import toast

class FoodOption(BoxLayout):
    def on_switch_active(self, switch, value):
        if value:
            App.get_running_app().food = True
        else:
            App.get_running_app().food = False

class DialogContent(BoxLayout):
    pass

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