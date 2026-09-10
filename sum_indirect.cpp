#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
#include <string.h>
#include <stdlib.h>

#include "sums.h"

void 
setup(int64_t N, int64_t A[])
{
   printf(" inside sum_indirect problem_setup, N=%lld \n", (long long)N);
   for (int64_t i = 0; i < N; i++)
      A[i] = lrand48() % N;
}

int64_t
sum(int64_t N, int64_t A[])
{
   int64_t sum = 0;
   for (int64_t i = 0; i < N; i++)
      sum += A[A[i]];
   return sum;
}

