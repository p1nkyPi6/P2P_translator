from enum import Enum
from queue import Queue

from Classes.Frame import Frame
from Classes.MSS._ScreenCapturerMSS import _ScreenCapturerMSS

class _InputType(Enum):
    MSS = "MSS"

class ScreenCapturer():
    __strategies = {
        "MSS": _ScreenCapturerMSS()
    }

    def __init__(self, input_type: _InputType = "MSS"):

        strategy_class = self.__strategies.get(input_type)
        if not strategy_class:
            raise ValueError(f"This type jf ScreenCapturer:({input_type}) is not supported.")

        self.__capture_engine = strategy_class
        self.__raw_frames_queue: Queue[Frame] = Queue()

    def __readFrame(self):
        self.__raw_frames_queue.put(self.__capture_engine.returnFrame())

    def returnFrame(self) -> Frame:
        self.__readFrame()
        return self.__raw_frames_queue.get()