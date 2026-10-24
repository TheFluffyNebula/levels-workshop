## Simple Solution
The minimum number of servers Bob needs is the least number such that the number of servers times 
the number of requests they can each handle is at least the maximum number of requests at any moment. 

We can mark timeslots for every request. 
For example, if a request comes in at t=0 we can increment 0 through 999 by 1. 

After that we can take the max of the array to get the most number of requests at a time. 

Finally, we can use the peak request amount to get the number of servers needed. 

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
Each of the n intervals are processed in O(1). There is also a sweep over all times. 
Thus, the time complexity is O(max(n, max_t)), on the magnitude of about 100k or 10^5 operations. 
