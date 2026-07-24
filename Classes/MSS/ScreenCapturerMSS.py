import mss
import numpy as np

from Classes.Frame import Frame

from Classes.Interfaces.InputStrategy import InputStrategy

class ScreenCapturerMSS(InputStrategy):
    def __init__(self):
        self.input = mss.MSS()
        
        #Пока зашью это строго в код, потом сделаю подгрузку из конфига
        self.monitor = self.input.primary_monitor

    def returnFrame(self) -> Frame:
        return Frame(np.asarray(self.input.grab(self.monitor)))