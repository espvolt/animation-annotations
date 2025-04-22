
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

def pinrect(p: tuple[float, float], rect: tuple[float, float, float, float]):
        return p[0] > rect[0] and p[1] > rect[1] and \
               p[0] < rect[0] + rect[2] and p[1] < rect[1] + rect[3]


def pinpoints(p: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float]):
    return p[0] > p1[0] and p[1] > p1[1] and p[0] < p2[0] and p[1] < p2[1]