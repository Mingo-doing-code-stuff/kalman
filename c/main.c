#include <stdio.h>
#include "kalman1D.h"

int main(int argc, char const *argv[])
{
  SimpleKalman kalman = init();
  float positions[] = {10.05476138, 20.28458674, 29.49295574, 38.62625017, 49.53275068};
  float distances[] = {10.98636654,  10.00344322,  10.93369829,   9.85055967,  10.33031138};

  for (size_t i = 0; i < 4; i++)
  {
    kalman.predict_mean(&kalman, kalman.mean_mov, distances[i]);
    kalman.predict_var(&kalman,kalman.var_mov, kalman.mean_0);
  }
  
}
