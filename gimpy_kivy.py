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
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

class SaveDialog(Popup):

    def save_file(self, path):
        savepath = os.path.join(path, self.ids.dialog_savename.text)
        if not savepath.endswith('.json'):
            savepath += '.json'
        print(savepath)
        return savepath

class LoadDialog(Popup):

    def load_file(self, filepath):
        print(filepath[0])
        self.filepath = filepath[0]

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        # add box layout to avoid issue with
        # button spanning multiple columns
        overall = BoxLayout(orientation="vertical")
        layout = GridLayout(rows=9, cols=2)
        self.entries = []
        
        # loop to add all labels and buttons
        for i in range(8):
           lbl = Label(text=f"Class {i}")
           entry = TextInput(multiline=False)
           layout.add_widget(lbl)
           layout.add_widget(entry)
           self.entries.append(entry)
           
        load_btn = Button(text="Load")
        save_btn = Button(text="Save")
        start_btn = Button(text="Annotate", size_hint=(1.0, 0.2))
        
        # bind buttons to callbacks
        load_btn.bind(on_release=self.open_load_dialog)
        save_btn.bind(on_release=self.open_save_dialog)
        start_btn.bind(on_release=self.start_annotate)
        
        # add widgets to layouts
        layout.add_widget(load_btn)
        layout.add_widget(save_btn)
        overall.add_widget(layout)
        overall.add_widget(start_btn)
        self.add_widget(overall)
        
    def on_pre_enter(self):
        Window.size = (400, 500)
        
    def open_save_dialog(self, instance):
        # set up the saving file window
        saving = Factory.SaveDialog()
        saving.open()

    def save_settings(self):
        print('running save settings function')
        
        # save the data
        d = dict((i, e.text) for i, e in enumerate(self.entries))
        with open(self.savepath, "w") as f:
            json.dump(d, f)
    
    def open_load_dialog(self, instance):
        loading = Factory.LoadDialog()
        loading.open()
        
    def load_settings(self, fname):
        print("running load settings function")
        
        # load the data
        with open(fname, 'r') as f:
            data = json.load(f)
        for entry, val in zip(self.entries, data.values()):
            entry.text = val
    
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
    
    def rename_file(self):
        pass

if __name__ == "__main__":
    gimpyApp().run()
