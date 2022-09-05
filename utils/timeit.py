from functools import wraps
from time import time


def timeit(func):
    @wraps(func)
    def wrapper(arg, *args, **kwargs):
        start = time()
        res = func(arg, *args, **kwargs)
        time_spent = time() - start

        if isinstance(arg, (list, tuple, dict, set)):
            info = f"{len(arg)} items"
        else:
            info = f"no metric, {type(arg)} not handled"
        print(f"Took {time_spent:.5f}s in {func.__name__!r} [{info}]")
        return res

    return wrapper
