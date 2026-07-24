import socket

from queue import Queue

from utils.decorators import validate_types
from utils.decorators import check_closed

from Classes.Frame import Frame
from Classes.NetworkPacket import NetworkPacket

#Пока зашью это строго в код, потом сделаю подгрузку из конфига
#HOST = "192.168.1.151"
HOST = "127.0.0.1"
PORT = 65432

class NetworkClient:

    def __init__(self):
        self.__network_packet_queue: Queue[NetworkPacket] = Queue()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__isClose = False

        try:
            self.__socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            raise ConnectionRefusedError("Error: The server rejected the connection (it might not be running).")
        except socket.timeout:
            raise TimeoutError("Error: The server response timed out.")
        except socket.error as e:
            raise OSError(f"System socket error: {e}")

    def __getResponse(self):
        response = self.__socket.recv(1024)

        if response == b"Exit code":
            print("Сервер закрыл соединение. Окончание сеанса")
            self.__isClose = True

        if response != b"Pass":
            print(f"Неверный ответ от сервера: {response}. Ожидалось b'Pass'.")
            self.__isClose = True

        if not response:
            print("Сервер закрыл соединение (получен пустой пакет).")
            self.__isClose = True
    
    def Close(self):
        self.__socket.close()

    @validate_types(data=Frame)
    def addPacket(self, data: Frame):
        new_packet = NetworkPacket(data)
        self.__network_packet_queue.put(new_packet)

    @check_closed('isClose')
    def sendPacket(self):
        if self.__network_packet_queue.empty():
            return

        self.__socket.sendall(self.__network_packet_queue.get().getBytes())

        self.__getResponse()

    @property
    def isClose(self) -> bool:
            return self.__isClose