#!/usr/bin/env python3
"""Stress-test a level: brute force vs. solution on random inputs.

Usage (from the levels-workshop folder):
    python tools/stress.py difference-array/code/level1-fence
    python tools/stress.py difference-array/code/level1-fence --tests 5000

Expected layout of a level folder:
    sol.py, sol.cpp        the published solutions (read stdin, print the answer)
    test/gen.py            small(seed) -> input tuple, to_text(input) -> str
    test/brute.py          solve(*input) -> answer   (slow but obviously correct)
    test/sol.py            solve(*input) -> answer   (the fast solution as a function)

Two stages:
  1. In-process: brute.solve vs sol.solve on --tests random inputs (fast).
  2. Published files: sol.py and sol.cpp (if present) are run as real programs
     on --file-tests inputs and compared to the brute force. This checks the
     files viewers will actually copy, and the C++ translation. Use
     --file-tests 0 to skip.

On the first failure the input is saved to test/fail_input.txt, printed, and the
script exits with status 1.
"""
import argparse
import copy
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fail(test_dir, text, header, extra=()):
    path = os.path.join(test_dir, "fail_input.txt")
    with open(path, "w") as f:
        f.write(text)
    print(header)
    print("--- input ---")
    print(text.rstrip())
    for line in extra:
        print(line)
    print(f"(input saved to {path})")
    sys.exit(1)


def stage_in_process(gen, brute, sol, test_dir, tests, seed0):
    for k in range(tests):
        seed = seed0 + k
        inp = gen.small(seed)
        text = gen.to_text(inp)
        try:
            want = brute.solve(*copy.deepcopy(inp))
        except Exception as e:
            fail(test_dir, text, f"BRUTE FORCE crashed on test {k + 1} (seed {seed}): "
                                 f"{type(e).__name__}: {e}")
        try:
            got = sol.solve(*copy.deepcopy(inp))
        except Exception as e:
            fail(test_dir, text, f"test/sol.py crashed on test {k + 1} (seed {seed}): "
                                 f"{type(e).__name__}: {e}")
        if str(want).split() != str(got).split():
            fail(test_dir, text, f"MISMATCH in test/sol.py on test {k + 1} (seed {seed})",
                 ["--- brute force says ---", str(want),
                  "--- solution says ---", str(got)])
    print(f"test/sol.py: all {tests} tests passed (in-process)")


def stage_published(level, gen, brute, test_dir, tests, seed0):
    with tempfile.TemporaryDirectory() as work:
        targets = []
        py = os.path.join(level, "sol.py")
        cpp = os.path.join(level, "sol.cpp")
        if os.path.exists(py):
            targets.append(("sol.py", [sys.executable, py]))
        if os.path.exists(cpp):
            if shutil.which("g++") is None:
                print("sol.cpp: SKIPPED (g++ not found; install MinGW-w64 or use WSL2)")
            else:
                exe = os.path.join(work, "sol.out")
                r = subprocess.run(["g++", "-O2", "-std=c++17", "-o", exe, cpp],
                                   capture_output=True, text=True)
                if r.returncode != 0:
                    sys.exit(f"compile failed for sol.cpp:\n{r.stderr}")
                targets.append(("sol.cpp", [exe]))
        if not targets:
            print("no published sol.py / sol.cpp found; skipping file check")
            return

        for name, cmd in targets:
            for k in range(tests):
                seed = seed0 + k
                inp = gen.small(seed)
                text = gen.to_text(inp)
                want = str(brute.solve(*copy.deepcopy(inp)))
                try:
                    r = subprocess.run(cmd, input=text, capture_output=True,
                                       text=True, timeout=10)
                except subprocess.TimeoutExpired:
                    fail(test_dir, text, f"{name} timed out on test {k + 1} (seed {seed})")
                if r.returncode != 0:
                    tail = " | ".join(r.stderr.strip().splitlines()[-3:])
                    fail(test_dir, text, f"{name} crashed on test {k + 1} (seed {seed}): {tail}")
                if r.stdout.split() != want.split():
                    fail(test_dir, text, f"MISMATCH in published {name} on test {k + 1} (seed {seed})",
                         ["--- brute force says ---", want,
                          "--- " + name + " says ---", r.stdout.strip()])
            print(f"{name}: all {tests} tests passed (run as a program)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("level_dir")
    ap.add_argument("--tests", type=int, default=2000, help="in-process tests")
    ap.add_argument("--file-tests", type=int, default=200,
                    help="tests for the published sol.py / sol.cpp (0 to skip)")
    ap.add_argument("--seed0", type=int, default=1)
    args = ap.parse_args()

    level = os.path.abspath(args.level_dir)
    test_dir = os.path.join(level, "test")
    gen = load(os.path.join(test_dir, "gen.py"), "level_gen")
    brute = load(os.path.join(test_dir, "brute.py"), "level_brute")
    sol = load(os.path.join(test_dir, "sol.py"), "level_sol")

    stage_in_process(gen, brute, sol, test_dir, args.tests, args.seed0)
    if args.file_tests > 0:
        stage_published(level, gen, brute, test_dir, args.file_tests, args.seed0)


if __name__ == "__main__":
    main()