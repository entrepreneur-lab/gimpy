import os
from .basedialog import BaseDialog

class MySaveDialog(BaseDialog):
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
