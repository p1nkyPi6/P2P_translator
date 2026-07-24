import pytest
import numpy as np

from Classes.Frame import Frame

@pytest.fixture
def test_nparray():
    data = np.zeros((250, 250, 4), dtype = np.uint8)

    data[:, :, 2] = 255  # R канал
    data[:, :, 3] = 255  # A канал
    
    return data

@pytest.fixture
def test_frame():
    data = np.zeros((250, 250, 4), dtype = np.uint8)

    data[:, :, 2] = 255  # R канал
    data[:, :, 3] = 255  # A канал
    
    return Frame(data)