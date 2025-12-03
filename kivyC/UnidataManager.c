#include <stdio.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

// 배열 합계 계산
EXPORT int sum_array(int* arr, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}

// 배열 평균 계산
EXPORT double average_array(int* arr, int n) {
    if (n == 0) return 0.0;
    int total = sum_array(arr, n);
    return (double)total / n;
}
