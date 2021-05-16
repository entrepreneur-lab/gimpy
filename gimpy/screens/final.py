from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

class FinalScreen(Screen):
    def __init__(self, **kwargs):
        super(FinalScreen, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(None, self)
        
    def on_pre_enter(self):
        Window.size = (300, 300)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        
    def on_leave(self):
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        
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
        if text == 'r':
            self.ids["again"].trigger_action(0.2)
