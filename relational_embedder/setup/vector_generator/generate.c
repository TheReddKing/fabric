
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>

#define MAX_STRING 100

int num_threads = 1;
char train_file[MAX_STRING],train_folder[MAX_STRING];
// A normal C function that is executed as a thread
// when its name is specified in pthread_create()
void *runThread(void * threadnum)
{

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
  int i;
  if (argc == 1) {
    printf("No args");
    return 0;
  }

  if ((i = ArgPos((char *)"-name", argc, argv)) > 0) {
    strcpy(train_file, argv[i + 1]);
  }
  if ((i = ArgPos((char *)"-folder", argc, argv)) > 0) {
    strcpy(train_folder, argv[i + 1]);
  }
  if ((i = ArgPos((char *)"-threads", argc, argv)) > 0) {
    num_threads = atoi(argv[i+1]);
  }
  // printf("%s\n", train_file);
  // WE NEED TO GENERATE THE Parameters

  int ITERATION_TYPES[] = {2,4,8,16};
  int VECTOR_SIZES[] = {10,25,50,100,200,300};
  int NEGATIVE_TYPES[] = {10,50,100};
  // int* CSV_NAME = train_folder
  // for(int i=0;i<sizeof(ITERATION_TYPES)/sizeof(ITERATION_TYPES[0]);i+=1) {
  //   for(int v=0;v<sizeof(VECTOR_SIZES)/sizeof(VECTOR_SIZES[0]);v+=1) {
  //     for(int n=0;n<sizeof(NEGATIVE_TYPES)/sizeof(NEGATIVE_TYPES[0]);n+=1) {
  //       char*s;
  //       sprintf(s, "./word2vec -train %s/dataparsed/.txt",train_folder);
  //       printf("%s\n", s);
  //       sprintf(s, "./word2vec -train %s/dataparsed/%s.txt -output %s/vectors/%s_v%d_n%d_i%d.txt -size %d -sample 1e-3 -negative %d -hs 0 -binary 0 -cbow 1 -iter %d", train_folder,train_file,train_folder,train_file,VECTOR_SIZES[v],NEGATIVE_TYPES[n],ITERATION_TYPES[i],VECTOR_SIZES[v],NEGATIVE_TYPES[n],ITERATION_TYPES[i]);
  //       printf("%s\n", s);
  //       // char *s;
  //       // sprintf(s, "./word2vec_csv -train %s/dataparsed/%s.csv -output %s/vectors/%s_v%d_n%d_i%d_csv.txt -size %d -sample 1e-3 -negative %d -hs 0 -binary 0 -cbow 1 -iter %d", train_folder,train_file,train_folder,train_file,VECTOR_SIZES[v],NEGATIVE_TYPES[n],ITERATION_TYPES[i],VECTOR_SIZES[v],NEGATIVE_TYPES[n],ITERATION_TYPES[i]);
  //       // printf("%s\n", s);
  //     }
  //   }
    // printf("%d\n", ITERATION_TYPES[v]);
  }
  for (int v=0;v<num_threads;v+= 1) {
    pthread_t tid;
    printf("Before Thread\n");
    pthread_create(&tid, NULL, runThread,(void*)v);
    pthread_join(tid, NULL);
    printf("After Thread\n");
    // system("echo 'heelo';");
  }
  exit(0);
}

char * readline(FILE *fp, char *buffer)
{
    int ch;
    int i = 0;
    size_t buff_len = 0;

    buffer = malloc(buff_len + 1);
    if (!buffer) return NULL;  // Out of memory

    while ((ch = fgetc(fp)) != '\n' && ch != EOF)
    {
        buff_len++;
        void *tmp = realloc(buffer, buff_len + 1);
        if (tmp == NULL)
        {
            free(buffer);
            return NULL; // Out of memory
        }
        buffer = tmp;

        buffer[i] = (char) ch;
        i++;
    }
    buffer[i] = '\0';

    // Detect end
    if (ch == EOF && (i == 0 || ferror(fp)))
    {
        free(buffer);
        return NULL;
    }
    return buffer;
}
