from app.utils.query.query_string_parser import QueryStringParser


def test_init_with_empty_string():
    target = QueryStringParser("")
    assert len(target.query_parameters) == 0


def test_init_with_none_value():
    target = QueryStringParser(None)
    assert len(target.query_parameters) == 0


def test_init_with_one_query_parameter():
    target = QueryStringParser("name=val")
    assert len(target.query_parameters) == 1


def test_init_with_advanced_parameters():
    target = QueryStringParser("name=val&name=val2&other_name=val3")
    assert len(target.query_parameters) == 2


def test_iter():
    target = QueryStringParser("name=val&name=val2&other_name=val3")
    for index, val in enumerate(target):
        if index == 0:
            assert val.param_name == "name"
        elif index == 1:
            assert val.param_name == "other_name"
        else:
            assert False
