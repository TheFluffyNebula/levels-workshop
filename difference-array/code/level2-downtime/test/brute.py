def solve(k, xs):
    # paint every millisecond a request is active, then take the busiest one
    busy = [0] * (max(xs) + 1000)
    for x in xs:
        for t in range(x, x + 1000):     # a request at x is active during [x, x + 1000)
            busy[t] += 1
    peak = max(busy)
    servers = 0
    while servers * k < peak:            # smallest number of servers with capacity >= peak
        servers += 1
    return servers
