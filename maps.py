from classes import Terrain, BlueFloor
import pygame

TILE_SIZE = 30

def loadMap(matrix):
	fileName = 'map/newMap.txt'
	print "# Loading map from file:",fileName
	file = open(fileName, 'r')
	for i, line in enumerate(file):
		List = line.split()
		for j, letter in enumerate(List):
			if i < len(matrix) and j < len(matrix[0]):
				matrix[i][j] = int(letter)
	file.close()
	print "# Map loaded."

	return matrix

def createMap(matrix):
	print len(matrix)
	print len(matrix[0])
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if i == 0 or i == len(matrix) - 1 or j == 0 or j == len(matrix[i]) - 1:
				matrix[i][j] = 3
			else:
				matrix[i][j] = 1

	return matrix

def generateMap(matrix):
	for i, line in enumerate(matrix):
		for j, item in enumerate(matrix[i]):
			if(matrix[i][j] == 1):
				t = BlueFloor((j * TILE_SIZE), i * TILE_SIZE)
				# t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BlueFloor.png", True)
			if(matrix[i][j] == 2):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallVertical.png", False)
			if(matrix[i][j] == 3):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallHorizontal.png", False)
			if(matrix[i][j] == 4):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallTopLeftCorner.png", False)
			if(matrix[i][j] == 5):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallTopRightCorner.png", False)
			if(matrix[i][j] == 6):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallHorizontalBottomLeftCorner.png", False)
			if(matrix[i][j] == 7):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallHorizontalBottomRightCorner.png", False)
			if(matrix[i][j] == 8):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallHorizontalLeftEnd.png", False)
			if(matrix[i][j] == 9):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallHorizontalRightEnd.png", False)
			if(matrix[i][j] == 10):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallVerticalTopEnd.png", False)
			if(matrix[i][j] == 11):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallVerticalBottomEnd.png", False)
			if(matrix[i][j] == 12):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallIntersect.png", False)
			if(matrix[i][j] == 13):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/WoodenDoors.png", True)
			if(matrix[i][j] == 14):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallTopConnection.png", False)
			if(matrix[i][j] == 15):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/BrickWallBottomConnection.png", False)


class Grid(object):
	def __init__(self, matrix):
		self.width = len(matrix[0]) - matrix[0].count(0)
		self.height = len(matrix) - 1
		self.walls = []
		self.grid = [[0 for i in range(self.width)] for i in range(self.height)]

		for y, l in enumerate(matrix):
			for x, element in enumerate(l):
				if int(element) > 1:
					self.walls.append((x, y))

	def update(self, tiles):
		self.walls = []
		for tile in tiles:
			if not tile.walkable:
				x = tile.rect.x / 30
				y = tile.rect.y / 30

				self.walls.append((x, y))

	# def orientWalls():



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