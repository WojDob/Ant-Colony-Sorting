import random
import math
import os

class Operation:
	def __init__(self,id,time):
		self.id = id
		self.time = time
	endTime=0

class Maintenance:
	def __init__(self, startTime, time):
		self.startTime = startTime
		self.time = time
		self.endTime = time +startTime

def sumTimes(m):
	sum = 0
	for task in m:
		sum = sum + int(task.time)
	return sum

def printMachines(n,m1,m2,maint):
	#prints a list of all of operations and maintenances and their times
	print ("machine one \t\t\t\t\t machine two")

	for i in range(n):
		print ("nr.: {}  req: {} end: {} \t\t\t nr.: {} req: {} end: {}"
		.format(m1[i].id,m1[i].time,m1[i].endTime,m2[i].id,m2[i].time,m2[i].endTime))

	print("sum of times: machine one: {} \t machine two: {}".format(sumTimes(m1),sumTimes(m2)))
	print("sums of end times : {} ".format(countEndTimes(m1,m2)))
	print("maintenances: ")
	for j in range(len(maint)):
		print("{}-{}".format(maint[j].startTime,maint[j].endTime))

def load(n,m1,m2,maint,instanceNumber):
	f =  open('inst'+str(instanceNumber)+'.txt')
	instanceNumber = f.readline()
	n = f.readline()
	n = int(n)
	count = 0
	for line in f:
		if count < n:
			number = line.split(';')
			m1.append(Operation(count,int(number[0])))
			m2.append(Operation(count,int(number[1])))
			count+=1
		else:
			if not line.startswith('***'):
				number = line.split(';')
				maint.append(Maintenance(int(number[2]),int(number[3])))
				count+=1

def getN(instanceNumber):
	f =  open('inst'+str(instanceNumber)+'.txt')
	f.readline()
	return int(f.readline())

def isInMaint(time,maint):
	for i in maint:
		if time>= i.startTime and time<=(i.startTime + i.time):
			return i
	return False

def isInBetweenInMaint(start,stop,maint):
	x = start
	y = stop
	for i in maint:
		while x!=y:
			if x>= i.startTime and x<=(i.startTime + i.time):
				return True
			x+=1
		x = start
	return False

def setEndTimes(m1,m2,maint):
	now1=0
	now2=0
	bonus = 0
	for i in m1:
		if isInBetweenInMaint(now1,math.ceil(i.time * (1-bonus)) + now1,maint):
			bonus = 0
			while isInBetweenInMaint(now1,math.ceil(i.time * (1-bonus)) + now1,maint):
				now1+=1   
		i.endTime = math.ceil(i.time * (1-bonus)) + now1
		now1 = i.endTime
		if (bonus<0.25):
			bonus+=0.05
	for j in range(len(m2)):
		while now2 < getOpById(m1,m2[j].id).endTime:
			now2+=1
		m2[j].endTime = m2[j].time + now2
		now2 =m2[j].endTime

def countEndTimes(m1,m2):
	total1=0
	total2=0
	li = list()
	for task in m1:
		total1 = total1 + task.endTime
	for task in m2:
		total2 = total2 + task.endTime
	li.append(total1)
	li.append(total2)
	return li

def ObjectiveFunction(m2):
	return m2[len(m2)-1].endTime

def getOpById(m,id):
	for op in m:
		if op.id == id:
			return op

def printMachine(m):
	for op in m:
		print(op.id, end = " ")
	print('')

#======================ACO======================#======================ACO======================#

def setPheromoneMatrix(n):
	Matrix = [[0 for x in range(n)] for y in range(n)]
	return Matrix

def showMatrix(matr,n):
	for i in range(n):
		print (matr[i])

def setMachineTwo(m1,m2):
	new = list()
	for op in m1:
		new.append(getOpById(m2, op.id))
	return new

def getSumOfRow(row,matr):
	sum = 0
	for i in range(len(matr[row])):
		sum = sum + matr[row][i]
	return sum

def getAviSumOfRow(row,matr,done):
	sum = 0
	for i in range(len(matr[row])):
		if isInDone(i,done)!= True:
			sum = sum + matr[row][i]
	return sum
def isRowChanceable(n,matr,done):
	for i in range(len(matr[n])-1):
		if matr[n][i]>0 and isInDone(i,done)==False and n!=i:
			return True
	return False

def isInDone(idboi,done):
	for i in done:
		if i.id == idboi:
			return True
	return False

def ant(m1,m2,matr,inte,shortestMachine):
	done = list()
	done.append(shortestMachine)
	curOp = shortestMachine.id

	while len(done) != len(m1):

		chance = (random.randint(1,100))

		if chance <= inte:
			if isRowChanceable(curOp,matr,done):
				key = True
				while key:
					j = random.randint(0,len(m1)-1)
					while j == curOp:
						j = random.randint(0,len(m1)-1)
					chance2 =random.randint(1,getAviSumOfRow(curOp,matr,done))
					if chance2<= matr[curOp][j] and isInDone(j,done)==False:
						done.append(getOpById(m1,j))
						curOp = j
						key=False
			else:
				randOp = m1[random.randint(0,len(m1)-1)]
				while randOp in done:
					randOp = m1[random.randint(0,len(m1)-1)]
				done.append(randOp)
				curOp = randOp.id

		else:

			randOp = m1[random.randint(0,len(m1)-1)]
			while randOp in done:
				randOp = m1[random.randint(0,len(m1)-1)]
			done.append(randOp)
			curOp = randOp.id

	return done

def pherSubstrPerc(pher, percent):
	for x in range(len(pher)):
		for y in range(len(pher)):
			pher[x][y] = round(pher[x][y] - (pher[x][y] *(percent/100)))
	return pher

def pherSubstrPoint(pher, points):
	for x in range(len(pher)):
		for y in range(len(pher)):
			if pher[x][y] - points >=0:
				pher[x][y] = pher[x][y] - points
	return pher

def pherSmooth(pher, howMuch):
	for x in range(len(pher)):
		for y in range(len(pher)):
			if x != y:
				if pher[x][y] > (getSumOfRow(x,pher)/len(pher)):
					pher[x][y] = round(pher[x][y] - ((pher[x][y] - getSumOfRow(x,pher)/len(pher))*howMuch))
				else:
					pher[x][y] = round(pher[x][y] + ((getSumOfRow(x,pher)/len(pher) - pher[x][y])*howMuch))
	return pher

def ACO(m1,m2,main,instanceNumber,randomOrderFunction):
	print("ACO working - please wait")

	interest = 0
	numberOfAnts = 40
	numberOfCycles= 75
	difOfInterest = 100/numberOfCycles # added to interest, every cycle

	smoothing= 0.1 # 0-1
	deletPerc = 7 # 0-100

	chosenAnts = 5

	pher = setPheromoneMatrix(len(m1))

	paths = list()
	pathsTwo = list()
	results = list()
	bestPaths = list()

	shortestMachine = m1[0]
	for machine in m1:
		if machine.time < shortestMachine.time:
			shortestMachine = machine

	recordTime = 9999999
	recordPath = m1

	for a in range (numberOfCycles):

		paths.clear()
		for i in range(numberOfAnts):	
			paths.append(ant(m1,m2,pher,interest,shortestMachine))

		pathsTwo.clear()
		for i in range(len(paths)):
			pathsTwo.append(setMachineTwo(paths[i],m2))

		results.clear()
		for i in range(len(paths)):
			setEndTimes(paths[i],pathsTwo[i],main)
			# printMachines(len(m1),paths[i],pathsTwo[i],main)
			results.append([ObjectiveFunction(pathsTwo[i]),i])
			results.sort()

		bestPaths.clear()
		for i in range (chosenAnts):
			bestPaths.append(paths[results[i][1]])

		for i in range(len(bestPaths)): #update the pheromone matrix
			for k in range(len(bestPaths[i])-1):
				pher[bestPaths[i][k].id][bestPaths[i][k+1].id]+=100

		if results[0][0] < recordTime:
				recordTime= results[0][0]
				recordPath= paths[results[0][1]]
				# print("new record: {}, cycle: {}, int: {}".format(recordTime,a,interest))
				for k in range(len(bestPaths[i])-1): #the best path gets  more points
					pher[bestPaths[0][k].id][bestPaths[0][k+1].id]+=20

		if interest < 100:
			interest= interest + difOfInterest

		pher = pherSubstrPerc(pher,deletPerc)

		if a % 10 == 0:
			pher = pherSmooth(pher,smoothing)
	
	print("record path:")
	p1 = recordPath
	p2 = setMachineTwo(recordPath,m2)
	setEndTimes(p1,p2,main)
	printMachines(len(m1),p1,p2,main)
	print(" \t\t\tbest result:     {}".format(recordTime))
	print()
	save(p1,p2,main,instanceNumber,randomOrderFunction,recordTime)

	return recordTime

def save(m1,m2,maint,instanceNumber,randomOrderFunction,recordTime):
	f = open('out'+str(instanceNumber)+'.txt','w')
	f.write("***{}***\n".format(instanceNumber))
	f.write("min time found: {} starting time: {}\n".format(recordTime,randomOrderFunction))
	f.write("machine one \t\t\t\t\t\t\t\t\t machine two\n")

	for i in range(len(m1)):
		f.write ("id: {}; time required: {}; op ended: {};\t\t\t id: {}; time required: {}; op ended: {};\n"
		.format(m1[i].id,m1[i].time,m1[i].endTime,m2[i].id,m2[i].time,m2[i].endTime))

	sum = 0
	for j in range(len(maint)):
		sum+= maint[j].time
	f.write("total maintenances: {} total maintenance time: {}\n".format(len(maint),sum))
	f.write("*** EOF ***")
	f.close()




instanceNumber = 1 


mOne = list()
mTwo = list()
main = list()
n = getN(instanceNumber)
load(n,mOne,mTwo,main,instanceNumber)
setEndTimes(mOne,mTwo,main)
randomOrderFunction = mTwo[len(mTwo)-1].endTime
printMachines(len(mOne),mOne,mTwo,main)
results = list()
for i in range(10):
	results.append(ACO(mOne,mTwo,main,instanceNumber,randomOrderFunction))
	print(results)
print("Average result: {}".format(sum(results)/float(len(results))))
os.system('pause')
