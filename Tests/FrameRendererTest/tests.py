import pytest

from Classes.FrameRenderer import FrameRenderer

#pytest Tests/FrameRendererTest/tests.py

# ===================================================
# ============ НЕГАТИВНЫЕ ТЕСТЫ (ОШИБКИ) ============
# ===================================================

#pytest Tests/FrameRendererTest/tests.py::test__init_output_type_error -v
def test__init_output_type_error():
    with pytest.raises(ValueError) as error_message:
        frame_renderer = FrameRenderer("mss")

    assert "output strategies is not in strategies dict" in str(error_message.value)

#pytest Tests/FrameRendererTest/tests.py::test_readFrame_error_None -v
def test_readFrame_error_None():
    frame_renderer = FrameRenderer()

    with pytest.raises(TypeError) as error_message:
        frame_renderer.readFrame(None)

    assert "data cannot be None" in str(error_message.value)

#pytest Tests/FrameRendererTest/tests.py::test_readFrame_wrong_type -v
def test_readFrame_wrong_type(test_image):
    frame_renderer = FrameRenderer()

    with pytest.raises(TypeError) as error_message:
        frame_renderer.readFrame(test_image)

    assert "'data' must be Frame" in str(error_message.value)

#pytest Tests/FrameRendererTest/tests.py::test_printFrame_with_empty_queue -v
def test_printFrame_with_empty_queue():
    frame_renderer = FrameRenderer()

    with pytest.raises(ValueError) as error_message:
        frame_renderer.printFrame()

    assert "render queue is empty" in str(error_message.value)

# ===================================================
# ================== ТЕСТЫ МЕТОДОВ ==================
# ===================================================

#pytest Tests/FrameRendererTest/tests.py::test_readFrame -v
def test_readFrame(test_frame):
    frame_renderer = FrameRenderer()
    assert not frame_renderer.isClose

    frame_renderer.readFrame(test_frame)
    assert not frame_renderer.isClose

#pytest Tests/FrameRendererTest/tests.py::test_printFrame -v
def test_printFrame(test_frame):
    frame_renderer = FrameRenderer()
    frame_renderer.readFrame(test_frame)

    frame_renderer.printFrame()
    assert not frame_renderer.isClose