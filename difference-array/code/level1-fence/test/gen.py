"""Input generator for level 1 (fence).

An "input" is the tuple (n, segs), where segs is a list of (L, R) pairs.
The tools call:
    small(seed)        tiny random input; the seed also picks a flavor so edge
                       cases show up regularly
    large(size, seed)  n = m = size, random segments (used by bench.py)
    to_text(inp)       the stdin text for the published sol.py / sol.cpp

Run `python gen.py SEED` to print one small input.

Flavors:
    random  random segments
    full    every painter covers the whole fence (max layers = m)
    point   every painter has L = R
    single  exactly one painter
    ends    segments that touch post 1 or post n
"""
import random

MODES = ["random", "full", "point", "single", "ends"]


def _segments(n, m, mode, rnd):
    segs = []
    for _ in range(m):
        if mode == "full":
            l, r = 1, n
        elif mode == "point":
            l = r = rnd.randint(1, n)
        elif mode == "ends":
            if rnd.random() < 0.5:
                l, r = 1, rnd.randint(1, n)
            else:
                l, r = rnd.randint(1, n), n
        else:  # random / single
            l = rnd.randint(1, n)
            r = rnd.randint(l, n)
        segs.append((l, r))
    return segs


def small(seed):
    rnd = random.Random(seed)
    n = rnd.randint(1, 8)
    m = rnd.randint(1, 8)
    mode = MODES[seed % len(MODES)]
    if mode == "single":
        m = 1
    return n, _segments(n, m, mode, rnd)


def large(size, seed=1):
    rnd = random.Random(seed)
    return size, _segments(size, size, "random", rnd)


def to_text(inp):
    n, segs = inp
    lines = [f"{n} {len(segs)}"] + [f"{l} {r}" for l, r in segs]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import sys
    print(to_text(small(int(sys.argv[1]) if len(sys.argv) > 1 else 0)), end="")
