from functools import wraps
from time import time


def timeit(func):
    @wraps(func)
    def wrapper(arg, *args, **kwargs):
        start = time()
        res = func(arg, *args, **kwargs)
        time_spent = time() - start

        try:
            info = f"{len(arg)} items"
        except TypeError:
            info = f"no metric, {type(arg)} not handled"
        print(f"{func.__name__!r} run took {time_spent:.5f}s [{info}]")
        return res

    return wrapper
