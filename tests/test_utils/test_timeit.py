import utils.timeit as lib


def test_arguments_metric_info():
    assert lib.arguments_metric_info() == 'no argument'
    assert lib.arguments_metric_info([1, 2, 3]) == '3 items'
    assert lib.arguments_metric_info([1, 2, 3], 'so', 'other', 'stuff') == '3 items'
    assert lib.arguments_metric_info(mylist=[1, 2, 3]) == '3 items'
    assert lib.arguments_metric_info(mylist=1) == 'no metric, int not handled'
