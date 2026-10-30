# Network Routing Simulator

A Python program that simulates a network of routers and finds the cheapest
route between any two routers using Dijkstra's algorithm, the idea behind
link-state routing protocols such as OSPF.

## Features
- Build a network of routers and links with costs
- Find the shortest route and its total cost
- Remove a link to simulate a failure and see the route change
- Add new links while the program is running

## Tools
Python, heapq (priority queue), graph data structure (dictionary)

## How to run
python routing_simulator.py

## Example
Route from A to F: A -> C -> B -> D -> E -> F (cost 13)
After removing link D-E: A -> C -> B -> D -> F (cost 14)
