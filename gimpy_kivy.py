#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 22:47:47 2021

@author: martin
"""

import os
import json
# not sure how necessary this import will be
# from skimage.io import imread
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = GridLayout(rows=8, cols=2)
        for i in range(8):
           lbl = Label(text=f"Class {i}")
           entry = TextInput()
           layout.add_widget(lbl)
           layout.add_widget(entry)
        load_btn = Button(text="Load")
        save_btn = Button(text="Save")
        start_btn = Button(text="Annotate")
        layout.add_widget(load_btn)
        layout.add_widget(save_btn)
        layout.add_widget(start_btn)

class ViewerScreen(Screen):
    pass

class gimpyApp(App):
    
    def build(self):
        return

if __name__ == "__main__":
    gimpyApp().run()
    
