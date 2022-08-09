#Banker's Algorithm Simulation

import numpy

NUMBER_OF_PROCESSES = 5
NUMBER_OF_RESOURCES = 4

available = [0]*NUMBER_OF_RESOURCES
claim = [[0]*NUMBER_OF_RESOURCES]*NUMBER_OF_PROCESSES
allocation = [[0]*NUMBER_OF_RESOURCES]*NUMBER_OF_PROCESSES
need = [[0]*NUMBER_OF_RESOURCES]*NUMBER_OF_PROCESSES
sequence = []

def setInputs():
    global available
    global claim
    global allocation
    global need
    f = open("inp3.txt", "r")
    lines = f.readlines()
    lines = [e for e in lines if e not in ('\n')]
    
    temp = 0
    for i in range(len(lines)):
        if(i < 5):
            claim[i] = lines[i].split()
        elif(i < 10):
            allocation[temp] = lines[i].split()
            temp += 1
        elif(i == 10):
            available = lines[i].split()


    f.close()
    for j in range(NUMBER_OF_PROCESSES):
        for k in range(NUMBER_OF_RESOURCES):
            claim[j][k] = int(claim[j][k])
            allocation[j][k] = int(allocation[j][k])
    
    for x in range(NUMBER_OF_RESOURCES):
        available[x] = int(available[x])
    
    arr1 = numpy.array(claim)
    arr2 = numpy.array(allocation)
    need = numpy.subtract(arr1, arr2)
    need = need.tolist()

    return 0

def bankers():
    global available
    global claim
    global allocation
    global need
    global sequence
    procsRun = []
    cantRun = []
    print("Available: ")
    print(available)
    while len(sequence) != 5:
        temp = 0
        for i in range(NUMBER_OF_PROCESSES):
            for j in range(NUMBER_OF_RESOURCES):
                if need[i][j] <= available[j]:
                    temp += 1
            if temp == 4 and i not in procsRun:
                sequence.append("P" + str(i))
                procsRun.append(i)
                cantRun.clear()
                print("P" + str(i) + " Runs: ")
                print(allocation[i])
                for k in range(NUMBER_OF_RESOURCES):
                    available[k] += allocation[i][k]
                print("Available: ")
                print(available)
            elif i not in cantRun and i not in procsRun:
                cantRun.append(i)
            temp = 0
        if (len(procsRun) + len(cantRun) == 5):
            break
    if len(procsRun) == 5:
        print("The initial state is a safe state. Possible safe sequence: ")
        print(sequence)
    else:
        print("The initial state is not safe.")

    return 0

def main():
    global available
    global claim
    global allocation
    global need

    setInputs()
    print("Claim Matrix: ")
    for i in range(NUMBER_OF_PROCESSES):
        print(claim[i])
    print("---------------------------------------")
    print("Allocation Matrix: ")
    for j in range(NUMBER_OF_PROCESSES):
        print(allocation[j])
    print("---------------------------------------")
    print("C-A Matrix: ")
    for k in range(NUMBER_OF_PROCESSES):
        print(need[k])
    print("---------------------------------------")
    bankers()
    return 0

if __name__ == "__main__":
    main()