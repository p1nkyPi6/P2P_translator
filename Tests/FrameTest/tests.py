import pytest
import numpy as np

from Classes.Frame import Frame

#pytest Tests/FrameTest/tests.py

# ===================================================
# ============ НЕГАТИВНЫЕ ТЕСТЫ (ОШИБКИ) ============
# ===================================================

#pytest Tests/FrameTest/tests.py::test__init_type_error_None -v
def test__init_type_error_None():
    with pytest.raises(TypeError) as error_message:
        frame = Frame(None)

    assert "data cannot be None" in str(error_message.value)

#pytest Tests/FrameTest/tests.py::test__init_type_error_InvalidData -v
def test__init_type_error_InvalidData():
    with pytest.raises(TypeError) as error_message:
        frame = Frame("Invalid data")

    assert f"data must be ndarray, got {type("Invalid data").__name__}" in str(error_message.value)

#pytest Tests/FrameTest/tests.py::test__init_from_empty_array -v
def test__init_from_empty_array():
    with pytest.raises(ValueError) as error_message:
        frame = Frame(np.array([]))

    assert "data cannot be empty" in str(error_message.value)

#pytest Tests/FrameTest/tests.py::test__init_from_array_of_wrong_datatype -v
def test__init_from_array_of_wrong_datatype(test_image_with_uint32):
    with pytest.raises(TypeError) as error_message:
        frame = Frame(test_image_with_uint32)

    assert f"data dtype must be uint8" in str(error_message.value)
    
#
def test__init_from_array_of_data(test_image_without_alpha):
    with pytest.raises(ValueError) as error_message:
        frame = Frame(test_image_without_alpha)

    assert f"Unsupported shape" in str(error_message.value)

# ===================================================
# ================ ПОЗИТИВНЫЕ ТЕСТЫ =================
# ===================================================

#pytest Tests/FrameTest/tests.py::test__init_from_array -v
def test__init_from_img(test_image):
    frame = Frame(test_image)

    assert not frame.isCompressed

#pytest Tests/FrameTest/tests.py::test__init_from_compressed_img -v
def test__init_from_compressed_img(test_compress_image):
    compress_frame = Frame(test_compress_image)

    assert compress_frame.isCompressed

# ===================================================
# ================== ТЕСТЫ МЕТОДОВ ==================
# ===================================================

#Тест метода сжатия кадра
#pytest Tests/FrameTest/tests.py::test_compress -v
def test_compress(test_image):
    frame = Frame(test_image)
    frame.compress()

    assert frame.isCompressed

    frame.compress()
    assert frame.isCompressed

#Тест метода распаковки кадра
#pytest Tests/FrameTest/tests.py::test_decompress -v
def test_decompress(test_compress_image):
    compress_frame = Frame(test_compress_image)
    compress_frame.decompress()

    assert not compress_frame.isCompressed

    compress_frame.decompress()
    assert not compress_frame.isCompressed