# OOP-Ex1
Nir Sasson and Ofri Tavor's repository for assignment number 1 in the course OOP in Ariel university 

## About the project
The Elevator scheduling optimization problem have many algorithm and solution and there isn't only one answer which will allow to solve this problem.
This project took over after last project was ended, in the last project we had to write an online algorithm which will allow us to solve the problem with optimal waiting times.
This time we had to write an offline algorithm which will allow us to allocate every call ahead of time in order to reach optimal avarage waiting time.
We understood the problem much better after writing the online algorithm, we realized the problems in our algorithm, and we used it to make this algorithm better and easier.
# The problem
The advantage in writing an offline algorithm is that we get the whole input ahead of time, while in online algorithm we recieve the data in real time.
The fact that we have the list of calls we need to allocate forces us to think of an optimal way to allocate every call while taking into account many parameter:

1. The time that will take to finish the call and which elevator could finish it faster.
2. Which allocation will cause it's elevator the minimal delay time
3. Taking into account that every change we will try to make after allocating a call could lead to chain reaction that might increase the avarage waiting time severely.

Taking into account those 3 parameters, we had to think of a way to deal with most of them the best way we can in order to create an algorithm which can lead to good results in the general case.

# Classes and objects
| Class Name |                                                                                                                                                                                                                                                                       Class Meaning                                                                                                                                                                                                                                                                       |
|------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Building   | Object that contain every detail about the building which we simulate the elevators movement on. It contains all of the elevators,  as well as other details like minimal floor and maximal floor which the elevator can't reach outside this range.                                                                                                                                                                                                                                                                                                      |
| Elevator   | Object that represent the elevator. This object contain every detail about the elevator, from it's id to it's speed and it's also contain a Route object that control the course of the elevator.                                                                                                                                                                                                                                                                                                                                                         |
| Call       | Object that represent a call which will be allocated to one of the elevators                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Node       | Object that contain some of the data of the Call object, there are 3 types of Node: 1. incoming: This type represent the event that the call was arrived and allocated, and of course it won't change it's values. 2. src: This type represent the event that the elevator reached the source floor. 3. dst: This type represent the event that the elevator reached the destenation floor. Every node represent an event that will happen on the time line of the elevator.                                                                              |
| Vector     | Data structure that contain 3 Node objects, one of each type and represent a Call object which we can use easily.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Route      | Data structure that contain list of vectors which represent the Calls it's elevator is taking care of, list of Nodes which  represent the course of the elevator as well as it's time line along the whole simulation. This Data Structure can insert every Node into the course as if it's an online algorithm, in order to simulation which will be  as close as possible to the choice of most optimal elevator in online algorithm. This feature allow us to use both offline algorithm and online algorithm to improve the results of the algorithm. |
| Controller | The controller is the brain behind the whole algorithm. The controller parse the csv file into list of Calls and using allocate  functions run the whole simulation by check for every call which elevator would be optimal for the long term.                                                                                                                                                                                                                                                                                                            |

## Connection between nodes
As we mentioned earlier there are 3 types of Nodes:

1. incoming
2. src
3. dst

And every Vector contain one of each type.

Every node contain a pointer to each of the other nodes in the vector.

The connection can help us to take into account the diffrence in calculating the delay that might be caused to the src node and the dst node based on the type of the node.
 The incoming Node is special, since it's time won't change.

For example, if we reach the source floor 10 second later than we expected, then we will reach the destenation floor 10 seconds later as well, but if we will only reach the destenation floor 10 seconds later- if the elevator already been to the source floor, we reached the source floor at the expected time, and we will reach only the destentaion floor 10 seconds later.

The Node class is taking care of that, if we want to delay the source floor arrival time, it will automatically delay the destenation floor as well, but if we want to delay only the destenation floor arrival time, we won't delay the source floor arrival time as well.

This delay factor control system help us to keep track of the delay and arrival time much easier and it solve the most delicate part of the project which is time calculations.



# The process of the algorithm
***  ***
## Pre allocation auction
We will allocate the calls backwards- The last call will be allocated first and the first call will be the last call to be allocated.
Every elevator will check how much time will be needed to finish taking care of the call, and how much it will affect the other calls that already allocated to the elevator.
## Calculations
every elevator will check where to insert the src and dst nodes, and calculate how long will it take to reach the source floor and the destenation floor.
The delay factor that will be caused to every call will be updated during the insertion of the Nodes and will be updated directly in the time property of every Node.
## Allocation
Every elevator returns the time that it will need to finish taking care of this call, as well as how much time it will take longer than expected to finish taking care of every other calls.
The elevator which returns the minimal time will be chosen and this call will be allocated to it.
## Building online course
After a call was allocated to an elevator, the system will insert it's nodes to their most suitable indexes, and update the arrival time to every Node after the source node and destenation node.
By doing that, we might ruined the order of the nodes in the course. The system will sort the nodes by their time so the order will not change and the course would still be as if it's an online 

# The algorithm
1. Loop through the call list backwards
2. Loop through the elevator list
3. Check the time needed for every elevator
4. Keep the minimal time and the id of the elevator.
5. allocate the call to the elevator
6. Insert the Vector of the call to the course of the elevator
7. Update the arrival time for every node that will be delayed because of the new call.
8. Sort the course the course by the time property of the nodes so the order will be as if it's an online algorithm course 

# UML
![UML](/UML.jpeg)


## Taking care of the recources
In this project, unlike the previous one, we had to read .json and .csv files for the building objects and the list of calls accordingly proccess it in order to create building, elevator and call objects.
We had to create our own output recources as well this time, after the algorithm is done, it will create new .csv file as it's output.

# Getting started

## Clone the repositorty
Enter your IDE and clone the repository:
```sh
git clone https://github.com/SassonNir/OOP-Ex1.git
```

## Prerequisites
Enter the terminal in your IDE and install the next commands in order to install the required modules:
```git
pip install -r requirements.txt
```

# Usage
This algorithm can be used to make an optimal call allocations, follow the and see how the algorithm evolve with every generation and the waiting time improve with every generation.

# Achnowledgement
These recourses helped us along the way while we thought or write the algorithm:

1. P. Cortés, J. Larrañeta, L. Onieva,
Genetic algorithm for controllers in elevator groups: analysis and simulation during lunchpeak traffic,
Applied Soft Computing,
Volume 4, Issue 2,
2004,
Pages 159-174,
ISSN 1568-4946,
https://doi.org/10.1016/j.asoc.2003.11.002. 
<cite>https://www.sciencedirect.com/science/article/abs/pii/S1568494604000286?via%3Dihub</cite>

2. Yerzhigit Bapin and Vasilios Zarikas, “Smart Building’s Elevator with Intelligent Control Algorithm based on Bayesian Networks” International Journal of Advanced Computer Science and Applications(ijacsa), 10(2), 2019.
<cite>http://dx.doi.org/10.14569/IJACSA.2019.0100203</cite>

3. <cite>https://www.youtube.com/watch?v=siqiJAJWUVg&t=1229s</cite>

4. <cite>https://www.youtube.com/watch?v=14Cc8IDWtFM</cite>