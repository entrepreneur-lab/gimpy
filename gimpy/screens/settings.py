import json
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from .dialogs.load import LoadDialog
from .dialogs.save import MySaveDialog
from .dialogs.image_dir import ImageDirDialog 

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(None, self)
        
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
        if text == 's':
            self.open_save_dialog(1)
        elif text == 'l':
            self.open_load_dialog(1)
        elif text == 'a':
            self.choose_image_dir(1)
    
    def on_pre_enter(self):
        """
        Generates the layout for the settings screen
        just before entering the screen

        Returns
        -------
        None.

        """
        
        # bind keys before entering
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        Window.size = (300, 400)
        
        # add box layout to avoid issue with
        # button spanning multiple columns
        overall = BoxLayout(orientation="vertical")
        layout = GridLayout(rows=9, cols=2)
        self.entries = []
        
        # loop to add all labels and buttons
        for i in range(1, 9):
           lbl = Label(text=f"Class {i}")
           entry = TextInput(multiline=False)
           layout.add_widget(lbl)
           layout.add_widget(entry)
           self.entries.append(entry)
           
        load_btn = Button(text="[u]l[/u]oad", markup=True)
        save_btn = Button(text="[u]s[/u]ave", markup=True)
        start_btn = Button(text="[u]a[/u]nnotate", markup=True,
                           size_hint=(1.0, 0.2))
        
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
        
    def on_leave(self):
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        
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
        print("Opening save dialog")
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
        d = dict((i, e.text) for i, e in enumerate(self.entries, 1))
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
        print("Opening load dialog")
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
        and pass class labels with respective key bindings
        to the app itself

        Parameters
        ----------
        instance : ImageDirDialog
            instance of the ImageDirDialog class

        Returns
        -------
        None.

        """
        self.label_dict = dict(
            (i, e.text) for i, e in enumerate(self.entries, 1)
            )
        
        choose = Factory.ImageDirDialog()
        choose.open()
