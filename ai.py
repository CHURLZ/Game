
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, math, time
import pygame, math, Queue, time
from collision import *

import heapq
import collections


# Wrapper for deque class
class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

class PriorityQueue:
	def __init__(self):
		self.elements = []

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))

	def get(self):
		return heapq.heappop(self.elements)[1]

class Grid(object):
	def __init__(self, matrix):
		self.width = len(matrix[0]) - matrix[0].count(0)
		self.height = len(matrix) - 1
		self.walls = []

		for y, l in enumerate(matrix):
			for x, element in enumerate(l):
				if int(element) > 1:
					self.walls.append((x, y))

	def in_bounds(self, id):
		(x, y) = id
		return 0 <= x <= self.width and 0 <= y <= self.height
    
	def passable(self, id):
		return id not in self.walls
    
	def neighbors(self, id):
		(x, y) = id
		
		# results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
		# Allows diagonal movement
		results = [(x+1, y-1), (x+1, y), (x+1, y-1), (x, y-1), (x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1)]
		if (x + y) % 2 == 0: results.reverse() # aesthetics
		
		results = filter(self.in_bounds, results)
		results = filter(self.passable, results)

		return results

	def printPath(self, start, goal, path):
		out = [[' ' for i in range(self.width)] for i in range(self.height)]

		grid = [[0 for i in range(self.width)] for i in range(self.height)]

		for element in self.walls:
			grid[element[1]][element[0]] = 1


		for i in range(self.height):
			for j in range(self.width):
				if (j, i) == start:
					out[i][j] = 'S'
				elif (j, i) == goal:
					out[i][j] = 'G'
				elif grid[i][j] == 0:
					if (j, i) in path:
						out[i][j] = '%'
					else:
						out[i][j] = '-'
				elif grid[i][j] == 1:
					out[i][j] = '#'

		printout = [""] * self.height 
		for i in range(self.height):
			for j in range(self.width):
				printout[i] += out[i][j]
				printout[i] += " "


		for l in printout:
			print l


class GridWithWeights(Grid):
	def __init__(self, matrix):
		super(GridWithWeights, self).__init__(matrix)
		self.weights = {}

	def cost(self, a, b): 
		return self.weights.get(b, 1)



class AI:
	total = 0
	count = 0

	@staticmethod
	def calculatePath(graph, start, goal):
		startTime = time.clock() * 1000
		frontier = PriorityQueue()
		frontier.put(start, 0)

		came_from = {}
		cost_so_far = {}

		came_from[start] = None
		cost_so_far[start] = 0

		while not frontier.empty():
			current = frontier.get()

			if current == goal:
				break

			for next in graph.neighbors(current):
				new_cost = cost_so_far[current] + graph.cost(current, next)
				if next not in cost_so_far or new_cost < cost_so_far[next]:
					cost_so_far[next] = new_cost
					priority = new_cost + AI.heuristic(goal, next)
					frontier.put(next, priority)
					came_from[next] = current

		AI.total += (time.clock() * 1000) - startTime
		AI.count += 1

		print "Average time: " + str(AI.total / AI.count) + "ms"

		return came_from, cost_so_far

	@staticmethod
	def reconstructPath(came_from, start, goal):
		current = goal
		path = [current]
		while current != start:
			current = came_from[current]
			# path.append((current[0] * 30, current[1] * 30))
			path.append(current)
		return path

	@staticmethod
	def heuristic(a, b):
		(x1, y1) = a
		(x2, y2) = b

		return abs(x1 - x2) + abs(y1 - y2)
