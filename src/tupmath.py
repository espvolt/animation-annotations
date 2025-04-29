
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

def add2(tup1: tuple[float, float], tup2: tuple[float, float]) -> tuple[float, float]:
    return (tup1[0] + tup2[0], tup1[1] + tup2[1])

def sub2(tup1: tuple[float, float], tup2: tuple[float, float]) -> tuple[float, float]:
    return (tup1[0] - tup2[0], tup1[1] - tup2[1])

def mult2(tup: tuple[float, float], a: float) -> tuple[float, float]:
    return (a * tup[0], a * tup[1])

def pinrect(p: tuple[float, float], rect: tuple[float, float, float, float]):
        return p[0] > rect[0] and p[1] > rect[1] and \
               p[0] < rect[0] + rect[2] and p[1] < rect[1] + rect[3]


def pinpoints(p: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float]):
    return p[0] > p1[0] and p[1] > p1[1] and p[0] < p2[0] and p[1] < p2[1]

def lerp_2(p1: tuple[float, float], p2: tuple[float, float], t: float):
     return add2(p1, mult2(sub2(p2, p1), t))

def lerp_3(a: tuple[float, float, float],
           b: tuple[float, float, float],
           c: float) -> tuple[float, float, float]:
    return (a[0] + (b[0] - a[0]) * c,
            a[1] + (b[1] - a[1]) * c,
            a[2] + (b[2] - a[2]) * c)
