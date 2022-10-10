def factoriel(n):
    if n <= 1:
        return 1
    else:
        return n * factoriel(n - 1)


assert factoriel(5) == 120 and factoriel(7) == 5040


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(16))
assert fibonacci(6) == 8


def pars(d):
    temp = []
    if isinstance(d, dict):
        for n, p in d.items():
            if isinstance(p, dict) or isinstance(p, list):
                temp.extend(pars(p))
            elif n == "message":
                temp.append(p)
    else:
        for i in d:
            if isinstance(i, dict):
                temp.extend(pars(i))

    return temp


b = {
    "message": "1",
    "heelo": "2",
    "soius": {"message": "77", "pour": "jrjrj"},
    "ejej": {"message": "09", "kkkkkk": {"okokokok": "eee", "jjjj": {"message": "3"}}},
}

h = {
    "message": "1",
    "heelo": "2",
    "soius": [{"message": "77", "blai": "jrjrj"}, 1, 5],
    "ejej": {"message": "09", "kkkkkk": {"okokokok": "eee", "jjjj": {"message": "3"}}},
}
print(pars(h))
