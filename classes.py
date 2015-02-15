import random, threading, Queue
import pygame, math
import os
from collision import *
from ai import *

WHITE = (255, 255, 255, 255)
LIGHT_GRAY = (170, 170, 170, 255)
DARK_GRAY = (85, 85, 85, 255)
BLACK = (0, 0, 0, 255)

# Utility function to convert hex RGB codes to pygame BGR Color tuples
def hexToBGR(hex):
	red = (hex & 0xff0000) >> 16
	green = (hex & 0x00ff00) >> 8
	blue = (hex & 0x0000ff)

	return (blue, green, red)

class BaseClass(pygame.sprite.Sprite):
	foregroundSprites = pygame.sprite.OrderedUpdates()
	backgroundSprites = pygame.sprite.OrderedUpdates()
	BACKGROUND = 0;
	FOREGROUND = 1;
	def __init__(self, x, y, width, height, image_string, layer):
		pygame.sprite.Sprite.__init__(self)

		if layer == BaseClass.BACKGROUND:
			BaseClass.backgroundSprites.add(self)
		if layer == BaseClass.FOREGROUND:
			BaseClass.foregroundSprites.add(self)

		self.image = pygame.image.load(image_string)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height

class Employee(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.FOREGROUND)
		Employee.List.add(self)

class Customer(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.FOREGROUND)
		self.xSpeed, self.ySpeed = 0, 0
		self.movementSpeed, self.xDir, self.yDir = 3, 1, 1
		self.targetX, self.targetY = 0, 0
		self.targetSet = False
		self.targetTile = self.rect
		self.currentTile = self.getCurrentTile()
		self.nextTile = None
		self.path = Queue.Queue()
		Customer.List.add(self)

	def getCurrentTile(self):
		for obj in Terrain.List:
			if Collision.contains(obj, self.rect.x, self.rect.y):
				return obj

	def setTarget(self, x, y):
		self.targetX = x
		self.targetY = y
		self.targetSet = True

	def setTarget(self, obj):
		self.targetTile = obj
		self.targetX = obj.rect.x # for later
		self.targetY = obj.rect.y # for later

		self.targetSet = True
		self.path = Queue.Queue()
		path = self.getPath(self.targetTile)
		path.reverse()
		for tile in path:
			self.path.put(tile)

		self.nextTile = self.path.get()

	def motion(self):
		self.rect.x += self.xSpeed
		self.rect.y += self.ySpeed

	def animate(self, state):
		flipped = ""
		if self.xDir == 1:
			flipped ="_flipped"

	def update(self):
		self.animate(0)
		if(self.targetSet):
			self.navigate()

		if self.xSpeed < 0:
			self.xDir = -1
		elif self.xSpeed > 0:
			self.xDir = 1
		if self.ySpeed < 0:
			self.yDir = -1
		elif self.ySpeed > 0:
			self.yDir = 1

	def getPath(self, goal):
		self.currentTile = self.getCurrentTile()
		return AI.calculatePath(self.currentTile, goal, Terrain.List)

	def navigate(self):
		targetXReached, targetYReached = False, False
		if self.rect.x < self.nextTile.rect.x+(self.nextTile.width/2):
			self.xSpeed = self.movementSpeed
		elif self.rect.x > self.nextTile.rect.x+(self.nextTile.width/2):
			self.xSpeed = -self.movementSpeed
		else:
			targetXReached = True
			self.xSpeed = 0

		if self.rect.y < self.nextTile.rect.y+(self.nextTile.height/2):
			self.ySpeed = self.movementSpeed
		elif self.rect.y > self.nextTile.rect.y+(self.nextTile.height/2):
			self.ySpeed = -self.movementSpeed
		else:
			targetYReached = True
			self.ySpeed = 0

		if targetXReached and targetYReached:
			if not self.path.empty():
				self.nextTile = self.path.get()
			else:
				self.targetSet = False


class Terrain(BaseClass):
	List = pygame.sprite.Group()

	def __init__(self, x, y, width, height, image_string, walkable, palette=None):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.BACKGROUND)
		Terrain.List.add(self)
		self.default_image = image_string
		self.walkable = walkable

		if palette:
			for y in range(width):
				for x in range(height):
					if self.image.get_at((x, y)) == WHITE:
						self.image.set_at((x, y), palette[0])
					elif self.image.get_at((x, y)) == LIGHT_GRAY:
						self.image.set_at((x, y), palette[1])
					elif self.image.get_at((x, y)) == DARK_GRAY:
						self.image.set_at((x, y), palette[2])
					elif self.image.get_at((x, y)) == BLACK:
						self.image.set_at((x, y), palette[3])


class BlueFloor(Terrain):
	def __init__(self, x, y):
		width = 30
		height = 30
		image_string = os.path.join("img", "GrayScaleFloor.png")

		# RGB values are in reverse order, so (Blue, Green, Red)
		palette = [hexToBGR(0x8EAEE0), hexToBGR(0x5D7394), hexToBGR(0x5D7394), hexToBGR(0x354154)]

		Terrain.__init__(self, x, y, width, height, image_string, True, palette)

