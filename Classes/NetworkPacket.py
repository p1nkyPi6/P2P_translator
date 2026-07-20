import struct

from Classes.Frame import Frame

class NetworkPacket:
        '''
        def __init__(self):
            self.__header = b''
            self.__body =b''

        def __init__(self, data: bytes):
            self.__header = len(data)
            self.__body = data
        '''

        def __init__(self, data: Frame):
            encoded_data = Frame.CompressFrameToBytes(data)

            self.__header = len(encoded_data)
            self.__body = encoded_data

        def getBytes(self) -> bytes:
            return struct.pack('!i', self.__header) + self.__body.tobytes()