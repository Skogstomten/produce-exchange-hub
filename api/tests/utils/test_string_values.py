from app.utils.string_values import StringValues


def test_can_create_string_values_without_values():
    target = StringValues()
    assert target.values is not None
    assert len(target.values) == 0


def test_can_create_with_values_and_values_are_correct():
    target = StringValues('val1', 'val2', 'val3')
    assert target.values == ['val1', 'val2', 'val3']


def test_can_append_values():
    target = StringValues('val1')
    target.append('val2', 'val3')
    assert target.values == ['val1', 'val2', 'val3']


def test_can_iterate():
    target = StringValues('val1', 'val2')
    for index, val in enumerate(target):
        if index == 0:
            assert val == 'val1'
        elif index == 1:
            assert val == 'val2'
        else:
            assert False


def test_can_get_size_of():
    target = StringValues('1', '2')
    assert len(target) == 2
