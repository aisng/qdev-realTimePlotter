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
    assert response_json_dict.get("status") == "ERROR"
    assert "message" in response_json_dict
    mock_update_plot.assert_called_once_with(x=1, y=1)


@patch("server.update_plot")
def test_handle_client_data_not_json(mock_update_plot) -> None:
    mock_client_socket = Mock()

    mock_client_socket.recv.side_effect = [b"+", b"+", b"+", b'{', b'"', b'x', b'\'', b':', b' ', b'1',
                                           b',', b' ', b' ', b'y', b'z', b':', b' ', b'1', b'}', b"-", b"-",
                                           b"-", None]

    handle_client(mock_client_socket, "mock_addr")
    call = mock_client_socket.sendall.call_args_list
    first_call = call[0]

    args, *_ = first_call.args
    response_json_dict = json.loads(args)

    assert "JSONDecodeError" in response_json_dict["message"]
    mock_update_plot.assert_not_called()


@patch("server.update_plot")
def test_handle_client_json_data_missing_coordinate_values(mock_update_plot) -> None:
    mock_client_socket = Mock()

    mock_client_socket.recv.side_effect = [b'+++{"z": 4, "g": 87}---', None]

    handle_client(mock_client_socket, "mock_addr")
    call = mock_client_socket.sendall.call_args_list
    first_call = call[0]

    args, *_ = first_call.args
    response_json_dict = json.loads(args)

    assert response_json_dict.get("message") == "missing x and y values"
    mock_update_plot.assert_not_called()
