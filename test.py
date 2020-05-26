from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.image import Image

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
from kivymd.uix.spinner import MDSpinner

import io
import zipfile
from itertools import cycle

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from routepage import RoutePage

class RoutePageApp(MDApp): 

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"


TripRouletteApp().run()