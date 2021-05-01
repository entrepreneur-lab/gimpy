#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 22:47:47 2021

@author: martin
"""

import os
import json
from skimage.io import imread # not sure how necessary this import will be
from kixy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class SettingsScreen(Screen):
    pass

class ViewerScreen(Screen):
    pass

class gimpyApp(App):
    pass

if __name__ == "__main__":
    gimpyApp().run()
    