def solve(k, t):
    req = [0] * (max(t) + 1001)
    for x in t:
        req[x] += 1          # request starts
        req[x + 1000] -= 1   # request ends 1000 later

    mx = 0
    c = 0
    for v in req:
        c += v
        mx = max(mx, c)
    return (mx + k - 1) // k   # ceil(mx / k)
