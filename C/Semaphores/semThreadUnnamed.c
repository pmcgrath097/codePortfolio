#include <stdio.h> 
#include <pthread.h> 
#include <semaphore.h> 
#include <unistd.h> 

sem_t s; 		//a semaphore s

//function prototype
void* threadFunction(void* param); 

int main() 
{ 
	//initialize the unnamed semaphore s using: sem_init(&s, 0, 1);
	//&s is the pointer to the semaphore
	//0 means that this semaphore is shared by threads created by this process
	//1 sets the initial value of the semaphore to 1
	sem_init(&s, 0, 1); 
	
	pthread_t t0,t1; 
	
	int tnumber = 0;
	
	pthread_create(&t0,NULL,threadFunction,&tnumber); 
	sleep(2);	//wait 2 seconds
	
	tnumber++;
	pthread_create(&t1,NULL,threadFunction,&tnumber); 
	
	pthread_join(t0,NULL); 
	pthread_join(t1,NULL); 
	
	sem_destroy(&s);
	
	return 0; 
} 

void* threadFunction(void* param) 
{ 
	int tnum;
	tnum = *((int *)param);
	
	
	sem_wait(&s); 			//can I access my critical section? (semWait())
	
	//critical section 
	printf("\nThread %d has enetered its CS..\n", tnum); 
	printf("\nThread %d is executing in its CS..\n", tnum);
	
	sleep(4); 
	
	printf("\nThread %d is leaving its CS..\n", tnum);
	
	sem_post(&s); 		//signal that the thread is leaving and the CS is free (semSignal())
	
	pthread_exit(0);
}
