from app.authentication.utils.str_utils import remove_brackets


def test_remove_brackets():
    assert remove_brackets("{Value}") == "Value"
    assert remove_brackets("Value") == "Value"
