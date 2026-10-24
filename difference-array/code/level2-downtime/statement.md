## Statement
Based on [Disastrous Downtime](https://open.kattis.com/problems/downtime) on Kattis.

Bob runs a web service that receives n requests. Request i arrives at millisecond
t_i and must start processing immediately; it takes exactly 1000 ms, so it is
active during [t_i, t_i + 1000). A server can handle at most k requests at the
same time. What is the minimum number of servers needed to handle every request?

## Input
```
n k
t_1
t_2
...
t_n
```
The times are in non-decreasing order, and several requests can share a time.

## Output
A single integer: the minimum number of servers.

## Constraints
- 1 <= n, k <= 100000
- 0 <= t_i <= 100000

## Samples
```
3 2
1000
1010
1999
```
Output: `2`
All three requests are being processed at time 1999, and a server handles at
most 2 at once, so 2 servers are needed.

```
2 1
0
1000
```
Output: `1`
The first request ends at 1000 (exclusive), exactly when the second begins,
so they never overlap and one server is enough.
