# Assignment 6 - Search Agents

CIS 454, AI and Advanced Python; University of Maine at Augusta, Spring 2026

## Overview 

This repository contains the files necessary to complete Assignment 6, Search.

In this assignment you will implement three graph-traversal algorithms:  BFS for 
unweighted graphs, Dijkstra's shortest-path, and informed search using A*.   

## Clone Repository

To work on the assignment you will want to clone this repository to your local 
computer.   Refer to the instructions from Assignment 1 to review the process.

## Complete the agent

You will implement the three algorithms in the search.py file.    
You will find it most effective to complete this work within the PyCharm IDE 
environment.  

## What is provided

Two datasets have been provided:
- romania.pickle is a graph of the map of romania
- kennebec.pickle is a graph of the streets of greater kennebec county.

The files are in pickle form -- pickle is a python utility which allows us to 
save & retrieve objects.  Each dataset is a Graph representation of the 
relevant map.   

## Common Code

Two additional files have been provided:

- graph.py -- the class defintion for Graph objects
- IndexMinPQ.py -- an implementation of a priority queue which supports 
dynamic updating of the value for a given key.  This will be helpful when 
  implmenting Dijkstra's & A* to main the "search frontier" queue

You should familiarize yourself with the code contained in each of these 
modules, especially the Graph class definition.

## Data Structures

For each algorithm you will need data structures to track various details 
(explored, prior, pathcost).  I recommend trying Python Dictionaries, where 
the key is the node id and the value is the data being tracked for that node.
You can also accomplish this via a Python list, using the node id as an 
index into a list.   

You will have to manage default values for these entries. For 
example, `explore[v]` will be initially False for a node. If you use a 
dictionary, take advantage of the optional  default value with the `.get
(<key>, <default value>)` method -- this allows  you to effectively handle 
the first time values are accessed.   If you use a 
list, you will have to prepopulate the list with the default values.   

## Commit & Push Your work

Once you have completed the assignment, Commit and Push your changes back to 
your repository.

## Submit to Brightspace

Your completed search.py file should be submitted to Brightspace by the 
Assignment Due Date.

## Grading Rubric

- 20 points, implement BFS
- 30 points, implement Dijkstra's shortest path
- 35 points, implement A*
- 10 points, your code is well structured & properly documented
-  5 points, your GIT repo is properly updated and matches your brightspace 
  submission

For the 3 algorithms to be considered correct:
- they must return the correct path
- the number of POPs must be within an acceptable range

For example, the first test case (find a path from 0 to 2 in romania) 
yields the following:
- BFS: 3 edges, 7 pops, path: [0, 15, 5, 1]
- Dijkstra: weight 418, 13 pops, path: [0, 15, 14, 13, 1]
- A*: weight 418, 6 pops, path: [0, 15, 14, 13, 1]

## 📚  Resources 

See Brightspace for additional reading on our search algorithms.


