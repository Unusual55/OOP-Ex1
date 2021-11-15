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

# The algorithm
***  ***

## Taking care of the recources
In this project, unlike the previous one, we had to read .json and .csv files for the building objects and the list of calls accordingly proccess it in order to create building, elevator and call objects.
We had to create our own output recources as well this time, after the algorithm is done, it will create new .csv file as it's output.

# Getting started

## Clone the repositorty
Enter your IDE and clone the repository:
```java

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