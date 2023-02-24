import algorithms.tsp as lib


def test_list_permutations():
    assert lib.list_permutations([1, 2, 3]) == [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert len(lib.list_permutations(list(range(7)))) == 5040


def test_get_best_path():
    """Example is built on following graph:

    path = "data/cities.csv"
    graph = CitiesGraph.from_file(path, [
        "Dallas",
        "Detroit",
        "Los Angeles",
        "Miami",
        "New York City",
        "Oklahoma City",
        "San Francisco",
    ])
    """

    nodes = [0, 1, 2, 3, 4, 5, 6]
    costs = {
        (4, 0): 3517098,
        (3, 4): 1779655,
        (4, 3): 1779655,
        (3, 1): 2056616,
        (5, 4): 2222330,
        (4, 6): 931577,
        (5, 1): 4107563,
        (0, 2): 2283221,
        (0, 5): 4520345,
        (1, 0): 559632,
        (1, 6): 4271219,
        (2, 5): 2277834,
        (1, 3): 2056616,
        (6, 2): 2443473,
        (6, 5): 2182103,
        (4, 2): 1613636,
        (3, 0): 2447810,
        (4, 5): 2222330,
        (5, 0): 4520345,
        (5, 6): 2182103,
        (3, 6): 2538516,
        (5, 3): 2072978,
        (0, 1): 559632,
        (2, 4): 1613636,
        (1, 2): 1950757,
        (0, 4): 3517098,
        (2, 1): 1950757,
        (1, 5): 4107563,
        (6, 1): 4271219,
        (6, 4): 931577,
        (3, 2): 329200,
        (4, 1): 3355696,
        (3, 5): 2072978,
        (5, 2): 2277834,
        (0, 3): 2447810,
        (2, 0): 2283221,
        (1, 4): 3355696,
        (0, 6): 4447606,
        (2, 3): 329200,
        (2, 6): 2443473,
        (6, 0): 4447606,
        (6, 3): 2538516
    }
    assert lib.find_best_sequence(nodes, costs) == [0, 1, 2, 3, 5, 6, 4, 0]
    costs.pop((0, 4))
    costs.pop((4, 0))
    assert lib.find_best_sequence(nodes, costs) == [0, 1, 3, 5, 6, 4, 2, 0]
