import struct

from utils.decorators import validate_types

from Classes.Frame import Frame

class NetworkPacket:
        @validate_types(data=Frame)
        def __init__(self, data: Frame):
            data.compress()
            encoded_data = data.data

            self.__header = len(encoded_data)
            self.__body = encoded_data

        @property
        def bytes(self) -> bytes:
            '''Возвращает массив байт экземпляра класса'''
            return struct.pack('!i', self.__header) + self.__body.tobytes()