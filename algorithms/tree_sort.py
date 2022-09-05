import numpy as np

from utils.timeit import timeit


class Tree:
    __slots__ = ["value", "node_inf", "node_sup"]

    def __init__(self, value: float, node_inf: "Tree" = None, node_sup: "Tree" = None):
        self.value = value
        self.node_inf = node_inf
        self.node_sup = node_sup

    def insert(self, value):
        if value < self.value:
            if self.node_inf is None:
                self.node_inf = Tree(value)
                return
            self.node_inf.insert(value)
        else:
            if self.node_sup is None:
                self.node_sup = Tree(value)
                return
            self.node_sup.insert(value)

    def to_list(self):
        return (
            (self.node_inf.to_list() if self.node_inf is not None else [])
            + [self.value]
            + (self.node_sup.to_list() if self.node_sup is not None else [])
        )


@timeit
def basic_sort(l):
    return sorted(l)


@timeit
def tree_sort(_list):
    tree = Tree(_list[0])
    for value in _list[1:]:
        tree.insert(value)
    return tree.to_list()


if __name__ == "__main__":

    for n in [10e2, 10e4, 10e6]:
        l = list(np.random.rand(int(n)))
        reference = basic_sort(l)
        our_result = tree_sort(l)
        assert reference == our_result
