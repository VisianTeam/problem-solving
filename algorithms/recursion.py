def factorial(n: int) -> int:
    """Return value of n! (factorial n)"""
    if n < 0:
        raise ValueError('Negative numbers are not handle by current implementation')
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """Return value of the i-th element of the Fibonacci sequence"""
    if n < 0:
        raise ValueError('Fibonacci is not defined on negative numbers')
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def look_for_message(d: dict) -> list:
    temp = []
    if isinstance(d, dict):
        for n, p in d.items():
            if isinstance(p, dict) or isinstance(p, list):
                temp.extend(look_for_message(p))
            elif n == "message":
                temp.append(p)
    else:
        for i in d:
            if isinstance(i, dict):
                temp.extend(look_for_message(i))

    return temp
