import pytest
import socket

from unittest.mock import Mock, patch

from Classes.NetworkClient import NetworkClient

#pytest Tests/NetworkClientTest/tests.py

#pytest Tests/NetworkClientTest/tests.py::test__init_with_correct_conection -v
@patch.object(socket.socket, 'connect')
def test__init_with_correct_conection(mock_connect):
    mock_connect.return_value = None

    network_client = NetworkClient()

    assert network_client is not None
    assert not network_client.isClose

#pytest Tests/NetworkClientTest/tests.py::test__init_connect_errors -v
@patch('socket.socket')
def test__init_connect_errors(mock_connect, mock_server_socket_with_errors):
    mock_connect.return_value = mock_server_socket_with_errors

    with pytest.raises(ConnectionRefusedError) as error_message:
        network_client = NetworkClient()
            
    assert "Error: The server rejected the connection" in str(error_message.value)

    with pytest.raises(TimeoutError) as error_message:
        network_client = NetworkClient()
                
    assert "Error: The server response timed out" in str(error_message.value)

    with pytest.raises(OSError) as error_message:
        network_client = NetworkClient()
                
    assert "System socket error" in str(error_message.value)