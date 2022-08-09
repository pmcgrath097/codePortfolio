#Collatz Conjecture implemented using child processes

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char *argv[])
{
    int n;
    printf("Enter a positive integer for the Collatz Conjecture: ");
    scanf("%d", &n);
    while(n < 0)
    {
        printf("Please enter a positive integer\n");
        scanf("%d", &n);
    }

    int pid;
    pid = fork();

    if(pid < 0)
    {
        fprintf(stderr, "fork failed\n");
        exit(1);
    }
    else if(pid == 0)
    {
        printf("%d, ", n);
        while(n != 1)
        {
            if(n %2 == 0)
            {
                n = n/2;
                printf("%d, ", n);
            }
            else
            {
                n = (n * 3) + 1;
                printf("%d, ", n);
            }
        }
    }
    else
    {
        int wc = wait(NULL);
        printf("Sequence Complete.\n");
    }

    return 0;
}