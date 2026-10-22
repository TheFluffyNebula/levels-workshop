## Statement
Also available on https://open.kattis.com/problems/downtime

Bob has to handle n requests. Each request takes 1000ms to process. He will use servers to handle these requests, 
with each handling up to k requests. What is the minimum number of servers needed to handle these requests?

## Input
```
n k
t_1
t_2
...
t_n
```

## Output
A single integer: the minimum number of servers required to handle all requests. 

## Constraints
```
1 <= n, k <= 100000
0 <= t_i <= 100000
```

## Sample
```
3 2
1000
1010
1999
```
Output 2
(at time t=1999 we need 2 servers)
