import sys

from Classes.FrameRenderer import FrameRenderer
from Classes.NetworkServer import NetworkServer

def main():
    network_server = NetworkServer()
    frame_renderer = FrameRenderer()

    while True:
        network_server.readPacket()
        frame_renderer.readFrame(network_server.getPacket())
        frame_renderer.paintFrame()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Корректный перехват нажатия Ctrl+C в терминале
        print("The program was forcibly stopped by the user.")
        sys.exit(0)