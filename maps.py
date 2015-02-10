from classes import Terrain
import pygame

TILE_SIZE = 30

def loadMap(matrix):
	print "# Loading map from file..."
	file = open('map/newMap.txt', 'r')
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
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/terrain.jpg", True)
			if(matrix[i][j] == 2):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/terrain_top.jpg", False)
			if(matrix[i][j] == 3):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/terrain_left.jpg", False)
			if(matrix[i][j] == 4):
				t = Terrain((j * TILE_SIZE), i * TILE_SIZE, TILE_SIZE, TILE_SIZE, "img/terrain_right.jpg", False)
