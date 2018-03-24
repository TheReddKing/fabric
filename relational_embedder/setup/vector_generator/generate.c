
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>

#define MAX_STRING 100

int num_threads = 1;
char train_file[MAX_STRING],train_folder[10000];
int ITERATION_TYPES[] = {2,4,8,16};
int VECTOR_SIZES[] = {10,25,50,100,200,300};
int NEGATIVE_TYPES[] = {10,50,100};
char arr[sizeof(VECTOR_SIZES)/sizeof(VECTOR_SIZES[0])*sizeof(NEGATIVE_TYPES)/sizeof(NEGATIVE_TYPES[0])*sizeof(ITERATION_TYPES)/sizeof(ITERATION_TYPES[0])*2][10000];
int counts = 0;
pthread_t *ptg;
// A normal C function that is executed as a thread
// when its name is specified in pthread_create()
void handle_sigint(int sig)
{
    printf("Caught signal %d\n", sig);
    for (int a = 0; a < num_threads; a++) pthread_cancel(ptg[a]);
}
void *runThread(void * threadnum)
{
  signal(SIGINT, handle_sigint);
  for (int v=(int)threadnum;v<counts;v+=num_threads) {
    int o =  system(arr[v]);
    // printf("%s\n",arr[v]);
    if (o == 2) {
      handle_sigint(SIGINT);
      break;
    }
  }
  pthread_exit(NULL);
  return NULL;
}
int ArgPos(char *str, int argc, char **argv) {
  int a;
  for (a = 1; a < argc; a++) if (!strcmp(str, argv[a])) {
    if (a == argc - 1) {
      printf("Argument missing for %s\n", str);
      exit(1);
    }
    return a;
  }
  return -1;
}

int main(int argc, char **argv)
{
  printf("MUST RUN IN BIN FOLDER\n");
  int i;
  if (argc == 1) {
    printf("No args");
    return 0;
  }

  if ((i = ArgPos((char *)"-name", argc, argv)) > 0) {
    strcpy(train_file, argv[i + 1]);
  }
  strcpy(train_folder, argv[1]);
  printf("%s\n", train_folder);
  if ((i = ArgPos((char *)"-threads", argc, argv)) > 0) {
    num_threads = atoi(argv[i+1]);
  }
  // printf("%s\n", train_file);
  // WE NEED TO GENERATE THE Parameters


  int counter = 0;
  for(int i=0;i<sizeof(ITERATION_TYPES)/sizeof(ITERATION_TYPES[0]);i+=1) {
    for(int v=0;v<sizeof(VECTOR_SIZES)/sizeof(VECTOR_SIZES[0]);v+=1) {
      for(int n=0;n<sizeof(NEGATIVE_TYPES)/sizeof(NEGATIVE_TYPES[0]);n+=1) {
        // printf("%s\n", "HI");
        char s [10000];
        sprintf(s, "./word2vec -train %s/dataparsed/%s.txt -output %s/vectors/%s_v%d_n%d_i%d.txt -size %d -sample 1e-3 -negative %d -hs 0 -binary 0 -cbow 1 -iter %d", train_folder,train_file,train_folder,train_file,VECTOR_SIZES[v],NEGATIVE_TYPES[n],ITERATION_TYPES[i],VECTOR_SIZES[v],NEGATIVE_TYPES[n],ITERATION_TYPES[i]);
        // printf("%s\n", s);
        strcpy(arr[counter],s);
        // char *s;
        sprintf(s, "./word2vec_csv -train %s/dataparsed/%s.csv -output %s/vectors/%s_v%d_n%d_i%d_csv.txt -size %d -sample 1e-3 -negative %d -hs 0 -binary 0 -cbow 1 -iter %d", train_folder,train_file,train_folder,train_file,VECTOR_SIZES[v],NEGATIVE_TYPES[n],ITERATION_TYPES[i],VECTOR_SIZES[v],NEGATIVE_TYPES[n],ITERATION_TYPES[i]);
        strcpy(arr[counter+1],s);
        counter += 2;
      }
    }
  }
  counts = counter;

  signal(SIGINT, handle_sigint);
  pthread_t *pt = (pthread_t *)malloc(num_threads * sizeof(pthread_t));
  for (int v=0;v<num_threads;v+= 1) {
    printf("Initialize Thread\n");
    pthread_create(&pt[v], NULL, runThread,(void*)v);
    // pthread_join(tid, NULL);
    // system("echo 'heelo';");
  }
  ptg = pt;
  for (int a = 0; a < num_threads; a++) pthread_join(pt[a], NULL);

  exit(0);
  return 0;
}
