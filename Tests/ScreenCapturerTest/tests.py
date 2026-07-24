import pytest

from unittest.mock import patch

from Classes.Frame import Frame
from Classes.MSS.ScreenCapturerMSS import ScreenCapturerMSS
from Classes.ScreenCapturer import ScreenCapturer

#pytest Tests/ScreenCapturerTest/tests.py

# ===================================================
# ============ НЕГАТИВНЫЕ ТЕСТЫ (ОШИБКИ) ============
# ===================================================

#pytest Tests/ScreenCapturerTest/tests.py::test__init_None_error -v
def test__init_None_error():
    with pytest.raises(TypeError) as error_message:
        screen_capture = ScreenCapturer(None)
    
    assert "data cannot be None" in str(error_message.value)

#pytest Tests/ScreenCapturerTest/tests.py::test__init_type_error -v
def test__init_strategy_type_error():
    with pytest.raises(ValueError) as error_message:
        screen_capture = ScreenCapturer("UNSUPPORTED")
    
    assert "This type of ScreenCapturer" in str(error_message.value)

#pytest Tests/ScreenCapturerTest/tests.py::test_returnFrame_after_closed -v
def test_returnFrame_after_closed():
    screen_capture = ScreenCapturer("MSS")
    screen_capture.Close()

    with pytest.raises(RuntimeError) as error_message:
        screen_capture.returnFrame()
        
    assert "Attempt to use a closed" in str(error_message.value)

# ===================================================
# ================ ПОЗИТИВНЫЕ ТЕСТЫ =================
# ===================================================

#pytest Tests/ScreenCapturerTest/tests.py::test_init_with_default_strategy -v
def test_init_with_default_strategy():
    capturer = ScreenCapturer()
    
    assert capturer is not None
    assert hasattr(capturer, '_ScreenCapturer__capture_engine')
    assert hasattr(capturer, '_ScreenCapturer__raw_frames_queue')

#pytest Tests/ScreenCapturerTest/tests.py::test__init_correct_strategy -v
def test__init_correct_strategy():
    screen_capture = ScreenCapturer("MSS")

    assert screen_capture is not None
    assert isinstance(
        screen_capture._ScreenCapturer__capture_engine,
        ScreenCapturerMSS
    )

    assert not screen_capture.isClose

# ===================================================
# ================== ТЕСТЫ МЕТОДОВ ==================
# ===================================================

#pytest Tests/ScreenCapturerTest/tests.py::test_Close -v
def test_Close():
    screen_capture = ScreenCapturer("MSS")
    screen_capture.Close()

    assert screen_capture.isClose

#pytest Tests/ScreenCapturerTest/tests.py::test_returnFrame_correct_data -v
@patch('Classes.MSS.ScreenCapturerMSS.ScreenCapturerMSS.returnFrame')
def test_returnFrame_correct_data(mock_return, test_frame):
    mock_return.return_value = test_frame

    screen_capture = ScreenCapturer("MSS")
    frame = screen_capture.returnFrame()
    queue = screen_capture._ScreenCapturer__raw_frames_queue
    
    assert queue.empty()
    assert isinstance(frame, Frame)
    assert frame.data.all() == test_frame.data.all()

#pytest Tests/ScreenCapturerTest/tests.py::test_returnFrame_multiple_calls -v
@patch('Classes.MSS.ScreenCapturerMSS.ScreenCapturerMSS.returnFrame')
def test_returnFrame_multiple_calls(mock_return, test_frame, test_frame_2):
    mock_return.side_effect = [test_frame, test_frame_2]

    screen_capture = ScreenCapturer("MSS")
    frame_1 = screen_capture.returnFrame()
    frame_2 = screen_capture.returnFrame()

    assert frame_1.data.all() == test_frame.data.all()
    assert frame_2.data.all() == test_frame_2.data.all()
    assert not screen_capture.isClose