#include <algorithm>
#include <cctype>
#include <cmath>
#include <cstring>
#include <iostream>
#include <sstream>
#include <numeric>
#include <map>
#include <set>
#include <queue>
#include <vector>
#include <atcoder/modint>

using namespace std;
using namespace atcoder;

static const int64_t INF = 1LL << 60;
{% if mod %}
using mint = static_modint<{{ mod }}>;
static const size_t TABLE_SIZE = 1000000;

mint combination(int n, int r) {
	if (r > n) {
		return 0;
	}
	static mint fact[TABLE_SIZE + 1], fact_inv[TABLE_SIZE + 1];
	if (!fact[0].val()) {
		fact[0] = 1;
		for (int i = 1; i <= TABLE_SIZE; ++i) {
			fact[i] = fact[i - 1] * i;
		}
		fact_inv[TABLE_SIZE] = fact[TABLE_SIZE].inv();
		for (int i = TABLE_SIZE; i >= 1; --i) {
			fact_inv[i - 1] = fact_inv[i] * i;
		}
	}
	return fact[n] * fact_inv[r] * fact_inv[n - r];
}
{% endif %}
{% if prediction_success %}

{% if yes_str %}
bool solve({{ formal_arguments }}) {
	bool ans = false;


	return ans;
}
{% else %}
int64_t solve({{ formal_arguments }}) {
	{% if mod %}
	mint ans = 0;


	return ans.val();
	{% else %}
	int64_t ans = 0;


	return ans;
	{% endif %}
}
{% endif %}
{% endif %}

int main() {
#if DEBUG
	freopen("in_1.txt", "r", stdin);
#endif
{% if prediction_success %}
	{{input_part}}
{% if yes_str %}
	cout << (solve({{ actual_arguments }}) ? "{{ yes_str }}" : "{{ no_str }}") << endl;
{% else %}
	cout << solve({{ actual_arguments }}) << endl;
{% endif %}
{% else %}
	int64_t N, M, ans = 0;


/*
	cin >> N >> M;

	std::vector<int64_t> X(N), Y(N);
	for (int i = 0; i < N; i++) {
		std::cin >> X[i] >> Y[i];
	}
*/


	cout << ans << endl;
{% endif %}
	return 0;
}
