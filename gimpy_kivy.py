#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 22:47:47 2021

@author: martin
"""

import os
import json
import matplotlib.pyplot as plt
from skimage.io import imread
from kivy.app import App
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


class MySaveDialog(Popup):
    def save_file(self, path):
        """
        Gets a file savename from the user

        Parameters
        ----------
        path : string
            directory to save the settings file

        Returns
        -------
        savepath : string
            full path for saving the setttings file as json

        """
        savepath = os.path.join(path, self.ids.dialog_savename.text)
        if not savepath.endswith('.json'):
            savepath += '.json'
        return savepath

class LoadDialog(Popup):
    pass
        
class ImageDirDialog(Popup):
    pass

class SettingsScreen(Screen):
    def on_pre_enter(self):
        """
        Generates the layout for the settings screen
        just before entering the screen

        Returns
        -------
        None.

        """
        Window.size = (400, 500)
        
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
        start_btn.bind(on_release=self.choose_image_dir)
        
        # add widgets to layouts
        layout.add_widget(load_btn)
        layout.add_widget(save_btn)
        overall.add_widget(layout)
        overall.add_widget(start_btn)
        self.add_widget(overall)
        
    def open_save_dialog(self, instance):
        """
        Opens a popup to allow user to choose a save directory

        Parameters
        ----------
        instance : MySaveDialog
            instance of the MySaveDialog class

        Returns
        -------
        None.

        """
        saving = Factory.MySaveDialog()
        saving.open()

    def save_settings(self):
        """
        Save a dictionary of key-value pairs of numbers
        and class labels to a json file

        Returns
        -------
        None.

        """
        d = dict((i, e.text) for i, e in enumerate(self.entries))
        with open(self.savepath, "w") as f:
            json.dump(d, f)
    
    def open_load_dialog(self, instance):
        """
        Opens a popup to allow user to choose a settings file
        
        Parameters
        ----------
        instance : LoadDialog
            instance of the LoadDialog class

        Returns
        -------
        None.

        """
        loading = Factory.LoadDialog()
        loading.open()
        
    def load_settings(self, fname):
        """
        Load settings from a user-selected json file

        Parameters
        ----------
        fname : string
            full path to the settings file

        Returns
        -------
        None.

        """
        with open(fname, 'r') as f:
            data = json.load(f)
        for entry, val in zip(self.entries, data.values()):
            entry.text = val
            
    def choose_image_dir(self, instance):
        """
        Opens a popup to allow user to choose a directory of images

        Parameters
        ----------
        instance : ImageDirDialog
            instance of the ImageDirDialog class

        Returns
        -------
        None.

        """
        choose = Factory.ImageDirDialog()
        choose.open()
    
class ViewerScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewerScreen, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.mapping = {'left' : self.nav_left, 'right' : self.nav_right,
                       'up' : self.nav_up, 'down' : self.nav_down}
    
    def on_pre_enter(self):
        """
        Create the layout just before entering the screen

        Returns
        -------
        None.

        """
        Window.size = (700, 700)
        
        # get image filenames and info
        os.chdir(self.imgdir)
        self.imglist = sorted([i for i in os.listdir() if i.endswith('.tif')])
        self.img_idx = 0
        self.num_images = len(self.imglist)
        
        # layout the screen
        self.layout = BoxLayout(orientation="vertical")
        self.layout_screen()
        self.add_widget(self.layout)
        
    def layout_screen(self):
        """
        Layout the viewer with the filename and
        an image of said file

        Returns
        -------
        None.

        """
        
        # prepare widgets
        self.layout.clear_widgets()
        self.current = self.imglist[self.img_idx]
        self.image = imread(self.current)
        
        # remove current_slice attribute if dealing with mix
        # of multislice and single slice images
        if hasattr(self, "current_slice"):
            delattr(self, "current_slice")
        
        # plot the image with matplotlib
        try:
            plt.imshow(self.image, cmap="viridis")
        except TypeError:
            self.current_slice = 0
            self.max_slice = self.image.shape[0] - 1
            plt.imshow(self.image[self.current_slice], cmap='viridis')
        plt.axis("off")
        plt.tight_layout()
        
        self.imglbl = Label(text=f"{self.current}", size_hint_y=None,
                            height=60)
        canvas = FigureCanvasKivyAgg(plt.gcf())
        self.layout.add_widget(self.imglbl)
        self.layout.add_widget(canvas)
        
    
    def _on_keyboard_up(self, keyboard, keycode):
        """
        When keyboard button is released, map the button to a method

        Parameters
        ----------
        keyboard : kivy.core.window.Keyboard
            kivy class to access keyboard key presses
        keycode : tuple
            numeric code for the key and the text of said key

        Returns
        -------
        None.

        """
        text = keycode[1]
        # ensure key is accounted for in mapping dictionary
        if text in self.mapping.keys(): 
            func = self.mapping[text]
            func()
        
    def nav_left(self):
        """
        Move left in the list of images (towards index 0)

        Returns
        -------
        None.

        """
        if self.img_idx > 0:
            self.img_idx -= 1
            self.layout_screen()
    
    def nav_right(self):
        """
        Move right in the list of images (towards last index)

        Returns
        -------
        None.

        """
        if self.img_idx + 1 < self.num_images:
            self.img_idx += 1
            self.layout_screen()
    
    def nav_up(self):
        """
        Navigate up a slice

        Returns
        -------
        None.

        """
        self.update_slice(1)
    
    def nav_down(self):
        """
        Navigate down a slice

        Returns
        -------
        None.

        """
        self.update_slice(-1)
        
    def update_slice(self, num):
        """
        Navigate between slices in a multislice images
        and update the canvas

        Parameters
        ----------
        num : integer
            -1 or 1, informs whether to go up or down a slice

        Returns
        -------
        None.

        """
        
        # check if multisclice tiff
        if hasattr(self, "current_slice"):
            self.layout.remove_widget(self.layout.children[0])
            plt.cla()
            
            # nav down
            if num == -1 and self.current_slice > 0:
                self.current_slice -= 1
            elif num == 1 and self.current_slice + 1 < self.max_slice:
                self.current_slice += 1
            plt.imshow(self.image[self.current_slice], cmap='viridis')
            plt.axis("off")
            plt.tight_layout()
            canvas = FigureCanvasKivyAgg(plt.gcf())
            self.layout.add_widget(canvas)
    

class gimpyApp(App):
    def build(self):
        """
        Build method to create the app

        Returns
        -------
        self.sm : screen manager instance
            the screen manager

        """
        self.sm = ScreenManager()
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(ViewerScreen(name="viewer"))
        self.sm.current = "settings"
        return self.sm
    
    def rename_file(self):
        pass

if __name__ == "__main__":
    gimpyApp().run()
