from queue import Queue
from enum import Enum

from utils.decorators import check_closed

from Classes.CV2.FrameRendererCV2 import FrameRendererCV2
from Classes.Frame import Frame

class FrameRenderer:
    class __InputType(Enum):
        MSS = "MSS"

    __strategies = {
        "cv2": FrameRendererCV2()
    }

    def __init__(self, output_strategies: __InputType = "cv2"):
        self.__render_engine = self.__strategies.get(output_strategies)
        if self.__render_engine is None:
            raise ValueError(f"output strategies is not in strategies dict or has type None")
        
        self.__freme_render_queue: Queue[Frame] = Queue()
        self.__closeRender = False

    def __validateRenderData(self, data) -> Frame:
        # 1. Проверка None
        if data is None:
            raise TypeError("data cannot be None")

        # 2. Проверка типа
        if not isinstance(data, Frame):
            raise TypeError(
                f"data must be Frame, got {type(data).__name__}"
            )
        
        return data
    
    @check_closed('isClose')
    def readFrame(self, data: Frame):
        frame = self.__validateRenderData(data)

        if frame.isCompressed:
            self.__freme_render_queue.put(
                frame.decompress()
            )
        else:
            self.__freme_render_queue.put(frame)

    @check_closed('isClose')
    def printFrame(self):
        if self.__freme_render_queue.empty():
            raise ValueError("render queue is empty")

        success = self.__render_engine.printFrame(
            self.__freme_render_queue.get()
        )

        if not success:
            self.__closeRender = True

    @property
    def isClose(self) -> bool:
        '''Возвращает True если рендер закрыт'''
        return self.__closeRender