import json

from server import handle_client
from unittest.mock import patch, Mock


@patch("server.update_plot")
def test_handle_client_positive(mock_update_plot) -> None:
    mock_client_socket = Mock()

    # AAA - arrange, act, assert

    # arrange
    mock_client_socket.recv.side_effect = [b"+", b"+", b"+", b'{', b'"', b'x', b'"', b':', b' ', b'1',
                                           b',', b' ', b'"', b'y', b'"', b':', b' ', b'1', b'}', b"-", b"-",
                                           b"-", None]
    # act
    handle_client(mock_client_socket, "mock_addr")
    call = mock_client_socket.sendall.call_args
    args, *_ = call.args
    response_json_dict = json.loads(args)

    # assert
    assert b"status" in args
    assert "status" in response_json_dict
    assert response_json_dict.get("status") == "ERROR"  # how to test a positive response "OK"?
    assert "message" in response_json_dict
    mock_update_plot.assert_called_once_with(x=1, y=1)


@patch("server.find_pattern")
@patch("server.update_plot")
def test_handle_client_negative(mock_update_plot, mock_find_pattern) -> None:
    mock_client_socket = Mock()

    # AAA - arrange, act, assert

    # arrange
    mock_client_socket.recv.side_effect = [b"+", b"+", b"+", b'{', b'"', b'x', b'\'', b':', b' ', b'1',
                                           b',', b' ', b' ', b'y', b'"', b':', b' ', b'1', b'}', b"-", b"-",
                                           b"-", None]

    mock_find_pattern.return_value = (False, -1)

    # act
    handle_client(mock_client_socket, "mock_addr")
    # assert
    mock_find_pattern.assert_called()
    mock_update_plot.assert_not_called()
