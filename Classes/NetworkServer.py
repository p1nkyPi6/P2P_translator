import socket
import struct

import numpy as np

from queue import Queue

#Пока зашью это строго в код, потом сделаю подгрузку из конфига
#HOST = "192.168.1.151"
HOST = "127.0.0.1"
PORT = 65432

SERVER_TIMEOUT = 200.0

class NetworkServer:

    def __init__(self):
        self.__network_bytes_from_packet_queue: Queue[np.array] = Queue()
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__closeNetworkServer = False

        self.__server_socket.settimeout(SERVER_TIMEOUT)

        self.__server_socket.bind((HOST, PORT))

    def __readBytesFromPacket(self, total_bytes) -> np.array:
        buffer = b""

        while(len(buffer) < total_bytes):

            remaining = total_bytes - len(buffer)
            chunk = self.__client_socket.recv(min(remaining, 4096))

            if not chunk:
                print(f"Соединение разорвано до передачи полного изображения!")
                return 0

            buffer += chunk
    
        return buffer
    
    def __sendAnswer(self):
        if self.__closeNetworkServer:
            self.__client_socket.sendall(b"Exit code")
            return

        self.__client_socket.sendall(b"Pass")
    
    def startService(self):
        self.__server_socket.listen()
        self.__client_socket, addr  = self.__server_socket.accept()

    def closeService(self):
        self.__closeNetworkServer = True

        self.__sendAnswer()
        
        self.__server_socket.close()
        self.__client_socket.close()

    def isClose(self) -> bool:
        return self.__closeNetworkServer

    def readPacket(self):
        pack_header = self.__readBytesFromPacket(4)

        if not pack_header:
            print("Соединение было закрыто")
            self.__closeNetworkServer = True
            return

        unpack_header = struct.unpack('!i', pack_header)[0]

        self.__network_bytes_from_packet_queue.put(
            self.__readBytesFromPacket(
                unpack_header
                )
            )
        
        self.__sendAnswer()

    def getPacket(self) -> np.array:
        return self.__network_bytes_from_packet_queue.get()