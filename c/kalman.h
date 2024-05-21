#ifndef kalman_h
#define kalman_h

// TEMP: 
#include <stdio.h> // Include stdio.h for printf

// Declare the KalmanFilter struct
typedef struct KalmanFilter KalmanFilter;

struct KalmanFilter
{
  float _err_measure;
  float _err_estimate;
  float _process_noise;
  float _current_estimate;
  float _last_estimate;
  float _kalman_gain;

  // Function pointers (= black magic stuff)
  float (*updateEstimate)(KalmanFilter *filter, float mea);
  void (*setMeasurementError)(KalmanFilter *filter, float mea_e);
  void (*setEstimateError)(KalmanFilter *filter, float est_e);
  void (*setProcessNoise)(KalmanFilter *filter, float q);
  float (*getKalmanGain)(KalmanFilter *filter);
  float (*getEstimateError)(KalmanFilter *filter);
  void (*sut)(int reps);
};

// Define function pointer types
typedef float (*UpdateEstimateFunction)(KalmanFilter *filter, float mea);
typedef void (*SetMeasurementErrorFunction)(KalmanFilter *filter, float mea_e);
typedef void (*SetEstimateErrorFunction)(KalmanFilter *filter, float est_e);
typedef void (*SetProcessNoiseFunction)(KalmanFilter *filter, float q);
typedef float (*GetKalmanGainFunction)(KalmanFilter *filter);
typedef float (*GetEstimateErrorFunction)(KalmanFilter *filter);
typedef void (*SayHelloFunction)(int reps);

void sayHello(int reps)
{
  while (reps > 0)
  {
    printf("hello, you an idiot\n");
    reps -= 1;
  }
}

void setMeasurementError(KalmanFilter *filter, float mea_e)
{
  filter->_err_measure = mea_e;
}

void setEstimateError(KalmanFilter *filter, float est_e)
{
  filter->_err_estimate = est_e;
}

void setProcessNoise(KalmanFilter *filter, float q)
{
  filter->_process_noise = q;
}

float updateEstimate(KalmanFilter *filter, float mea)
{
  // Implement the Kalman filter update logic here.
  // Example: Calculate and update current estimate based on mea and other parameters.
  filter->_last_estimate = filter->_current_estimate;
  filter->_kalman_gain = filter->_err_estimate / (filter->_err_estimate + filter->_err_measure);
  filter->_current_estimate = filter->_last_estimate + filter->_kalman_gain * (mea - filter->_last_estimate);
  filter->_err_estimate = (1 - filter->_kalman_gain) * filter->_err_estimate;

  // Return the new current estimate
  return filter->_current_estimate;
}

float getKalmanGain(KalmanFilter *filter)
{
  return filter->_kalman_gain;
}

float getEstimateError(KalmanFilter *filter)
{
  return filter->_err_estimate;
}

KalmanFilter new(
    float err_measure,
    float err_estimate,
    float q)
{
  KalmanFilter k = {
      .updateEstimate = updateEstimate,
      .setMeasurementError = setMeasurementError,
      .setEstimateError = setEstimateError,
      .setProcessNoise = setProcessNoise,
      .getKalmanGain = getKalmanGain,
      .getEstimateError = getEstimateError,
      .sut = sayHello,
      ._err_measure = err_measure,
      ._err_estimate = err_estimate,
      ._process_noise = q,
      ._current_estimate = 0,
      ._last_estimate = 0,
      ._kalman_gain = 0};

  return k;
}

#endif