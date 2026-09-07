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
   (void)N; (void)A; // preventing any unused variable warnings
   printf(" inside direct_sum problem_setup, N=%lld \n", N);
}

int64_t
sum(int64_t N, int64_t A[])
{
   (void)N; (void)A; // preventing any unused variable warnings

   int64_t sum = 0;
   for (int64_t i = 0; i < N; i++) {
      sum += i;
   }
   printf(" inside direct_sum perform_sum, N=%lld \n", N);

   return sum;
}

