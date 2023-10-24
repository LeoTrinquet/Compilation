int init(){

}

int malloc(int n)
{
  int r;
  r = *0;
  *0 = *0 + n;
  return r;
}

int free(int p)
{
  
}

int print_num_sub(int v)
{
  if(v != 0)
  {
    print_num_sub(v / 10);
    send (v%10) + 48;    
  }
  return 0;
}

int print_num(int v){
  if(v == 0)
  {
    send 48;
    send 10;
  }
  else if(v>0)
  {
    print_num_sub(v);
    send 10;

  }
  else if(v<0)
  {
    send 45;
    print_num_sub(-v);
    send 10;
  }
  return 0;
}