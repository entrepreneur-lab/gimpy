#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 10:55:52 2021

@author: martin
"""

import os
import numpy as np
import tkinter as TK
from PIL import Image
from tkinter import filedialog
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class app:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        
        self.master.bind('0', lambda event: self.rename_file(0))
        self.master.bind('1', lambda event: self.rename_file(1))
        self.master.bind('2', lambda event: self.rename_file(2))
        self.master.bind('3', lambda event: self.rename_file(3))
        self.master.bind('4', lambda event: self.rename_file(4))
        self.master.bind('5', lambda event: self.rename_file(5))
        self.master.bind('6', lambda event: self.rename_file(6))
        self.master.focus_set()
    
    def setup_window(self):
        self.master.withdraw()
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
        help_ = TK.Label(self.master, text='''Press number of nodules''')
        help_.pack()
            
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
                              command=self.setup_window)
            again.pack()
            close = TK.Button(self.master, text='Close', command=self.end)
            close.pack()

    def rename_file(self, event):
        replace_name = f'_nodules{event}_Actin.tif'
        os.rename(self.images[self.x],
                  self.images[self.x].replace('_Actin.tif',
                                              replace_name))
        self.next_image()
        
    def end(self):
        self.master.destroy()

if __name__ == "__main__":
    root = TK.Tk()
    app = app(root)
    root.mainloop()