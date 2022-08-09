#include <stdio.h> 
#include <pthread.h> 
#include <semaphore.h> 
#include <unistd.h> 
#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */

sem_t *s; 		//a semaphore s

//function prototype
void* threadFunction(void* param); 

int main() 
{ 
	char *name = "my_semaphore";
	int VALUE = 1;
	//initialize semaphore to 1
	s = sem_open(name, O_CREAT, 0666, VALUE);	//if the semaphore has not been already created, create
	
	pthread_t t0,t1; 
	
	int tnumber = 0;
	
	pthread_create(&t0,NULL,threadFunction,&tnumber); 
	sleep(2);
	
	tnumber++;
	pthread_create(&t1,NULL,threadFunction,&tnumber); 
	
	pthread_join(t0,NULL); 
	pthread_join(t1,NULL); 
	
	sem_close(s);
    sem_unlink(name);
	
	return 0; 
} 

void* threadFunction(void* param) 
{ 
	int tnum;
	tnum = *((int *)param);
	
	
	sem_wait(s); 			//can I access my critical section? (semWait())
	
	//critical section 
	printf("\nThread %d has enetered its CS..\n", tnum); 
	printf("\nThread %d is executing in its CS..\n", tnum);
	
	sleep(4); 
	
	printf("\nThread %d is leaving its CS..\n", tnum);
	
	sem_post(s); 		//signal that the thread is leaving and the CS is free (semSignal())
	
	pthread_exit(0);
}