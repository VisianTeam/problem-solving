from functools import wraps
from time import time



def arguments_metric_info(*args, **kwargs) -> str:
    """Find metric within arguments"""
    if not args and not kwargs:
        return 'no argument'
    elif args:
        arg = args[0]
    else:
        arg = next(iter(kwargs.values()))

    try:
        info = f"{len(arg)} items"
    except TypeError:
        info = f"no metric, {type(arg).__name__} not handled"

    return info


def timeit(func):
    """decorator to print runtime for each function call"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = arguments_metric_info(*args, **kwargs)

        start = time()
        res = func(*args, **kwargs)
        time_spent = time() - start

        print(f"{func.__name__!r} run took {time_spent:.5f}s [{info}]")
        return res

    return wrapper
