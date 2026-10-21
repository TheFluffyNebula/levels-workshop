def solve(n, segs):
    ans = 0
    for i in range(n): # check every post...
        c = 0
        for L, R in segs: # against every painter
            # i + 1 since posts are numbered from 1
            if L <= i + 1 <= R:
                c += 1
        ans = max(ans, c)
    return ans
