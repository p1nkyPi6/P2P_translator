import socket

from queue import Queue

from Classes.Frame import Frame
from Classes.NetworkPacket import NetworkPacket

#Пока зашью это строго в код, потом сделаю подгрузку из конфига
#HOST = "192.168.1.151"
HOST = "127.0.0.1"
PORT = 65432

class NetWorkClient:

    def __init__(self):
        self.__network_packet_queue: Queue[NetworkPacket] = Queue()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.__socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("Ошибка: Сервер отверг подключение (возможно, он не запущен).")
        except socket.timeout:
            print("Ошибка: Время ожидания ответа от сервера истекло.")
        except socket.error as e:
            print(f"Системная ошибка сокета: {e}")
            
    def close(self):
        self.__socket.close()

    def addPacket(self, data: bytes | Frame):
        new_packet = NetworkPacket(data)
        self.__network_packet_queue.put(new_packet)

    def sendPacket(self):
        if self.__network_packet_queue.empty():
            return

        self.__socket.sendall(self.__network_packet_queue.get().getBytes())