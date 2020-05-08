from  kivy.app import App
from kivymd.theming import ThemeManager

class MainApp(MDApp):
    theme_cls = ThemeManager()
    

MainApp().run()