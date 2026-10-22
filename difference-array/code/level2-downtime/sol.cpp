#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    // a request at x <= 100000 writes to req[x + 1000], so we need 100000 + 1000 + 1 slots
    vector<int> req(101001, 0);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        req[x] += 1;           // request starts
        req[x + 1000] -= 1;    // request ends 1000 later
    }

    int mx = 0;
    int c = 0;
    for (int i = 0; i < (int)req.size(); i++) {
        c += req[i];
        mx = max(mx, c);
    }

    // ceil(mx / k)
    int ans = (mx + k - 1) / k;
    cout << ans << "\n";
    return 0;
}