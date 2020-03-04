
import random
import sys
import math



class job:
    def __init__(self, id, mem, rt, start, pageSize):
        self.id = id
        self.mem = mem
        self.rt = rt
        self.start = start
        self.end = 0
        self.active = False
        self.pageNum = math.ceil(self.mem/pageSize)

class RoundRobinScheduler:
    def __init__(self, memSize, pageSize, jobNo, minRuntime, maxRuntime, minMem, maxMem):

        #initialize class attributes
        self.memSize = int(memSize)
        self.pageSize = int(pageSize)
        self.jobNo = int(jobNo)
        self.minRuntime = int(minRuntime)
        self.maxRuntime = int(maxRuntime)
        self.minMem = int(minMem)
        self.maxMem = int(maxMem)

        #hardcoded attributes
        self.timeslice = 1

        #calculated attributes
        self.currentJob = 0
        self.pageNum = 0
        self.tick = 0
        self.jobs = []
        self.pageTable = []
        self.jobQueue = []
        self.completedJobs = []


        if (self.memSize/self.pageSize)%2 != 0:
            print("Error: Memory must be an even multiple of page size!")
            exit(0)

        if self.jobNo <= 0:
            print("Error: Job number must be greater than 0!")
            exit(0)

        if self.minRuntime >= self.maxRuntime:
            print("Error: Minimun run time must be less than maximum run time!")
            exit(0)

        if self.minMem >= self.maxMem:
            print("Error: Minimun memory must be less than maximum memory!")
            exit(0)

        self.pageNum = self.memSize/self.pageSize

        print("init complete")
        self.start()

    def start(self):
        print("hello!")
        #instantiate our page table
        for i in range(self.pageNum):
            self.pageTable.append(".")

        #int array for now, will change to job object later
        for i in range(self.jobNo):
            self.queueJob(i+1)

        self.scheduleProcesses()

    def queueJob(self, jobId):
            mem = random.randint(self.minMem, self.maxMem)
            runtime = random.randint(self.minRuntime, self.maxRuntime)
            print("adding job {0} to jobQueue with memory size of {1} and runtime of {2}".format(jobId, mem, runtime))
            newJob = job(jobId, mem, runtime, self.tick, self.pageSize)
            self.jobQueue.append(newJob)
            print("job {0} has a page number of {1}".format(newJob.id, newJob.pageNum))

    #Takes an index of queueJob and a page location in virtual memory
    def addJob(self, jobIndex):
        #print(jobIndex)
        #print(self.jobQueue[jobIndex])
        job = self.jobQueue[jobIndex]

        print("adding job {0} to self.jobs".format(job.id))

        address = self.findPageCluster(job.pageNum)
        if address != -1:
            self.jobs.append(job)
            for i in range (int(job.pageNum)):
                self.pageTable[i] = job.id
            return 1
        return 0
        
    def scheduleProcesses(self):
        self.poop()


        while len(self.jobs) != 0:
            job = self.jobs[self.currentJob]
            print("running timeslice for job {0}".format(job.id))
            print(str(self.pageTable))
            job.rt -= self.timeslice
            if job.rt <= 0:
                self.removeJob(self.currentJob)

                #make up for hte lost index
                self.currentJob = self.currentJob-1
                self.poop()
                
            if len(self.jobs) != 0:
                self.currentJob = (self.currentJob + 1)%len(self.jobs)
        
    def poop(self):
        if len(self.jobQueue) == 0:
            return
        tempQueue = self.jobQueue[:]
        differential = 0
        for i in range(len(self.jobQueue)):
            print("i = {0}".format(i))
            print(self.jobQueue[i].id)
            job = self.jobQueue[i]

            print("adding job {0} to self.jobs".format(job.id))
    
            address = self.findPageCluster(job.pageNum)
            if address != -1:
                differential += 1
                print("found a page cluster for job {0} at location {1}".format(job.id, address))
                self.jobs.append(job)
                for j in range (int(job.pageNum)):
                    self.pageTable[j + address] = job.id
                tempQueue.pop(i - differential)  \

        self.jobQueue = tempQueue[:]
        if len(self.jobQueue) == 0:
            print("Hurray!")


    def removeJob(self, jobId):
        job = self.jobs.pop(jobId)
        self.completedJobs.append(job)
        for i in range(self.pageNum):
            page = self.pageTable[i]
            if page == jobId:
                self.pageTable[i] = "."


    #Takes an integer pageNumber as a parameter, returns -1 if no page cluster could be found
    def findPageCluster(self, pageNumber):                  
        for i in range(len(self.pageTable)-1):                
            if self.pageTable[i] == ".":                     
                for j in range(int(pageNumber)):
                    if self.pageTable[i + j + 1] != ".":
                        i = j
                        break
                    if i + j >= pageNumber:
                        return i - 1

        return -1


print(str(sys.argv))

rr = RoundRobinScheduler(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])    
