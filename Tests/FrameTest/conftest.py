import pytest
import numpy as np
import cv2

@pytest.fixture
def test_image_with_uint32():
    """Создаёт тестовое изображение 250x250."""

    data = np.zeros((250, 250, 4), dtype=np.uint32)
    
    data[:, :, 2] = 255  # R канал
    data[:, :, 3] = 255  # A канал
    
    return data

@pytest.fixture
def test_image_without_alpha():
    """Создаёт тестовое изображение 250x250."""

    data = np.zeros((250, 250, 3), dtype=np.uint8)
    
    data[:, :, 2] = 255  # R канал

    return data

@pytest.fixture
def test_image():
    """Создаёт тестовое изображение 250x250."""

    data = np.zeros((250, 250, 4), dtype=np.uint8)
    
    data[:, :, 2] = 255  # R канал
    data[:, :, 3] = 255  # A канал

    return data

@pytest.fixture
def test_compress_image():
    """Создаёт тестовое изображение 250x250 и сжимает"""

    data = np.zeros((250, 250, 4), dtype=np.uint8)
    
    data[:, :, 2] = 255  # R канал
    data[:, :, 3] = 255  # A канал

    compressed_data = cv2.imencode(
        ".jpg",
        cv2.cvtColor(
            data,
            cv2.COLOR_BGRA2BGR
            ),
        [int(cv2.IMWRITE_JPEG_QUALITY), 75]
    )

    return compressed_data[1]