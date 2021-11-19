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

# The algorithm
***  ***

# UML
![UML](/UML.jpeg)


## Taking care of the recources
In this project, unlike the previous one, we had to read .json and .csv files for the building objects and the list of calls accordingly proccess it in order to create building, elevator and call objects.
We had to create our own output recources as well this time, after the algorithm is done, it will create new .csv file as it's output.

# Getting started

## Clone the repositorty
Enter your IDE and clone the repository:
```java
https://github.com/SassonNir/OOP-Ex1.git
```

## Prerequisites
Enter the terminal in your IDE and install the next commands in order to install the required modules:
# Usage
This algorithm can be used to make an optimal call allocations, follow the and see how the algorithm evolve with every generation and the waiting time improve with every generation.

# Achnowledgement
These recourses helped us along the way while we thought or write the algorithm:

1. 
<cite>https://www.sciencedirect.com/science/article/abs/pii/S1568494604000286?via%3Dihub</cite>

2.
<cite></cite>