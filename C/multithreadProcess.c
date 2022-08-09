#Multithreaded process using pthread library

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <math.h>
#include <time.h>

sem_t *s;

void* solder_worker(void* param);

int main(int argc, char* argv[])
{
    srand(time(0));

    char *name = "solder_semaphore";
    int VALUE = 3;
    s = sem_open(name, O_CREAT, 0666, VALUE);

    pthread_t workers[7];

    int tnum = 0;
    for(int i = 0; i < 7; i++)
    {
        pthread_create(&workers[i], 0, solder_worker, &tnum);
        sleep(2);
        tnum++;
    }
    for(int j = 0; j < 7; j++)
    {
        pthread_join(workers[j], NULL);
    }

    sem_close(s);
    sem_unlink(name);

    printf("All students have finished soldering.\n");

    return 0;
}

void* solder_worker(void* param)
{
    int tnum;
    tnum = *((int *)param);
    int wait_time = (rand() % (5 - 1 + 1)) + 1;

    sem_wait(s);

    printf("Student %d wants to use the soldering station.\n", tnum+1);
    printf("Student %d has begun soldering...\n", tnum+1);
    
    sleep(wait_time);

    printf("Student %d has finished soldering, cleaned their station, and is leaving the station...\n", tnum+1);

    sem_post(s);

    pthread_exit(0);
}