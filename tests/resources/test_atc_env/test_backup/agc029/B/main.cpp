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

void solve(long long N, std::vector<long long> A){

}

int main(){
    long long N;
<<<<<<< HEAD
    std::cin >> N;
    std::vector<long long> A(N);
    for(int i = 0 ; i < N ; i++){
        std::cin >> A[i];
=======
    std::scanf("%lld", &N);
    std::vector<long long> A(N);
    for(int i = 0 ; i < N ; i++){
        std::scanf("%lld", &A[i]);
>>>>>>> test_fmtprediction
    }
    solve(N, std::move(A));
    return 0;
}
