## Naive Solution
We could check each post, counting the layers of paint that cover it. 
This approach would be O(n * m) since for each of the n posts we're 
checking if a post is covered by the m painters. 

```python
n, m = map(int, input().split())
L, R = [], []
for i in range(m):
    a, b = map(int, input().split())
    L.append(a)
    R.append(b)

ans = 0
for i in range(n): # check every post...
    c = 0
    for j in range(m): # against every painter
        # i + 1 since the input is 1-indexed
        if L[j] <= i + 1 <= R[j]:
            c += 1
    ans = max(ans, c)
print(ans)
```

A computer does roughly 100 million simple operations per second, 
and judges usually give 1-2 seconds. Thus, the budget is 10^8 operations, 
with Python being closer to 10^7. O(n * m) here is 10^10. In C++, that's 
about tens of seconds to a couple of minutes (estimated), and in Python many minutes. 
So, how can we speed this up?

## Full Solution
We can use a technique called the Difference Array. This is an array where we 
process an interval using two edits: one where it's active, and one where it deactivates. 
In general, it's +1 at arr[L] and -1 at arr[R + 1], though the number can change, ex. a 
painting operation that applies 2 layers instead of one would have +2 and -2. 

### Warm-up: one painter
Let n = 5 and m = 1, with the painter covering [2, 4]. The painter makes two edits:
+1 at L = 2, and -1 at R + 1 = 5.

| post i  | 1 | 2 | 3 | 4 | 5  |
|---------|---|---|---|---|----|
| diff[i] | 0 | 1 | 0 | 0 | -1 |
| running | 0 | 1 | 1 | 1 | 0  |

Sweeping left to right, we keep a running total `running`. At post 2 the +1 turns the painter
on, so `running` becomes 1 and stays there. At post 5 the -1 turns it off, and `running` returns
to 0. Posts 2, 3, and 4 end up with one layer, which is exactly [2, 4].


### Stacking: the full sample
One painter doesn't show what the difference array is really for, so let's use the
sample: n = 5, with painters [1, 3], [2, 5], and [3, 4].

We keep the array 1-indexed, with one spare slot at the end. Each painter makes two edits:
+1 at L, and -1 at R + 1.

- Painter [1, 3]: +1 at 1, -1 at 4
- Painter [2, 5]: +1 at 2, -1 at 6
- Painter [3, 4]: +1 at 3, -1 at 5

The `-1` at index 6 sits one past the last post. We never sweep over it, but we still
need the slot so the edit doesn't go out of bounds. That's why the array has size n + 2.

| post i    | 1 | 2 | 3 | 4  | 5  |
|-----------|---|---|---|----|----|
| diff[i]   | 1 | 1 | 1 | -1 | -1 |
| running   | 1 | 2 | 3 | 2  | 1  |

The running sum is the number of layers on each post, and its maximum is 3, which matches
the sample answer.

### Code
```python
n, m = map(int, input().split())

# diff[1..n+1]; the extra slot at n + 1 absorbs the "stop" marker of a segment ending at n
diff = [0] * (n + 2)
for _ in range(m):
    L, R = map(int, input().split())
    diff[L] += 1       # start counting here
    diff[R + 1] -= 1   # stop counting after R

ans = 0
running = 0
for i in range(1, n + 1):
    running += diff[i]
    ans = max(ans, running)
print(ans)
```

### Why does this work?

At post p, the running sum has added every +1 at or before p (painters who have started)
and every -1 at or before p (painters who have already finished). What remains is exactly
the painters whose segment covers p. The sweep rebuilds each post's layer count
without ever touching the posts in between.

### Common Mistakes
* Subtracting at R, dropping the last post's layer
* No padding/check for R + 1: results in trying to write out of bounds

### Complexity

Each painter costs two edits, and the sweep visits each post once, so this is O(n + m).
At n = m = 10^5 that's about 2 * 10^5 operations, compared to 10^10 for the naive
approach: roughly 50,000 times fewer, and well inside the 10^8 budget even in Python.

### How we know it's right

A solution that is fast but wrong is worthless, so we compared it against the naive
solution, which is slow but obviously correct, on [2000] random small inputs. The generator
focuses on tiny n and m so that endpoints collide often, and also includes edge cases:
a single painter, L = R, and every painter covering the whole fence. All [2000] matched.

