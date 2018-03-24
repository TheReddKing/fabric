
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
#include <dirent.h>

#define MAX_STRING 100

int num_threads = 1;
char train_files[1000],train_folder[1000];

char arr[10000][1000];

// void* temparr;
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
  // char arr[counts][1000] = *temparr;
  signal(SIGINT, handle_sigint);
  for (int v=(int)threadnum;v<counts;v+=num_threads) {
    int o =  system(arr[v]);
    // printf("%s\n",arr[v]);
    printf("%d\n",o);
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

  // if ((i = ArgPos((char *)"-vectors", argc, argv)) > 0) {
  //   strcpy(train_files, argv[i + 1]);
  // }
  char s [10000];
  strcpy(train_folder, argv[1]);
  sprintf(s,"%s/vectors",train_folder);
  strcpy(train_files,s);
  printf("%s\n", train_folder);
  if ((i = ArgPos((char *)"-threads", argc, argv)) > 0) {
    num_threads = atoi(argv[i+1]);
  }



  DIR *d;
  struct dirent *dir;
  d = opendir(train_files);
  int filenum = 0;
  if (d) {
    while ((dir = readdir(d)) != NULL)
    {
      if (strstr(dir->d_name,".txt") != NULL) {
        filenum += 1;
      }
    }
    closedir(d);
  }
  // char ff[filenum][1000];
  d = opendir(train_files);
  filenum = 0;
  if (d){
    while ((dir = readdir(d)) != NULL)
    {
      // strcpy(ff[filenum],dir->d_name);
      if (strstr(dir->d_name,".txt") != NULL) {
          // contains
          char s [10000];
          sprintf(s, "python ./../checkAccuracy.py %s %s/%s",train_folder,train_files,dir->d_name);
          strcpy(arr[filenum],s);
          filenum += 1;
      }
    }
    closedir(d);
  }
  // arr = *ff;
  counts = filenum;

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
