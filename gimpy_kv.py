#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 22:47:47 2021

@author: martin
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# import custom screens
from screens.final import FinalScreen
from screens.viewer import ViewerScreen
from screens.settings import SettingsScreen      

class GimpyApp(App):
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
        self.sm.add_widget(FinalScreen(name="final"))
        self.sm.current = "settings"
        return self.sm

def main():
    GimpyApp().run()

if __name__ == "__main__":
    main()
