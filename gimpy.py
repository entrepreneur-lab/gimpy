#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 10:55:52 2021

@author: martin
"""

import os
import json
import numpy as np
import tkinter as TK
from PIL import Image
from tkinter import filedialog
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class app:
    def __init__(self, master):
        self.master = master
        self.settings_window()
        self.master.focus_set()
        
    def settings_window(self):
        """
        Create the settings window

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

        """
        settings = filedialog.askopenfilename(
            title="Open a json settings file")
        with open(settings, "r") as f:
            d = json.loads(f)
        for value, entry in zip(d, self.inputs):
            entry.insert(0, value)
    
    def _save_settings(self):
        """
        Save current settings to a json file

        """
        d = {}
        
        for i, ann in enumerate(self.inputs):
            d[i] = ann
        savename = filedialog.asksaveasfile(
            title="Save settings file", mode='w', defaultextension=".json"
            )
        if savename != None:
            with open(savename, "w") as f:
                json.dump(d, f)
    
    def map_inputs(self):
        """
        Bind button presses to the name to insert into the images
        found in the directory

        Returns
        -------
        None.

        """
        for i, entry in enumerate(self.inputs):
            self.master.bind(f"{i}", lambda event: self.rename_file(entry))
    
    def annotate(self):
        self.map_inputs()
        self.master.withdraw()
        
        # destroy widgets from settings window
        widgets = self.master.grid_slaves()
        for w in widgets:
            w.destroy()
                    
        self.dir = filedialog.askdirectory()
        self.master.deiconify()
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()
        os.chdir(self.dir)
        
        self.images = [i for i in os.listdir(os.getcwd()) if i.endswith('.tif')]
        self.x = 0
        
        self.label = TK.Label(self.master,
                              text=f"{self.x + 1} of {len(self.images)}")
        self.label.pack()
        # help_ = TK.Label(self.master, text='''Press number of nodules''')
        # help_.pack()
            
        fig = Figure(figsize=(5,5))
        ax = fig.add_subplot(111)
        ax.imshow(
            np.array(
                Image.open(self.images[self.x])
                ),
            cmap = 'viridis')
        self.canvas = FigureCanvasTkAgg(fig, master = self.master)
        self.canvas.get_tk_widget().pack()
    
    def next_image(self):
        self.x += 1
        if self.x != len(self.images):
            self.label.configure(text = f"{self.x + 1} of {len(self.images)}")
            self.canvas.get_tk_widget().pack_forget()
            fig = Figure(figsize = (5, 5))
            ax = fig.add_subplot(111)
            ax.imshow(np.array(Image.open(self.images[self.x])), cmap='viridis')
            self.canvas = FigureCanvasTkAgg(fig, master=self.master)
            self.canvas.get_tk_widget().pack()
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
            close = TK.Button(self.master, text='Close', command=self.end)
            close.pack()
            
    def change_settings(self):
        self.master.deiconify()
        widgets = self.master.pack_slaves()
        
        for w in widgets:
            w.destroy()
        
        self.settings_window()

    def rename_file(self, map_value):
        renamed = self.images[self.x].replace('.', f"{map_value}.")
        os.rename(self.images[self.x], renamed)
        self.next_image()
        
    def end(self):
        self.master.destroy()

if __name__ == "__main__":
    root = TK.Tk()
    app = app(root)
    root.mainloop()