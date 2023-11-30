import pytest
from server import find_pattern


# TODO: reconsider the meaning of 'negative' case
@pytest.mark.parametrize("data, pattern, expected_result, expected_index",
                         [("abcdefgh", "cd", True, 2),
                          (b"1234zxz5678", b"zxz", True, 4),
                          ("jxj", "jz", False, -1),
                          (b"jjjjjjjjjjjj", b"j4j", False, -1)]
                         )
def test_find_pattern_positive(data, pattern, expected_result, expected_index) -> None:
    result, index = find_pattern(data, pattern)
    assert result == expected_result, f"Failed to find pattern ({pattern} in data ({data}))"
    assert index == expected_index, "Incorrect index of pattern location"


@pytest.mark.parametrize("data, pattern, expected_result, expected_index",
                         [("abcde", "abcdef", False, -1),
                          ("00000", "000000000", False, -1),
                          ("one", "onee", False, -1)])
def test_find_pattern_pattern_exceeds_data_length(data, pattern, expected_result, expected_index) -> None:
    result, index = find_pattern(data, pattern)
    assert result == expected_result, f"Failed to find pattern ({pattern}) in data ({data}))"
    assert index == expected_index, "Incorrect index of pattern location"


@pytest.mark.parametrize("data, pattern, expected_result, expected_index",
                         [("abcde", "abcde", True, 0),
                          ("0", "0", True, 0),
                          ("one", "one", True, 0)])
def test_find_pattern_pattern_equals_data_length(data, pattern, expected_result, expected_index) -> None:
    result, index = find_pattern(data, pattern)
    assert result == expected_result, f"Failed to find pattern ({pattern}) in data ({data}))"
    assert index == expected_index, "Incorrect index of pattern location"


@pytest.mark.parametrize("data, pattern",
                         [(2.542, 10.4),
                          (True, "22.4556"),
                          ([1, 2, False], (5648, "5465"))])
def test_find_pattern_invalid_param_types(data, pattern) -> None:
    with pytest.raises(TypeError, match="data and pattern must be of type str or bytes"):
        find_pattern(data, pattern)


@pytest.mark.parametrize("data, pattern", [("abcdefgh", b"def"),
                                           (b"1234zxz5678", "zxz"),
                                           ("jjjjjjjjjjjj", b"jj")])
def test_find_pattern_inconsistent_param_types(data, pattern) -> None:
    with pytest.raises(TypeError, match="data and pattern must be of the same type"):
        find_pattern(data, pattern)
