import random, threading, Queue
import pygame, math
import os
from collision import *
from ai import AI

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
		self.walkX = x + (width / 2)
		self.walkY = y + height 
		self.centerX = self.walkX
		self.centerY = self.rect.y + (height / 2)

class Employee(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.FOREGROUND)
		Employee.List.add(self)

class Box(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.BACKGROUND)
		Box.List.add(self)
		self.currentTile = self.getCurrentTile()
		self.currentTile.walkable = False

	def getCurrentTile(self):
		for obj in Terrain.List:
			if Collision.contains(obj, self.centerX, self.centerY):
				return obj

class Truck(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.FOREGROUND)
		Truck.List.add(self)
		self.DRIVING = 0
		self.ARRIVED = 1
		self.LOADING = 2
		self.UNLOADING = 3
		self.WAITING = 4
		self.state = self.DRIVING

		self.targetSet = True
		self.targetX = 200
		self.xDir = 1
		self.xSpeed, self.ySpeed, self.acceleration = 0, 0, 0
		self.movementSpeed, self.maxSpeed = 2, 5

	def motion(self):
		self.xSpeed += self.acceleration
		self.xSpeed *= .9
		if abs(self.xSpeed) > self.maxSpeed:
			self.xSpeed = self.maxSpeed * self.xDir

		self.rect.x += self.xSpeed
		self.rect.y += self.ySpeed

		self.walkX = self.rect.x + (self.width/2)
		self.walkY = self.rect.y + self.height

	def update(self):
		if(self.targetSet):
			self.navigate()

		if self.xSpeed < 0:
			self.xDir = -1
		elif self.xSpeed > 0:
			self.xDir = 1
		else:
			self.xDir = 0

	def navigate(self):
		targetXReached = False
		self.state = self.DRIVING
		if self.walkX < self.targetX:
			self.acceleration = 0
		elif self.walkX > self.targetX:
			self.acceleration = -self.movementSpeed
		else:
			targetXReached = True
			self.acceleration = 0

		if targetXReached:
			self.state = self.ARRIVED
			self.targetSet = False

class Customer(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.FOREGROUND)
		#MOTION
		self.xSpeed, self.ySpeed = 0, 0
		self.movementSpeed, self.xDir, self.yDir = 3, 1, 1

		#INTERACTION
		self.targetX, self.targetY = 0, 0
		self.targetSet = False
		self.isHolding = False
		self.holdingObject = None

		#PATHFINDING
		self.targetTile = None
		self.currentTile = self.getCurrentTile()
		self.nextTile = None
		self.path = Queue.Queue()

		#ANIMATION
		self.STANDING = 0
		self.WALKING = 1
		self.state = self.STANDING
		
		Customer.List.add(self)

	def getNextTile(self):
		(nextDestx, nextDesty) = self.path.pop()

		for obj in Terrain.List:
			if obj.rect.x == nextDestx * 30 and obj.rect.y == (nextDesty * 30):
				if obj.walkable == False:
					self.targetSet = False
					return None
				return obj

	def getCurrentTile(self):
		for obj in Terrain.List:
			if Collision.contains(obj, self.walkX, self.walkY):
				return obj

	def setTarget(self, x, y):
		self.targetX = x
		self.targetY = y
		self.targetSet = True

	def setTarget(self, obj, grid):
		self.targetTile = obj
		self.targetX = obj.rect.x # for later
		self.targetY = obj.rect.y # for later

		if obj.walkable == False:
			return

		self.targetSet = True
		self.path = self.getPath(self.targetTile, grid)
		if self.path == None:
			self.targetSet = False
			return 

		# path.reverse()
		# for tile in path:
		# 	self.path.put(tile)

		self.nextTile = self.getNextTile()

	def motion(self):
		if (self.xSpeed + self.ySpeed) > self.movementSpeed:
			self.xSpeed = self.movementSpeed /2
			self.ySpeed = self.movementSpeed /2

		self.rect.x += self.xSpeed
		self.rect.y += self.ySpeed

		self.walkX = self.rect.x + (self.width/2)
		self.walkY = self.rect.y + self.height

	def animate(self, state):	
		fileName = "img/customer/customer_1_front.png"

		if state == self.WALKING:
			fileName = "img/customer/customer_1_side.png"
			if self.yDir == -1:
				fileName = "img/customer/customer_1_back.png"
			self.image = pygame.image.load(fileName)
			if self.xDir == 1:
				self.image = pygame.transform.flip(self.image, True, False)

		elif state == self.STANDING:
			fileName = "img/customer/customer_1_front.png"
			if self.yDir == -1 :
				fileName = "img/customer/customer_1_back.png"	
			self.image = pygame.image.load(fileName)

	def update(self):
		self.animate(self.state)
		if(self.targetSet):
			self.navigate()

		if self.xSpeed < 0:
			self.xDir = -1
		elif self.xSpeed > 0:
			self.xDir = 1
		else:
			self.xDir = 0

		if self.ySpeed < 0:
			self.yDir = -1
		elif self.ySpeed > 0:
			self.yDir = 1
		else:
			self.yDir = 0

	def getPath(self, goalTile, grid):
		self.currentTile = self.getCurrentTile()
		start = (self.currentTile.rect.x / 30, self.currentTile.rect.y / 30)
		goal = (goalTile.rect.x / 30, goalTile.rect.y / 30)
		#hardcoded val 30 to variable PLIIIIZ
		parents, cost = AI.calculatePath(grid, start, goal)

		return AI.reconstructPath(parents, start, goal)

	def navigate(self):
		self.state = self.WALKING
		targetXReached, targetYReached = False, False
		if self.walkX < self.nextTile.rect.x+(self.nextTile.width/2):
			self.xSpeed = self.movementSpeed
		elif self.walkX > self.nextTile.rect.x+(self.nextTile.width/2):
			self.xSpeed = -self.movementSpeed
		else:
			targetXReached = True
			self.xSpeed = 0

		if self.walkY < self.nextTile.rect.y+(self.nextTile.height/2):
			self.ySpeed = self.movementSpeed
		elif self.walkY > self.nextTile.rect.y+(self.nextTile.height/2):
			self.ySpeed = -self.movementSpeed
		else:
			targetYReached = True
			self.ySpeed = 0

		if targetXReached and targetYReached:
			if self.path:
				self.nextTile = self.getNextTile()
			else:
				self.state = self.STANDING
				self.targetSet = False

class Terrain(BaseClass):
	List = pygame.sprite.Group()

	def __init__(self, x, y, width, height, image_string, walkable, palette=None):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.BACKGROUND)
		Terrain.List.add(self)
		self.default_image = image_string
		self.walkable = walkable
		self.default_palette = palette

		if palette:
			self.drawPalette(palette, width, height)

	def drawPalette(self, palette, width, height):
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
		image_string = os.path.join("img/floor/", "GrayScaleFloor.png")
		# RGB values are in reverse order, so (Blue, Green, Red)
		palette = [hexToBGR(0x8EAEE0), hexToBGR(0x5D7394), hexToBGR(0x5D7394), hexToBGR(0x354154)]

		Terrain.__init__(self, x, y, width, height, image_string, True, palette)

