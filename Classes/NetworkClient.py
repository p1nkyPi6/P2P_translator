import socket
import struct

from queue import Queue

from Classes.Frame import Frame

class NetWorkClient:

    class __NetworkPacket:
        def __init__(self):
            self.__header = b''
            self.__body =b''

        def __init__(self, data: bytes):
            self.__header = len(data)
            self.__body = data

        def __init__(self, data: Frame):
            encoded_data = Frame.CompressFrameToBytes(data)

            self.__header = len(encoded_data)
            self.__body = encoded_data

        def getBytes(self) -> bytes:
            return struct.pack('!i', self.__header) + self.__body.tobytes()

    def __init__(self):
        self.__network_packet_queue: Queue[NetWorkClient.__NetworkPacket] = Queue()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Пока зашью это строго в код, потом сделаю подгрузку из конфига
        self.__host = "192.168.1.151"
        self.__port = 65432

    def connect(self):
        try:
            self.__socket.connect((self.__host, self.__port))
        except ConnectionRefusedError:
            print("Ошибка: Сервер отверг подключение (возможно, он не запущен).")
        except socket.timeout:
            print("Ошибка: Время ожидания ответа от сервера истекло.")
        except socket.error as e:
            print(f"Системная ошибка сокета: {e}")
            
    def close(self):
        self.__socket.close()

    def addPacket(self, data: bytes | Frame):
        new_packet = NetWorkClient.__NetworkPacket(data)
        self.__network_packet_queue.put(new_packet)

    def sendPacket(self):
        if self.__network_packet_queue.empty():
            return

        self.__socket.sendall(self.__network_packet_queue.get().getBytes())