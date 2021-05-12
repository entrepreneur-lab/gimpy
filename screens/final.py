from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

class FinalScreen(Screen):
    def on_pre_enter(self):
        Window.size = (300, 300)
