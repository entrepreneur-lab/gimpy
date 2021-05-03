#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 10:55:52 2021

@author: martin
"""

import os
import json
import tkinter as TK
from skimage.io import imread
from tkinter import filedialog
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GimpyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("gimpy")
        self.settings_window()
        self.master.focus_set()
        
        # correct for error when choosing another directory
        self.inputs_mapped = False
        
        # bind arrow keys to change slice
        self.min_slice = 0
        self.max_slice = 1
        self.master.bind("<Up>", self.up_slice)
        self.master.bind("<Down>", self.down_slice)
        self.master.bind("<Left>", self.navigate_left)
        self.master.bind("<Right>", self.navigate_right)
        
    def up_slice(self, event):
        """
        Move up a slice in the stack

        Parameters
        ----------
        event : event
            The event triggered by the <Up> key press

        Returns
        -------
        None.

        """ 
        if self.current_slice < self.max_slice:
            self.current_slice += 1
            self.ax.clear()
            self.ax.imshow(self.image[self.current_slice])
            self.ax.axis("off")
            self.canvas.draw()
    
    def down_slice(self, event):
        """
        Move down a slice in the stack

        Parameters
        ----------
        event : event
            The event triggered by the <Down> key press

        Returns
        -------
        None.

        """        
        
        if self.current_slice > 0:
            self.current_slice -= 1
            self.ax.clear()
            self.ax.imshow(self.image[self.current_slice])
            self.ax.axis("off")
            self.canvas.draw()
            
    def navigate_left(self, event):
        """
        Press left arrow and move left in the list of images
        
        Returns
        -------
        None.

        """
        if hasattr(self, "img_idx"):
            if self.img_idx > 0:
                self.img_idx -= 1
                self.change_image()
    
    def navigate_right(self, event):
        """
        Press right arrow and move right in the list of images
        
        Returns
        -------
        None.

        """
        if hasattr(self, "img_idx"):
            if self.img_idx < self.num_images - 1:
                self.img_idx += 1
                self.change_image()
        
    def settings_window(self):
        """
        Create the settings window

        Returns
        -------
        None.

        """

        self.lbls = []
        self.inputs = []
        for i in range(8):
            label = TK.Label(self.master, text=f"Class {i}")
            input_ = TK.Entry(self.master)
            label.grid(row=i, column=0)
            input_.grid(row=i, column=1)
            self.lbls.append(label)
            self.inputs.append(input_)
        load = TK.Button(self.master, text="Load settings",
                         command=self._load_settings)
        load.grid(row=8, column=0)
        save = TK.Button(self.master, text="Save settings",
                         command=self._save_settings)
        save.grid(row=8, column=1)
        annotate_images = TK.Button(self.master, text="Start annotating",
                                    command=self.annotate)
        annotate_images.grid(row=9, columnspan=2)
            
        
    def _load_settings(self):
        """
        Load settings from JSON file

        Returns
        -------
        None.

        """
        settings = filedialog.askopenfilename(
            title="Open a json settings file")
        with open(settings, "r") as f:
            d = json.load(f)
        for value, entry in zip(d.values(), self.inputs):
            entry.insert(0, value)
    
    def _save_settings(self):
        """
        Save current settings to a json file

        Returns
        -------
        None.

        """
        d = dict((i, ann.get()) for i, ann in enumerate(self.inputs))
        savename = filedialog.asksaveasfile(
            title="Save settings file", mode='w', defaultextension=".json"
            )
        savename = savename.name.split(os.sep)[-1]
        # print(savename)
        if savename == None:
            savename = "settings.json"
        with open(savename, "w") as f:
            json.dump(d, f)
    
    def map_inputs(self):
        """
        Bind key presses to the name to insert into the images
        found in the directory

        Returns
        -------
        None.

        """
        if not self.inputs_mapped:
            for i, entry in enumerate(self.inputs):
                self.master.bind(f"{i}",
                                 lambda event, entry=entry.get():
                                     self.rename_file(entry)
                                     )
        self.inputs_mapped = True
    
    def annotate(self):
        """
        Set up the annotation window for renaming files

        Returns
        -------
        None.

        """
        self.map_inputs()
        self.master.withdraw()
        
        # destroy widgets from settings window
        widgets = self.master.grid_slaves()
        for w in widgets:
            w.destroy()
        
        # destroys widgets added for annotating
        widgets = self.master.pack_slaves()
        for w in widgets:
            w.destroy()
                    
        self.dir = filedialog.askdirectory()
        self.master.deiconify()
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()
        os.chdir(self.dir)
        
        files = os.listdir(os.getcwd())
        self.images = sorted([i for i in files if i.endswith('.tif')])
        self.num_images = len(self.images)
        self.img_idx = 0
        self.imname = self.images[self.img_idx]
        
        text = f"{self.img_idx+1} of {self.num_images}\n{self.imname}"
        self.label = TK.Label(self.master, text=text)
        self.label.pack()
        self.update_image()
        
    def update_image(self):
        """
        Update the canvas with the next image in the sequence        

        Returns
        -------
        None.

        """            
        fig = Figure(figsize=(5,5))
        self.ax = fig.add_subplot(111)
        self.imname = self.images[self.img_idx]
        self.image = imread(self.imname)
        try:
            self.ax.imshow(self.image, cmap = 'viridis')
        except TypeError:
            self.current_slice = 0
            self.max_slice = self.image.shape[0] - 1
            self.ax.imshow(self.image[self.current_slice], cmap='viridis')
        self.ax.axis("off")
        self.canvas = FigureCanvasTkAgg(fig, master = self.master)
        self.canvas.get_tk_widget().pack()
    
    def change_image(self):
        """
        Opens the next image in the list of image files

        Returns
        -------
        None.

        """

        if self.img_idx != len(self.images):
            self.canvas.get_tk_widget().pack_forget()
            self.update_image()
            text = f"{self.img_idx+1} of {self.num_images}\n{self.imname}"
            self.label.configure(text=text)
        else:
            self.canvas.get_tk_widget().pack_forget()
            done = TK.Label(self.master, text='Finished!')
            done.pack()
            again = TK.Button(self.master, text='Choose another directory',
                              command=self.annotate)
            again.pack()
            change = TK.Button(self.master, text="Change settings",
                               command=self.change_settings)
            change.pack()
            close = TK.Button(self.master, text='Close',
                              command=self.close_app)
            close.pack()
            self.img_idx = 0
            
    def change_settings(self):
        """
        Clear widgets and go back to the settings window
        
        Returns
        -------
        None.

        """
        self.master.deiconify()
        widgets = self.master.pack_slaves()
        
        for w in widgets:
            w.destroy()
        
        self.settings_window()

    def rename_file(self, map_value):
        """
        Rename the file by adding the `map_value` just before the
        file extension

        Parameters
        ----------
        map_value : string
            class identifier for the image

        Returns
        -------
        None.

        """
        renamed = self.images[self.img_idx].replace('.', f"{map_value}.")
        os.rename(self.images[self.img_idx], renamed)
        files = os.listdir(os.getcwd())
        self.images = sorted([i for i in files if i.endswith('.tif')])
        self.img_idx += 1
        self.change_image()
        
    def close_app(self):
        """
        Close the app

        Returns
        -------
        None.

        """        
        self.master.destroy()
        
def main():
    root = TK.Tk()
    app = GimpyApp(root)
    root.mainloop()
    