#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 21:41:04 2021

@author: martin
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def show(self):
        content = LoadDialog(load=self.load_file, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load a file", content=content,
                            size_hint=(1, 1))
        self._popup.open()

    def load_file(self, path, filepath):
        print(filepath[0])
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()
        
class exampleApp(App):
    def build(self):
        btn = Button(text="Press me")
        btn.bind(on_release=self.load_settings)
        return btn
    
    def load_settings(self, instance):
        loading = LoadDialog()
        loading.show()
        
if __name__ == "__main__":
    exampleApp().run()