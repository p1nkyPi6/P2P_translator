import socket
import struct

import numpy as np

import mss
import cv2

HOST = "192.168.1.151"
PORT = 65432

def recv_img(client_sock, total_bytes):
    buffer = b""

    while(len(buffer) < total_bytes):

        remaining = total_bytes - len(buffer)
        chunk = client_sock.recv(min(remaining, 4096))

        if not chunk:
            print(f"Соединение разорвано до передачи полного изображения!")
            return 0

        buffer += chunk
    
    return buffer

def decode_from_jpg(encoded_img: bytes) -> np.ndarray:
    decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    if decoded_img is None:
        raise ValueError("JPEG decoded failed")
    
    return decoded_img

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(60.0)

    s.bind((HOST, PORT))
    s.listen()
    conn, addr  = s.accept()
    with conn:
        print(f"Connecting by {addr}")
        while True:
            # Read header 
            pack_header = conn.recv(4)
            if not pack_header:
                print("Ничего не пришло!!!")
                exit(1)

            # Метод всегда возвращает кортеж, но нам нужно только ОДНО значение
            unpack_header = struct.unpack('!i', pack_header)[0]
            print(unpack_header)

            lenght_of_encoded_img = unpack_header

            # Read encoded img
            encoded_img = recv_img(conn, lenght_of_encoded_img)
            if encoded_img == 0:
                pass

            print(f"{hash(encoded_img)}")
            print(f"{encoded_img[:10]}")

            decode_img = decode_from_jpg(np.frombuffer(encoded_img, np.uint8))

            with mss.MSS() as img_stream_output:
                cv2.imshow("OpenCV/Numpy normal", decode_img)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()