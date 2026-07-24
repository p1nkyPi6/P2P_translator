import pytest

from Classes.NetworkPacket import NetworkPacket

#pytest Tests/NetworkPacketTest/tests.py

# ===================================================
# ============ НЕГАТИВНЫЕ ТЕСТЫ (ОШИБКИ) ============
# ===================================================

#pytest Tests/NetworkPacketTest/tests.py::test__init_error_None -v
def test__init_error_None():
    with pytest.raises(TypeError) as error_message:
        frame = NetworkPacket(None)

    assert "data cannot be None" in str(error_message.value)

#pytest Tests/NetworkPacketTest/tests.py::test__init_error_type -v
def test__init_error_type(test_nparray):
    with pytest.raises(TypeError) as error_message:
        network_packet = NetworkPacket(test_nparray)

    assert "data' must be Frame" in str(error_message.value)

# ===================================================
# ================ ПОЗИТИВНЫЕ ТЕСТЫ =================
# ===================================================

#pytest Tests/NetworkPacketTest/tests.py::test__init_from_Frame -v
def test__init_from_Frame(test_frame):
    network_packet = NetworkPacket(test_frame)

    assert network_packet is not None

# ===================================================
# ================== ТЕСТЫ МЕТОДОВ ==================
# ===================================================

#pytest Tests/NetworkPacketTest/tests.py::test_bytes_property -v
def test_bytes_property(test_frame):
    network_packet = NetworkPacket(test_frame)
    
    assert isinstance(network_packet.bytes, bytes)