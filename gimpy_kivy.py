#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 22:47:47 2021

@author: martin
"""

import os
import json
# not sure if skimage import is necessary
# from skimage.io import imread
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        # add box layout to avoid issue with
        # button spanning multiple columns
        overall = BoxLayout(orientation="vertical")
        layout = GridLayout(rows=9, cols=2)
        
        # loop to add all labels and buttons
        for i in range(8):
           lbl = Label(text=f"Class {i}")
           entry = TextInput(multiline=False)
           layout.add_widget(lbl)
           layout.add_widget(entry)
           
        load_btn = Button(text="Load")
        save_btn = Button(text="Save")
        start_btn = Button(text="Annotate", size_hint=(1.0, 0.2))
        
        # bind buttons to callbacks
        load_btn.bind(on_release=self.load_settings)
        save_btn.bind(on_release=self.save_settings)
        start_btn.bind(on_release=self.start_annotate)
        
        # add widgets to layouts
        layout.add_widget(load_btn)
        layout.add_widget(save_btn)
        overall.add_widget(layout)
        overall.add_widget(start_btn)
        self.add_widget(overall)
        
    def on_pre_enter(self):
        Window.size = (400, 500)
        
    def save_settings(self, instance):
        box = list(self.children)[0]
        grid = list(box.children)[1]
        for entry in list(grid.children):
            if isinstance(entry, TextInput):
                print(entry.text)
    
    def load_settings(self, instance):
        pass
    
    def start_annotate(self, instance):
        pass

class ViewerScreen(Screen):
    def on_pre_enter(self):
        Window.size = (600, 600)

class gimpyApp(App):
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(ViewerScreen(name="viewer"))
        sm.current = "settings"
        return sm

if __name__ == "__main__":
    gimpyApp().run()
