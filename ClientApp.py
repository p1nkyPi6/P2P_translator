import time
import sys

from Classes.ScreenCapturer import ScreenCapturer
from Classes.NetworkClient import NetWorkClient

def main():

    network_client = NetWorkClient()
    screen_capturer = ScreenCapturer("MSS")

    network_client.connect()

    while True:

        network_client.addPacket(screen_capturer.returnFrame())
        network_client.sendPacket()

        time.sleep(1 / 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Корректный перехват нажатия Ctrl+C в терминале
        print("The program was forcibly stopped by the user.")
        sys.exit(0)