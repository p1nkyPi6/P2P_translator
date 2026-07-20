from collections import deque

from Classes.Frame import Frame

class FrameQueue(deque):
    def append(self, item: Frame):
        super().append(item)

    def encoded_append(self, item: Frame):
        super().append(item.compres())

    def pop(self) -> Frame:
        return super().pop()

    def decoded_pop(self) -> Frame:
        return super().pop().decompress()
