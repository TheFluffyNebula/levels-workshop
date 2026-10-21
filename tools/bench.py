#!/usr/bin/env python3
"""Time a level's brute force or fast solution on growing inputs (in-process).

Usage (from the levels-workshop folder):
    python tools/bench.py difference-array/code/level1-fence brute \
        --sizes 1000 2000 4000 --project 100000 --growth quadratic
    python tools/bench.py difference-array/code/level1-fence sol \
        --sizes 10000 100000

`brute` or `sol` means test/brute.py or test/sol.py. Only the solve() call is
timed, so input parsing is not included. Each size is run --runs times (default 5);
the table shows the mean and the minimum. Inputs come from test/gen.py large(size, seed).

--project P extrapolates the mean at the last size to size P, assuming the given
growth. That is a projection, not a measurement. Sizes run to completion, so pick
them with the slow solution in mind (--max-seconds stops the table once a size is slow).
"""
import argparse
import copy
import importlib.util
import os
import time


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fmt(seconds):
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    if seconds < 120:
        return f"{seconds:.2f} s"
    if seconds < 7200:
        return f"{seconds / 60:.1f} min"
    return f"{seconds / 3600:.1f} h"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("level_dir")
    ap.add_argument("which", choices=["brute", "sol"])
    ap.add_argument("--sizes", type=int, nargs="+", default=[1000, 2000, 4000])
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--max-seconds", type=float, default=60.0,
                    help="stop once a size's mean exceeds this")
    ap.add_argument("--project", type=int, default=None)
    ap.add_argument("--growth", choices=["linear", "quadratic"], default="quadratic")
    args = ap.parse_args()

    test_dir = os.path.join(os.path.abspath(args.level_dir), "test")
    gen = load(os.path.join(test_dir, "gen.py"), "level_gen")
    mod = load(os.path.join(test_dir, args.which + ".py"), "level_" + args.which)

    print(f"test/{args.which}.py   (solve() only, n = m = size, {args.runs} runs each)")
    print(f"{'size':>10} | {'mean':>10} | {'min':>10}")
    print("-" * 36)

    last = None
    for size in args.sizes:
        inp = gen.large(size, 1)
        times = []
        for _ in range(args.runs):
            data = copy.deepcopy(inp)           # copy outside the timer
            t0 = time.perf_counter()
            mod.solve(*data)
            times.append(time.perf_counter() - t0)
        mean = sum(times) / len(times)
        print(f"{size:>10} | {fmt(mean):>10} | {fmt(min(times)):>10}")
        last = (size, mean)
        if mean > args.max_seconds:
            print("(stopping: that size already exceeds --max-seconds)")
            break

    if args.project and last:
        size, mean = last
        power = 2 if args.growth == "quadratic" else 1
        est = mean * (args.project / size) ** power
        print(f"\nProjected at size {args.project}: about {fmt(est)} "
              f"({args.growth} growth from size {size}; extrapolated, not measured)")


if __name__ == "__main__":
    main()
