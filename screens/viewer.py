import os
import matplotlib.pyplot as plt
from skimage.io import imread
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from .utils.data import ImageNames

class ViewerScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewerScreen, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.mapping = {
            'left' : self.nav_left,
            'right' : self.nav_right,
            'up' : self.nav_up,
            'down' : self.nav_down
            }
    
    def on_pre_enter(self):
        """
        Generate the layout just before entering the screen

        Returns
        -------
        None.

        """
        Window.size = (700, 700)
        
        # get image filenames and info
        os.chdir(self.imgdir)
        self.imglist = sorted([i for i in os.listdir() if i.endswith('.tif')])
        self.imglist = [ImageNames(i, "") for i in self.imglist]
        self.newnames = []
        self.img_idx = 0
        self.num_images = len(self.imglist)
        
        # layout the screen
        self.layout = BoxLayout(orientation="vertical")
        self.layout_screen()
        self.add_widget(self.layout)
        
    def layout_screen(self):
        """
        Layout the viewer with the filename
        and an image of said file

        Returns
        -------
        None.

        """
        
        # prepare widgets
        self.layout.clear_widgets()
        self.current = self.imglist[self.img_idx]
        self.image = imread(self.current.oldname)
        
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
        
        self.oldlbl = Label(text=f"{self.current.oldname}",
                            size_hint_y=0.05)
        self.newlbl = Label(text=f"{self.current.newname}",
                            size_hint_y=0.05)
        canvas = FigureCanvasKivyAgg(plt.gcf(), size_hint_y=0.9)
        self.layout.add_widget(self.oldlbl)
        self.layout.add_widget(self.newlbl)
        self.layout.add_widget(canvas)
        
    def change_filename(self, num):
        """
        Add the class label into the filename,
        rename the file, and move to next image.

        Parameters
        ----------
        num : integer
            the integer key pressed on the keyboard, which indicates
            the class label that should be inserted into the
            filename

        Returns
        -------
        None.

        """
        print(f"{num} key pressed!")
        
    
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
        elif int(text) in range(8):
            self.change_filename(int(text))
        
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
