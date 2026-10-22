"""Input generator for level 2 (Downtime).

An "input" is the tuple (k, xs): k requests per server, xs the request times.
The tools call:
    small(seed)        tiny random input; the seed picks a flavor
    large(size, seed)  size requests at random times (used by bench.py)
    to_text(inp)       the stdin text: "N k" then one time per line

Run `python gen.py SEED` to print one small input.

Flavors for small():
    edge     times chosen right around multiples of 1000, so requests start
             exactly when another one ends (the boundary the solution must get right)
    same     every request at the same time
    apart    requests spaced at least 1000 apart, so none overlap
    random   random times in a short range
    top      times at the very top of the allowed range (100000), where the array
             must be large enough for the "request ends" marker at time + 1000
"""
import random

MAX_T = 100000
FLAVORS = ["edge", "same", "apart", "random", "top"]


def small(seed):
    rnd = random.Random(seed)
    n = rnd.randint(1, 8)
    k = rnd.randint(1, 4)
    flavor = FLAVORS[seed % len(FLAVORS)]
    if flavor == "edge":
        xs = [max(0, rnd.randint(0, 3) * 1000 + rnd.choice([-1, 0, 0, 1, 500]))
              for _ in range(n)]
    elif flavor == "same":
        xs = [rnd.randint(0, 3000)] * n
    elif flavor == "apart":
        xs = [i * (1000 + rnd.randint(0, 3)) for i in range(n)]
    elif flavor == "top":
        xs = [MAX_T - rnd.randint(0, 3) for _ in range(n)]
    else:
        xs = [rnd.randint(0, 3000) for _ in range(n)]
    rnd.shuffle(xs)
    return k, xs


def large(size, seed=1):
    rnd = random.Random(seed)
    return 5, [rnd.randint(0, MAX_T) for _ in range(size)]


def to_text(inp):
    k, xs = inp
    return "\n".join([f"{len(xs)} {k}"] + [str(x) for x in xs]) + "\n"


if __name__ == "__main__":
    import sys
    print(to_text(small(int(sys.argv[1]) if len(sys.argv) > 1 else 0)), end="")