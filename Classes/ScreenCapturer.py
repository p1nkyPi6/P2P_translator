from queue import Queue

from utils.decorators import validate_types
from utils.decorators import check_closed

from Classes.Frame import Frame
from Classes.MSS.ScreenCapturerMSS import ScreenCapturerMSS

class ScreenCapturer():
    __strategies = {
        "MSS": ScreenCapturerMSS()
    }

    @validate_types(input_type=str)
    def __init__(self, input_type: str = "MSS"):
        strategy_class = self.__strategies.get(input_type)
        if not strategy_class:
            raise ValueError(f"This type of ScreenCapturer:({input_type}) is not supported.")

        self.__capture_engine = strategy_class
        self.__raw_frames_queue: Queue[Frame] = Queue()

        self.__isClosed = False

    def __readFrame(self):
        self.__raw_frames_queue.put(self.__capture_engine.returnFrame())

    @check_closed('isClose')
    def returnFrame(self) -> Frame:
        self.__readFrame()
        return self.__raw_frames_queue.get()

    def Close(self):
        self.__isClosed = True

    @property
    def isClose(self) -> bool:
        return self.__isClosed