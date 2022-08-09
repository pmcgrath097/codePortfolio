#Interrupt Driven Scheduling Simulation

class process:
    def __init__(self, pid, state):
        self.pid = pid
        self.state = state
        self.waitTime = 0

processes = [] # list of processes retrieved from the input file
initLines = [] # list containing each line of the original input file to use for output formatting
keywords = ["requests", "dispatched", "expires", "interrupt", "terminated", "disk", "keyboard", "printer"] # keywords used to simplify the input file
diskQ = []
printerQ = []
keyboardQ = []
numBlocked = 0
percentBlocked = 0.0
threshold = 0.0
numSwap = 1
latency = 0

def parseInput(file, result): # function to parse an input file and create a simplified version of the original
    f = open(file, "r")
    r = open(result, "w")
    global initLines
    initLines = f.readlines()
    r.write(initLines[0]) # copy the first line of the original file to the new one

    i = 1
    while i < len(initLines):
        newLine = initLines[i].replace(":", "") # remove punctiation marks from the current line
        newLine = newLine.replace(";", "")
        newLine = newLine.replace(".", "")
        temp = newLine.split()
        str = []
        for s in temp:
            if "P" in s or s in keywords: # put each element that is a keyword or PID in the list str
                str.append(s)
        if "interrupt" in str:
            tempIndex = str.index("interrupt") # swap the order of the PID and interrupt keyword if that keyword is in the list
            str[tempIndex] = str[tempIndex + 1]
            str[tempIndex + 1] = "interrupt"
        parsedLine = " ".join(str) # join the list into one string seperaating the elements with a blank space
        r.write(parsedLine + "\n") # write the new line to the new file
        i += 1
    f.close()
    r.close()

def findProcess(pid): # function to find a process in the list based on PID and return its index
    index = -1

    for p in processes:
        if p.pid == pid:
            index = processes.index(p)

    return index

def executeLine(temp, line):
    global latency
    global numBlocked
    global percentBlocked
    k = 0
    while(k < len(temp)):
        if "P" in temp[k]: # this conditional checks that the current element is a PID and will update the associated process according to the keyword(s) that follows
            index = findProcess(temp[k])
            if temp[k+1] == "terminated":
                processes[index].state = "Exit"
                for i in range(numSwap):
                    for j in range(len(processes)):
                        if processes[j].state == "Blocked*":
                            processes[j].state = "Blocked"
                            numBlocked += 1
                            latency += 1
                            break
                        elif processes[j].state == "Ready*":
                            processes[j].state = "Ready"
                            latency += 1
                            break
            elif temp[k+1] == "requests":
                processes[index].state = "Blocked"
                numBlocked += 1
                if temp[k+2] == "disk":
                        diskQ.append(processes[index])
                elif temp[k+2] == "printer":
                    printerQ.append(processes[index])
                elif temp[k+2] == "keyboard":
                    keyboardQ.append(processes[index])
                processes[index].waitTime = line
            elif temp[k+1] == "dispatched":
                processes[index].state = "Running"
            elif temp[k+1] == "expires":
                processes[index].state = "Ready"
            elif temp[k+1] == "interrupt":
                if processes[index].state == "Blocked*":
                    processes[index].state = "Ready*"
                    if processes[index] in diskQ:
                        diskQ.remove(processes[index])
                    elif processes[index] in printerQ:
                        printerQ.remove(processes[index])
                    elif processes[index] in keyboardQ:
                        keyboardQ.remove(processes[index])
                elif processes[index].state == "Blocked":
                    processes[index].state = "Ready"
                    numBlocked -= 1
                    if processes[index] in diskQ:
                        diskQ.remove(processes[index])
                    elif processes[index] in printerQ:
                        printerQ.remove(processes[index])
                    elif processes[index] in keyboardQ:
                        keyboardQ.remove(processes[index])
            percentBlocked = (numBlocked / len(processes)) * 100
        k += 1
    return 0

def main():
    global threshold
    global numSwap
    global latency
    global numBlocked
    print("Enter file name of the input file:")
    inputName = input()
    print("Enter the name of the new file created from the input file:")
    resultFile = input()
    print("Enter the desired threshold for the percentage of blocked processes: (80%, 90%, or 100%)")
    threshold = float(input())
    print("Enter the number of processes to be swapped in or out at one time: (1 or 2)")
    numSwap = int(input())
    parseInput(inputName, resultFile)
    inputFile = open(resultFile, "r") # open input file
    linesInFile = inputFile.readlines() # store each line into a list

    line = linesInFile[0].split() # seperate the first line by spaces
    
    i = 0
    while line[i] != "end": # while loop creates each process object and adds them to the list of processes
        if "P" in line[i]:
            processes.append(process(line[i], line[i+1]))
        i += 1
    
    j = 1
    while(j < len(linesInFile)): # this loop will go through each line of the file after the first and update the process states accordingly
        print(initLines[j].replace("\n", ""))
        print("------------------------------")
        temp = linesInFile[j].split()
        
        if percentBlocked >= threshold:
            for x in range(numSwap):
                    for y in range(len(processes)):
                        if processes[y].state == "Blocked":
                            processes[y].state = "Blocked*"
                            latency += 1
                            numBlocked -= 1
                            break
            executeLine(temp, j)
        else:
            executeLine(temp, j)

        for p in processes:
            print(p.pid + ": " + p.state)
        print("\nAdditional Latencies: " + str(latency))
        print("Percentage of Blocked Processes: " + str(percentBlocked) + "%\n")
        print("Disk Queue: ")
        if len(diskQ) != 0:
            for p in diskQ:
                print(p.pid + ", ")
        print("Printer Queue: ")
        if len(printerQ) != 0:
            for p in printerQ:
                print(p.pid + ", ")
        print("Keyboard Queue: ")
        if len(keyboardQ) != 0:
            for p in keyboardQ:
                print(p.pid + ", ")
        print("------------------------------")
        j += 1

    inputFile.close()

if __name__ == "__main__":
    main()