import cv2

from Classes.Frame import Frame
from Classes.Interfaces.OutputStrategy import OutputStrategy

class FrameRendererCV2(OutputStrategy):

    #Пока зашью это строго в код, потом сделаю подгрузку из конфига
    DEFAULT_WAIT_TIME = 5

    def __waitKey(self, waiting_time: int, exit_key_code: int = ord('q')) -> bool:

        if cv2.waitKey(waiting_time) & 0xFF == exit_key_code:
            cv2.destroyAllWindows()
            return True
        
        return False
    
    def printFrame(self, frame: Frame):
        if frame.isCompressed:
            frame.decompress()

        cv2.imshow("OpenCV/Numpy normal", frame.data)

        if self.__waitKey(self.DEFAULT_WAIT_TIME):
            return False
        
        return True