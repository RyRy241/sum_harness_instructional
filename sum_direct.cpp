#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
#include <string.h>

#include "sums.h"

void 
setup(int64_t N, int64_t A[])
{
   (void)A; 
   printf(" inside direct_sum problem_setup, N=%lld \n", (long long)N);
}

int64_t
sum(int64_t N, int64_t A[])
{
   (void)A;

   int64_t sum = 0;
   for (int64_t i = 0; i < N; i++) {
      sum += i;
   }
   
   return sum;
}

