
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

        #print("init complete")
        self.start()

    def start(self):
        #print("hello!")
        #instantiate our page table
        for i in range(self.pageNum):
            self.pageTable.append(".")

        #int array for now, will change to job object later
        for i in range(self.jobNo):
            self.queueJob(i+1)

        print("Simulator Parameters:")
        print("    Memory Size:{0}".format(self.memSize))
        print("    Page Size:{0}".format(self.pageSize))
        print("    Number of Jobs:{0}".format(self.jobNo))
        print("    Runtime (min/max):{0}-{1}".format(self.minRuntime, self.maxRuntime))
        print("    Memory (min/max):{0}-{1}".format(self.minMem, self.maxMem))

        self.scheduleProcesses()

    def queueJob(self, jobId):
            mem = random.randint(self.minMem, self.maxMem)
            runtime = random.randint(self.minRuntime, self.maxRuntime)
            #print("adding job {0} to jobQueue with memory size of {1} and runtime of {2}".format(jobId, mem, runtime))
            newJob = job(jobId, mem, runtime, self.tick, self.pageSize)
            self.jobQueue.append(newJob)
            #print("job {0} has a page number of {1}".format(newJob.id, newJob.pageNum))
        
    def scheduleProcesses(self):

        self.poop()

        print("Job Queue:")
        for i in range (len(self.jobs)):
            print("    Job {0}: Runtime {1}, Memory {2}".format (self.jobs[i].id, self.jobs[i].rt, self.jobs[i].mem))

        while len(self.jobs) != 0:
            print("Time Step {0}".format(self.tick + 1))
            self.tick += 1
            job = self.jobs[self.currentJob]
            print("    Job {0} Running".format(job.id))
            job.rt -= self.timeslice
            job.end += 1
            if job.rt <= 0:
                self.removeJob(self.currentJob)

                #make up for hte lost index
                self.currentJob = self.currentJob-1
                self.poop()

            print(str(self.pageTable))

                
            if len(self.jobs) != 0:
                self.currentJob = (self.currentJob + 1)%len(self.jobs)

           
        print("Job Informatoin:")
        for i in range (len(self.completedJobs)):
            print("    Job {0}: Start Time {1}, End Time {2}".format (self.completedJobs[i].id, self.completedJobs[i].start, self.completedJobs[i].end))     
        
    def poop(self):
        if len(self.jobQueue) == 0:
            return
        tempQueue = self.jobQueue[:]
        differential = 0
        for i in range(len(self.jobQueue)):
            #print("i = {0}".format(i))
            #print(self.jobQueue[i].id)
            job = self.jobQueue[i]

            print("    Job {0} Starting".format(job.id))
    
            address = self.findPageCluster(job.pageNum)
            if address != -1:
                differential += 1
                #print("found a page cluster for job {0} at location {1}".format(job.id, address))
                self.jobs.append(job)
                job.start = self.tick
                for j in range (int(job.pageNum)):
                    self.pageTable[j + address] = job.id
                tempQueue.pop(i - differential)  

        self.jobQueue = tempQueue[:] 
        '''
        if len(self.jobQueue) == 0:
            print("Hurray!") 
        '''


    def removeJob(self, jobIndex):
        job = self.jobs.pop(jobIndex)
        print("Job {0} complete".format(job.id))
        self.completedJobs.append(job)
        job.end = self.tick
        for i in range(self.pageNum):
            page = self.pageTable[i]
            if page == job.id:
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
