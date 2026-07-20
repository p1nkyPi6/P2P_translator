import sys

from Classes.FrameRenderer import FrameRenderer
from Classes.NetworkServer import NetworkServer

def main():
    network_server = NetworkServer()
    frame_renderer = FrameRenderer()

    network_server.startService()

    try:
        while not (frame_renderer.isClose() or network_server.isClose()):
            network_server.readPacket()
            if network_server.isClose():
                break

            frame_renderer.readFrame(network_server.getPacket())
            frame_renderer.paintFrame()
    finally:
        network_server.closeService() 

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Корректный перехват нажатия Ctrl+C в терминале
        print("The program was forcibly stopped by the user.")
        sys.exit(0)