import cv2
import numpy as np

from utils.decorators import validate_types

#Пока зашью это строго в код, потом сделаю подгрузку из конфига
JPG_QUALITY = 80

class Frame:

    @validate_types(data=np.ndarray)
    def __init__(self, data: np.ndarray):
        self.__data, self.__isCompressed = self.__validateData(data)

    def __validateData(self, data: np.ndarray) -> tuple[np.ndarray, bool]:
        # 1. Проверка размера
        if data.size == 0:
            raise ValueError("data cannot be empty")
    
        # 2. Проверка dtype
        if data.dtype != np.uint8:
            raise TypeError(
                f"data dtype must be uint8, got {data.dtype}"
            )
    
        # 5. Определение типа по форме
        if len(data.shape) == 1:
            return data, True
        elif len(data.shape) == 3 and data.shape[2] == 4:
            return data, False
        else:
            raise ValueError(
                f"Unsupported shape. Expected (H, W, 4) or (N), got {data.shape}"
            )

    def compress(self):
        """Сжимает кадр в JPEG."""
        if self.__isCompressed:
            return

        success, encoded_img = cv2.imencode(
            ".jpg",
            cv2.cvtColor(
                self.__data,
                cv2.COLOR_BGRA2BGR
            ),
            [int(cv2.IMWRITE_JPEG_QUALITY), JPG_QUALITY]
        )

        if not success:
            raise ValueError("JPEG encoding failed")
    
        self.__data = encoded_img
        self.__isCompressed = True

    def decompress(self):
        """Распаковывает кадр из JPEG."""
        if not self.__isCompressed:
            return

        decoded_img = cv2.imdecode(
            np.frombuffer(self.__data, np.uint8),
            cv2.IMREAD_COLOR
        )

        if decoded_img is None:
            raise ValueError("Can't decompress image from _data")
        
        self.__data = decoded_img
        self.__isCompressed = False

    @property
    def data(self) -> np.ndarray:
        """Возвращает данные кадра."""
        return self.__data

    @property
    def isCompressed(self) -> bool:
        """Возвращает True если кадр сжат."""
        return self.__isCompressed
