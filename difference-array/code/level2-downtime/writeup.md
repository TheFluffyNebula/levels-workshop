## Simple Solution
The minimum number of servers Bob needs is the least number such that the number of servers times 
the number of requests they can each handle is at least the maximum number of requests at any moment. 

We can mark timeslots for every request. 
For example, if a request comes in at t=0 we can increment 0 through 999 by 1. 

After that we can take the max of the array to get the most number of requests at a time. 

Finally, we can use the peak request amount to get the number of servers needed. 

Note: there are a few ways to do ceiling division. One is the `while` loop in the
simple solution. Another is `math.ceil(mx / k)` in Python, which needs `import math` and
divides as a float first. The most common is integer arithmetic: `(mx + k - 1) // k` in
Python, or `(mx + k - 1) / k` in C++.

It works because adding k - 1 pushes any remainder over the next multiple of k, but leaves an
exact multiple where it is. For k = 2: mx = 4 gives (4 + 1) // 2 = 2, and mx = 5 gives
(5 + 1) // 2 = 3.

```python
n, k = map(int, input().split())
busy = [0] * 101001
for i in range(n):
    x = int(input())
    # request is active during [x, x + 1000)
    # paint every millisecond it covers
    for t in range(x, x + 1000):
        busy[t] += 1

peak = max(busy)
servers = 0
# smallest number of servers with capacity >= peak
while servers * k < peak:
    servers += 1
print(servers)
```

### Complexity
This solution runs in time O(1000 * n) due to marking 1000 slots for each of the n requests. 
This is at most 1000 * 100000 = 10^8.
However, we can achieve a better time complexity with the difference array.

## Does the simple solution pass?
Yes. On Kattis, the paint-every-millisecond version was accepted in C++ (0.02 s)
and in Python 3 (PyPy) (0.36 s) with the 2 second limit.
It only works because the window is a fixed 1000 ms, so the cost is 1000 * n. If each
request lasted 100,000 ms instead, painting would cost 10^10 operations, and only the
difference array would still be fast.

## Optimal Solution
A request at x is active from x to x + 999. So, we can increment at x and decrement at x + 1000. 

```python
n, k = map(int,input().split())
req = 101001 * [0]
for i in range(n):
    x = int(input())
    req[x] += 1
    req[x + 1000] -= 1
mx = 0
c=0
for i in range(len(req)):
    c += req[i]
    if c>mx:
        mx=c
# math.ceil(mx / k)
ans = (mx + k - 1) // k
print(ans)
```

### Complexity
Each of the n intervals is processed in O(1). There is also a sweep over all times. 
Thus, the time complexity is O(n + T) where T is the largest time, on the magnitude of about 100k or 10^5 operations. 

### Example: the boundary
Take n = 2, k = 1, with requests at t = 0 and t = 1000. The first request is active during
[0, 1000) and the second during [1000, 2000), so they never overlap.

| ms         | diff       | running |
|------------|------------|---------|
| 0          | +1         | 1       |
| 1 to 999   | 0          | 1       |
| 1000       | -1 and +1  | 1       |
| 1001 to 1999 | 0        | 1       |
| 2000       | -1         | 0       |

At 1000, the first request's end (-1) and the second request's start (+1) cancel
out, so the count never reaches 2. The peak is 1, and ceil(1 / 1) = 1 server. This is why the
decrement goes at x + 1000 and not at x + 999 or x + 1001.

### Common Mistakes
* Decrementing at x + 999 or x + 1001 instead of x + 1000, which miscounts requests that
  start exactly when another ends.
* An array that is too small. A request at t = 100000 writes to index 101000, so the array
  needs 101001 slots.

### How we know it's right
We compared the difference array against the paint-every-millisecond version on 2000
random small inputs, and ran the sol.py and sol.cpp in this repo as programs on 200 inputs
each. The generator deliberately includes requests exactly 1000 ms apart, many requests at
the same time, requests that never overlap, and times at the very top of the range (100000).
All of them matched.
