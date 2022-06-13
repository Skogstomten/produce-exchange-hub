from app.utils.query.query_parameter import QueryParameter
from app.utils.string_values import StringValues


def test_can_initialize():
    target = QueryParameter('test', StringValues('val'))
    assert target.param_name == 'test'
    assert target.values.values[0] == 'val'


def test_can_initialize_with_only_one_value():
    target = QueryParameter('name', 123, 345)
    assert target.values.values[0] == '123'
    assert target.values.values[1] == '345'


def test_str_works_with_param_with_no_value():
    target = QueryParameter('name')
    assert str(target) == 'name'


def test_str_works_with_param_with_one_value():
    target = QueryParameter('name', 'val')
    assert str(target) == 'name=val'


def test_str_works_with_param_with_more_than_one_value():
    target = QueryParameter('name', 'val1', 'val2')
    assert str(target) == 'name=val1&name=val2'
