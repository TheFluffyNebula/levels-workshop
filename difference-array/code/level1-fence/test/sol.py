def solve(n, segs):
    # diff[1..n+1]; the extra slot at n + 1 absorbs the "stop" marker of a segment ending at n
    diff = [0] * (n + 2)
    for L, R in segs:
        diff[L] += 1       # start counting here
        diff[R + 1] -= 1   # stop counting after R

    ans = 0
    running = 0
    for i in range(1, n + 1):
        running += diff[i]
        ans = max(ans, running)
    return ans
