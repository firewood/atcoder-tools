<<<<<<< HEAD
#include<iostream>
#include<vector>
#include<string>
=======
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <deque>
#include <queue>
#include <stack>
#include <set>
#include <map>
#include <algorithm>
#include <functional>
#include <utility>
#include <bitset>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cstdio>
using namespace std;
>>>>>>> test_fmtprediction

void solve(long long N, long long M, std::vector<long long> a, std::vector<long long> b, std::vector<long long> t){

}
int main(){
    long long N;
<<<<<<< HEAD
    std::cin >> N;
    long long M;
    std::cin >> M;
=======
    std::scanf("%lld", &N);
    long long M;
    std::scanf("%lld", &M);
>>>>>>> test_fmtprediction
    std::vector<long long> a(M);
    std::vector<long long> b(M);
    std::vector<long long> t(M);
    for(int i = 0 ; i < M ; i++){
<<<<<<< HEAD
        std::cin >> a[i];
        std::cin >> b[i];
        std::cin >> t[i];
=======
        std::scanf("%lld", &a[i]);
        std::scanf("%lld", &b[i]);
        std::scanf("%lld", &t[i]);
>>>>>>> test_fmtprediction
    }
    solve(N, M, std::move(a), std::move(b), std::move(t));
    return 0;
}
