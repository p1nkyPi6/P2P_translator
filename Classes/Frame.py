import cv2
import numpy as np

#Пока зашью это строго в код, потом сделаю подгрузку из конфига
JPG_QUALITY = 80

class Frame:

    def __init__(self, data: np.array | bytes, isCompresed = False):
        self.isCompresed = isCompresed
        self.data = data

        if data is bytes:
            self.isCompresed = True

    def __getData(self) -> np.array:
        return self.data
    
    def __compress(self):
        if self.isCompresed:
            return

        success, encoded_img = cv2.imencode(
            ".jpg",
            self.__getData(),
            [int(cv2.IMWRITE_JPEG_QUALITY), JPG_QUALITY],
        )

        if not success:
            raise ValueError("JPEG encoding failed")
    
        self.data = encoded_img
        self.isCompresed = True

    def __decompress(self):
        if not self.isCompresed:
            return

        decoded_img = cv2.imdecode(
            np.frombuffer(self.data, np.uint8),
            cv2.IMREAD_COLOR
        )

        if decoded_img is None:
            raise ValueError("Can't decompress image from _data")
        
        self.data = decoded_img

    def toByte(self) -> bytes:
        return self.data.tobytes()

    @staticmethod
    def CompressFrameToBytes(frame: Frame, jpg_quality = JPG_QUALITY) -> bytes:
        frame.__compress()
        return frame.__getData()
    
    @staticmethod
    def DecompressFrameFromBytes(data: bytes) -> Frame:
        frame = Frame(data, True)
        frame.__decompress()
        
        return frame