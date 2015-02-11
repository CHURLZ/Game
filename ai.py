import pygame, math


class ai:
	LEFT = "left"
	RIGHT = "right"
	UP = "up"
	DOWN = "down"

	@staticmethod
	def calculatePath(objA, x, y):
		openList = set()
		closedList = set()
		path = set()

		current = objA.currentTile
		return restructurePath()
	
	@staticmethod
	def restructurePath():
		return path
	
	@staticmethod
	def getHeuristic(goal, tile):
		return 10 * (abs(tile.rect.x - goal.rect.x) + abs(tile.rect.y - goal.rect.y))

	@staticmethod
	def getAdjacant(current, side):
		if side == LEFT:
			return Collision.getTileAt(current.rect.x - 2, current.rect.y)		
		elif side == RIGHT:
			return Collision.getTileAt(current.rect.x + current.rect.width + 2, current.rect.y)	
		elif side == UP:
			return Collision.getTileAt(current.rect.x, current.rect.y - 2)	
		elif side == DOWN:
			return Collision.getTileAt(current.rect.x, current.rect.y + current.height + 2)	
		else:
			return None