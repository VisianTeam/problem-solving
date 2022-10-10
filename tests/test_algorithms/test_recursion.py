import pytest

from algorithms import algo_recur as recursion
from utils.timeout import timeout


@pytest.mark.parametrize('n,res', [
    (1, 1),
    (5, 120),
    (0, 1),
    (10, 3628800),
])
def test_factorial(n, res):
    assert recursion.factorial(n) == res

@pytest.mark.parametrize('n', [-1, -10])
def test_factorial_raises(n):
    with pytest.raises(ValueError):
        recursion.factorial(n)


@pytest.mark.parametrize('n,res', [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (10, 55),
])
def test_fibo(n, res):
    assert recursion.fibonacci(n) == res


def test_fibo_perf():
    with timeout(1):
        assert recursion.fibonacci(100) == 354224848179261915075


@pytest.mark.parametrize('n', [-1, -10])
def test_fibo_raises(n):
    with pytest.raises(ValueError):
        recursion.fibonacci(n)


def test_look_for_messages_empty():
    assert recursion.look_for_message({}) == []


def test_look_for_messages_simple():
    assert recursion.look_for_message({
        "key1": "1",
        "message": "1st_msg",
        "key2": "2",
        "key3": "3",
    }) == ["1st_msg"]


def test_look_for_messages_3layers():
    assert recursion.look_for_message({
        "message": "1st_msg",
        "key1": "1",
        "key2": {"message": "2nd_msg", "key21": "21"},
        "key3": {"key31": {"key311": "311", "312": {"message": "3rd_msg"}}, "message": "4th_msg"},
    }) == ["1st_msg", "2nd_msg", "3rd_msg", "4th_msg"]


def test_look_for_messages_with_list():
    assert recursion.look_for_message({
        "message": "1st_msg",
        "key1": "1",
        "key2": [{"message": "2nd_msg", "key21": "21"}, 1, 3],
    }) == ["1st_msg", "2nd_msg"]
