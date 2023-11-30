from unittest.mock import Mock, MagicMock, patch

import pytest

import server
from server import find_pattern


def test_find_pattern_bytes():
    assert find_pattern(b"1234zxz5678", b"zxz") == (True, 4)


# todo: bytes?
# TODO: refactor w/ messages, reconsider the meaning of 'negative' case
@pytest.mark.parametrize(
    "data, pattern, exp_result, expected_index",
    [("abcdefgh", "cd", True, 2),
     ("1234zxz5678", "zxz", True, 4),
     ("jxj", "j", True, 0),
     ("jjjjjjjjjjjj", "j4j", False, -1)]
)
def test_find_pattern_string_positive(data, pattern, exp_result, expected_index):
    result, index = find_pattern(data, pattern)
    assert result == exp_result, f"Failed to find pattern ({pattern} in data ({data}))"
    assert index == expected_index, "Incorrect index of pattern location"


# @pytest.mark.parametrize("data, pattern, expected_result", [("abcdefgh", "cdf", (False, -1)),
#                                                             ("1234zxz5678", "zxza", (False, -1)),
#                                                             ("jjjjjjjjjjjj", "j4j", (False, -1))])
# def test_find_pattern_string_negative(data, pattern, expected_result):
#     assert find_pattern(data, pattern) == expected_result


@pytest.mark.parametrize("data, pattern", [("abcde", "abcdef"),
                                           ("00000", "000000000"),
                                           ("one", "onee")])
def test_find_pattern_string_pattern_exceeds_data_length(data, pattern):
    with pytest.raises(ValueError, match="pattern length must not exceed data length"):
        find_pattern(data, pattern)


@pytest.mark.parametrize("data, pattern, expected_result", [("abcde", "abcde", (True, 0)),
                                                            ("0", "0", (True, 0)),
                                                            ("one", "one", (True, 0))])
def test_find_pattern_string_pattern_equals_data_length(data, pattern, expected_result):
    assert find_pattern(data, pattern) == expected_result


@pytest.mark.parametrize("data, pattern", [(2.542, 10.4),
                                           (True, "22.4556"),
                                           ([1, 2, False], (5648, "5465"))])
def test_find_pattern_incorrect_param_types(data, pattern):
    with pytest.raises(TypeError, match="data and pattern must be of type str or bytes"):
        find_pattern(data, pattern)


@pytest.mark.parametrize("data, pattern", [("abcdefgh", b"def"),
                                           (b"1234zxz5678", "zxz"),
                                           ("jjjjjjjjjjjj", b"jj")])
def test_find_pattern_inconsistent_param_types(data, pattern):
    with pytest.raises(TypeError, match="data and pattern must be of the same type"):
        find_pattern(data, pattern)


@patch("server.update_plot")
def test_mock_demo(mock_plot_function):
    my_mock = MagicMock()
    # return value
    # my_mock.return_value = 10

    my_mock.side_effect = [10, 9, 8, 7]

    assert my_mock() == 10
    assert my_mock() == 9
    assert my_mock() == 8
    assert my_mock() == 7

    mock_client_socket = MagicMock()

    # arrange data
    mock_client_socket.recv.side_effect = [b"asdophhhjasdpohhhajsdpoajk", None]

    server.handle_client(mock_client_socket, "mock_addr")

    mock_client_socket.assert_called_once_with("")
