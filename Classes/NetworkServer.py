import socket
import struct

import numpy as np

from queue import Queue

#Пока зашью это строго в код, потом сделаю подгрузку из конфига
#HOST = "192.168.1.151"
HOST = "127.0.0.1"
PORT = 65432

SERVER_TIMEOUT = 2.0

class NetworkServer:

    def __init__(self):
        self.__network_bytes_from_packet_queue: Queue[np.array] = Queue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.settimeout(SERVER_TIMEOUT)

        self.server_socket.bind((HOST, PORT))

    def __readBytesFromPacket(self, total_bytes) -> np.array:
        buffer = b""

        while(len(buffer) < total_bytes):

            remaining = total_bytes - len(buffer)
            chunk = self.client_socket.recv(min(remaining, 4096))

            if not chunk:
                print(f"Соединение разорвано до передачи полного изображения!")
                return 0

            buffer += chunk
    
        return buffer
    
    def startService(self):
        self.server_socket.listen()
        self.client_socket, addr  = self.server_socket.accept()

    def readPacket(self):
        pack_header = self.client_socket.recv(4)

        if not pack_header:
            print("Ничего не пришло!!!")
            exit(1)

        unpack_header = struct.unpack('!i', pack_header)[0]

        self.__network_bytes_from_packet_queue.put(
            self.__readBytesFromPacket(
                unpack_header
                )
            )

    def getPacket(self) -> np.array:
        return self.__network_bytes_from_packet_queue.get()