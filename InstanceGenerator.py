import random

class Operation:
    def __init__(self,id,time):
        self.id = id
        self.time = time

class Maintenance:
    def __init__(self, startTime, time):
        self.startTime = startTime
        self.time = time

def generator(n):
    minTime = 10 #minimum time set for each task
    maxTime = 70 #maximum
    instance = list()

    for i in range(n):
        instance.append(Operation(i,random.randint(minTime,maxTime)))

    return instance

def maintenanceGenerator(n,sum):
    minTime = 10 #minimum time set for each maintenance
    maxTime = 50 #maximum
    k = n * 0.2 #number of maintenances, equal to 20% of the number of tasks
    maint = list()
    for i in range(int(k)):
        maint.append(Maintenance(random.randint(0,sum),random.randint(minTime,maxTime)))
    return maint;

def sumTimes(m):
    sum = 0
    for task in m:
        sum = sum + int(task.time)
    return sum

def save(n,m1,m2,maint,instanceNumber):
    f = open('inst'+str(instanceNumber)+'.txt','w')
    f.write("***{}***\n".format(instanceNumber))
    f.write(str(n) + '\n')
    for i in range(n):
        f.write("{};{};1;2\n".format(m1[i].time,str(m2[i].time)))
    for j in range(len(maint)):
        f.write(str(j)+';1;'+str(maint[j].startTime)+';'+str(maint[j].time)+'\n')
    f.write("*** EOF ***")
    f.close

def generateNewInstance(n,x):
    #number of operations for each machine, use values divisible by 5!
    m1 = generator(n) #first machine
    m2 = generator(n) #second machine
    maint= maintenanceGenerator(n, sumTimes(m1))
    maint.sort(key = lambda Maintenance: Maintenance.startTime)
    #printMachines(m1,m2,n,maint)
    save(n,m1,m2,maint,x)


instanceNumber = 1
numberOfTasks = 50
generateNewInstance(numberOfTasks,instanceNumber) 
