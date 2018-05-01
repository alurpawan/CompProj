float average (float *a, int n) 
{
  float average = 0.0;

  for(int i = 0; i < n; i++)
 {
    average = average + (a[i] / n);
  }
  return average;
}
