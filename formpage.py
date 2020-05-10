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
    pass

class FormPage(Screen):
    pass