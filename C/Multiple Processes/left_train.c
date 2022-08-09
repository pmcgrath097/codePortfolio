#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

int main(int argc, char * argv[])
{
    int VALUE = 1;
    sem_t *right;
    sem_t *left;

    right = sem_open("right", O_CREAT, 0666, VALUE);
    left = sem_open("left", O_CREAT, 0666, VALUE);

    int tnum = 0;
    for(int t = 0; t < 5; t++)
    {
        sem_wait(right);
        printf("Train %d has crossed the left bridge.\n", tnum+1);
        sleep(1);
        tnum++;
        sem_post(right);
    }

    printf("%d trains have crossed the left bridge.\n", tnum);
    return 0;
}