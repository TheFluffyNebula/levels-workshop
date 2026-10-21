# tools

Shared scripts for testing and timing the solutions in each level.

Requirements: Python 3. A C++ compiler (`g++`) is optional and only needed to
test `sol.cpp` files.

Run everything from the repository root. On Windows, use `py` if `python` isn't
recognized.

## stress.py

Checks a level's solution against a brute force on random inputs.

```
python tools/stress.py difference-array/code/level1-fence
python tools/stress.py difference-array/code/level1-fence --tests 5000
```

It runs in two stages:

1. **In-process.** `test/brute.py` and `test/sol.py` are compared by calling
   `solve()` directly on `--tests` random inputs (default 2000).
2. **Published files.** The level's `sol.py` and `sol.cpp` are run as real
   programs on `--file-tests` inputs (default 200) and compared with the brute
   force. This checks the exact files you would submit, including the C++
   translation. If `g++` isn't installed, the C++ check is skipped with a
   message. Use `--file-tests 0` to skip this stage entirely.

On the first failure it prints the input and both answers, saves the input to
`test/fail_input.txt`, and exits with status 1.

## bench.py

Times `test/brute.py` or `test/sol.py` on growing inputs.

```
python tools/bench.py difference-array/code/level1-fence brute --sizes 1000 2000 4000 --project 100000
python tools/bench.py difference-array/code/level1-fence sol --sizes 10000 100000
```

- Only the `solve()` call is timed, so input parsing is not included.
- Each size runs `--runs` times (default 5); the table shows the mean and minimum.
- `--project P` extrapolates the mean at the last size to size `P` (`--growth
  quadratic` or `linear`). This is a projection, not a measurement.
- `--max-seconds` stops the table once a size is slow (default 60).
- Timings depend on your machine, so quote your own numbers.

## What a level needs

```
levelN-name/
  sol.py, sol.cpp      published solutions: read stdin, print the answer
  test/
    gen.py             small(seed), large(size, seed), to_text(inp)
    brute.py           solve(*inp): slow but obviously correct
    sol.py             solve(*inp): the fast solution as a function
```

An "input" is a tuple of the arguments to `solve`. For level 1 it is
`(n, segs)`, where `segs` is a list of `(L, R)` pairs.

- `small(seed)` returns a tiny random input. Keep sizes small so that boundary
  cases (equal endpoints, overlaps) come up often, and vary the "flavor" with
  the seed so edge cases are covered regularly.
- `large(size, seed)` returns an input of the given size for benchmarking.
- `to_text(inp)` returns the stdin text that the published `sol.py` and
  `sol.cpp` expect.
- `solve` must not modify its arguments, because the brute force and the
  solution receive copies of the same input.
