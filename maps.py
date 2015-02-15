from classes import Terrain, BlueFloor
import pygame

TILE_SIZE = 30

def loadMap(matrix):
	print "# Loading map from file..."
	fileName = 'map/newMap.txt'
	file = open(fileName, 'r')
	for i, line in enumerate(file):
		List = line.split()
		for j, letter in enumerate(List):
			if i < len(matrix) and j < len(matrix[0]):
				matrix[i][j] = int(letter)
	file.close()
	print "# Map loaded."
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