# Ant-Colony-Sorting

This script uses a metaheuristic algorithm - Ant Colony Optimization - to solve a complex flow shop scheduling problem. It's old and the code is chaotic, if I were writing it now, I would make it more readable, efficient and documented.

The InstanceGenerator.py generates random instances of the tasks, which are then stored in a text file used by Sorter.py, where the actual ACO algorithm is used.

# How to use
First, run InstanceGenerator.py to generate a random instance of the problem. The generator takes into account the number of tasks that each machine will have to process, and also generate a number of "maintenance tasks" - periods of times during which no task can be done. You can change these paramateres by altering the variables in the script.

Next, run Sorter.py. This is where the Ant Colony Sorting algorithm learns the best way to sort the tasks to minimize the time it takes to finish all the tasks on both machines. Depending on the size of the instance generated and the amount of ants set for every circle, this could take a while.

# Example
For this example we have generated a small instance of the problem - 20 tasks with 4 maintenance periods:

![Screenshot before](https://i.imgur.com/KReRVjb.png)

All tasks have different set parameters:
* **nr**: the number of the task - this is important because on machine two before a task can be started the task with the same number has to be completed on machine one
* **req**: the time required to finish the task
* **end**: the time at which this task end during the current iteration of the algorithm - this changes during the course of the algorithm.


After running the ACO algorithm we have found the following order of tasks:

![Screenshot after](https://i.imgur.com/KReRVjb.png)

As you can see, the order of the tasks has changed, as well as the end times of the tasks. The end time of the last task on machine two tell us the total time it takes to finish all tasks - in this instance the ACO managed to shorten the total time from **1063** to **893**.
