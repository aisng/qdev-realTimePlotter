import json
import random

import pytest
import server
from unittest.mock import Mock, MagicMock, patch
from server import find_pattern


def test_find_pattern_bytes() -> None:
    assert find_pattern(b"1234zxz5678", b"zxz") == (True, 4)


# todo: bytes?
# TODO: refactor w/ messages, reconsider the meaning of 'negative' case
@pytest.mark.parametrize(
    "data, pattern, expected_result, expected_index",
    [("abcdefgh", "cd", True, 2),
     ("1234zxz5678", "zxz", True, 4),
     ("jxj", "j", True, 0),
     ("jjjjjjjjjjjj", "j4j", False, -1)]
)
def test_find_pattern_string_positive(data, pattern, expected_result, expected_index) -> None:
    result, index = find_pattern(data, pattern)
    assert result == expected_result, f"Failed to find pattern ({pattern} in data ({data}))"
    assert index == expected_index, "Incorrect index of pattern location"


# @pytest.mark.parametrize("data, pattern, expected_result", [("abcdefgh", "cdf", (False, -1)),
#                                                             ("1234zxz5678", "zxza", (False, -1)),
#                                                             ("jjjjjjjjjjjj", "j4j", (False, -1))])
# def test_find_pattern_string_negative(data, pattern, expected_result):
#     assert find_pattern(data, pattern) == expected_result

# TODO: add bytes
@pytest.mark.parametrize("data, pattern, expected_result, expected_index",
                         [("abcde", "abcdef", False, -1),
                          ("00000", "000000000", False, -1),
                          ("one", "onee", False, -1)])
def test_find_pattern_pattern_exceeds_data_length(data, pattern, expected_result, expected_index) -> None:
    # with pytest.raises(ValueError, match="pattern length must not exceed data length"):
    #     find_pattern(data, pattern)
    result, index = find_pattern(data, pattern)
    assert result == expected_result, f"Failed to find pattern ({pattern}) in data ({data}))"
    assert index == expected_index, "Incorrect index of pattern location"


@pytest.mark.parametrize("data, pattern, expected_result", [("abcde", "abcde", (True, 0)),
                                                            ("0", "0", (True, 0)),
                                                            ("one", "one", (True, 0))])
def test_find_pattern_string_pattern_equals_data_length(data, pattern, expected_result) -> None:
    assert find_pattern(data, pattern) == expected_result


@pytest.mark.parametrize("data, pattern", [(2.542, 10.4),
                                           (True, "22.4556"),
                                           ([1, 2, False], (5648, "5465"))])
def test_find_pattern_incorrect_param_types(data, pattern) -> None:
    with pytest.raises(TypeError, match="data and pattern must be of type str or bytes"):
        find_pattern(data, pattern)


# ok - positive test, error - negative case (another test)


@pytest.mark.parametrize("data, pattern", [("abcdefgh", b"def"),
                                           (b"1234zxz5678", "zxz"),
                                           ("jjjjjjjjjjjj", b"jj")])
def test_find_pattern_inconsistent_param_types(data, pattern) -> None:
    with pytest.raises(TypeError, match="data and pattern must be of the same type"):
        find_pattern(data, pattern)


@patch("server.send_response")
@patch("server.update_plot")
def test_handle_client_positive(mock_update_plot, mock_send_response) -> None:
    mock_client_socket = MagicMock()

    # AAA - arrange, act, assert

    # data preparation
    # arrange
    mock_client_socket.recv.side_effect = [b"+", b"+", b"+", b'{', b'"', b'x', b'"', b':', b' ', b'1',
                                           b',', b' ', b'"', b'y', b'"', b':', b' ', b'1', b'}', b"-", b"-",
                                           b"-", None]

    # act
    server.handle_client(mock_client_socket, "mock_addr")

    # assert
    mock_send_response.assert_called_with(mock_client_socket, "ERROR", "packet not received")
    mock_update_plot.assert_called_once_with(x=1, y=1)
