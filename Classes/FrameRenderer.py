import numpy as np
import cv2

from queue import Queue

class FrameRenderer:

    def __init__(self):
        self.__freme_render_queue: Queue[np.array] = Queue()

    def readFrame(self, data: np.array | bytes):
        self.__freme_render_queue.put(data)

    def paintFrame(self):
        cv2.imshow("OpenCV/Numpy normal", self.__freme_render_queue.get())

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
