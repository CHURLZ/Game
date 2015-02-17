from classes import Terrain, BlueFloor
import pygame, images

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
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickVert, False)
			if(matrix[i][j] == 3):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickHori, False)
			if(matrix[i][j] == 4):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickTopLeftCorner, False)
			if(matrix[i][j] == 5):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickTopRightCorner, False)
			if(matrix[i][j] == 6):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickBottomLeftCorner, False)
			if(matrix[i][j] == 7):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickBottomRightCorner, False)
			if(matrix[i][j] == 8):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickHorizLeftEnd, False)
			if(matrix[i][j] == 9):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickHorizRightEnd, False)
			if(matrix[i][j] == 10):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickVertTopEnd, False)
			if(matrix[i][j] == 11):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickVertBottomEnd, False)
			if(matrix[i][j] == 12):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickIntersection, False)
			if(matrix[i][j] == 13):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.woodenDoors, True)
			if(matrix[i][j] == 14):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickTopConnection, False)
			if(matrix[i][j] == 15):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.brickBottomConnection, False)
			
			if(matrix[i][j] == 16):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.roadMidLeft, False)
			if(matrix[i][j] == 17):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.roadMidMid, False)

			if(matrix[i][j] == 18):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.road, False)

			if(matrix[i][j] == 19):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.roadBottomLeft, False)

			if(matrix[i][j] == 20):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.roadTopLeft, False)
			if(matrix[i][j] == 21):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, images.sidewalk, True)

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
