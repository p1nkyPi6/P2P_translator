import socket
import struct

import numpy as np

from queue import Queue

#Пока зашью это строго в код, потом сделаю подгрузку из конфига
HOST = "127.0.0.1"
PORT = 65432

SERVER_TIMEOUT = 120.0

class NetworkServer:

    def __init__(self):
        self.__network_bytes_array_from_packet_queue: Queue[np.array] = Queue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.settimeout(SERVER_TIMEOUT)

        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()
        self.client_socket, addr  = self.server_socket.accept()

        print(f"Соединение установлено")

    def __readFrameFromPacket(self, total_bytes) -> np.array:
        buffer = b""

        while(len(buffer) < total_bytes):

            remaining = total_bytes - len(buffer)
            chunk = self.client_socket.recv(min(remaining, 4096))

            if not chunk:
                print(f"Соединение разорвано до передачи полного изображения!")
                return 0

            buffer += chunk
    
        return np.frombuffer(buffer, np.uint8)

    def readPacket(self):
        pack_header = self.client_socket.recv(4)

        if not pack_header:
            print("Ничего не пришло!!!")
            exit(1)

        # Метод всегда возвращает кортеж, но нам нужно только ОДНО значение
        unpack_header = struct.unpack('!i', pack_header)[0]

        self.__network_bytes_array_from_packet_queue.put(self.__readFrameFromPacket(unpack_header))

    def getPacket(self) -> np.array:
        return self.__network_bytes_array_from_packet_queue.get()