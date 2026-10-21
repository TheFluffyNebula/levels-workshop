#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;

    vector<int> diff(n + 2, 0);   // diff[1..n+1]
    for (int i = 0; i < m; i++) {
        int L, R;
        cin >> L >> R;
        diff[L] += 1;       // start counting here
        diff[R + 1] -= 1;   // stop counting after R
    }

    int ans = 0, running = 0;
    for (int i = 1; i <= n; i++) {
        running += diff[i];
        ans = max(ans, running);
    }
    cout << ans << "\n";
    return 0;
}