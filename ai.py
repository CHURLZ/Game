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

class AI:
	total = 0
	count = 0

	@staticmethod
	def calculatePath(graph, start, goal):
		# startTime = time.clock() * 1000
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

			for next in graph.neighbors(current, True):
				new_cost = cost_so_far[current] + graph.cost(current, next)
				if next not in cost_so_far or new_cost < cost_so_far[next]:
					cost_so_far[next] = new_cost
					priority = new_cost + AI.heuristic(goal, next)
					frontier.put(next, priority)
					came_from[next] = current

		# AI.total += (time.clock() * 1000) - startTime
		# AI.count += 1

		#print "Average time: " + str(AI.total / AI.count) + "ms"

		return came_from, cost_so_far

	@staticmethod
	def reconstructPath(came_from, start, goal):
		current = goal
		path = [current]
		while current != start:
			if current not in came_from:
				return None 
			current = came_from[current]
			# path.append((current[0] * 30, current[1] * 30))
			path.append(current)
		return path

	@staticmethod
	def heuristic(a, b):
		(x1, y1) = a
		(x2, y2) = b

		return abs(x1 - x2) + abs(y1 - y2)
