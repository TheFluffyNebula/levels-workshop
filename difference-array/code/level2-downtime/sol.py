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