
def add2all(tup: tuple, amt) -> tuple:
    res = [0] * len(tup)

    for i, v in enumerate(tup):
        res[i] = v + amt

    return tuple(res)

def add(tup1: tuple, tup2: tuple) -> tuple:
    res = [0] * len(tup1)

    for i, v in enumerate(tup1):
        res[i] = v + tup2[i]

    return tuple(res)
