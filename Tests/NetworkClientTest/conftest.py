import pytest

from unittest.mock import MagicMock

@pytest.fixture
def mock_server_socket_with_errors():
    fake_server_socket = MagicMock()

    fake_server_socket.connect.side_effect = [ConnectionRefusedError, TimeoutError, OSError]

    return fake_server_socket

@pytest.fixture
def mock_socket():
    fake_server_socket = MagicMock()

    fake_server_socket.connect.return_value = None
    