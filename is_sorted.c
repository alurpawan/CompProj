bool example_is_sorted (int *a, int n) 
{
  int iss = 1;
  int prev = -999;
  int i;
 for(i = 0; i < n; i++) 
{
    iss = iss && (prev < a[i]);
    prev = a[i];
  
}

  return iss;
