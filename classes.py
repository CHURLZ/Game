import random, threading, Queue
import pygame, math
import os
import images
from sprites import *
from collision import *
from ai import AI
from God import *

TILE_SIZE = 30
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
	def __init__(self, x, y, width, height, image, layer):
		pygame.sprite.Sprite.__init__(self)

		if layer == BaseClass.BACKGROUND:
			BaseClass.backgroundSprites.add(self)
		if layer == BaseClass.FOREGROUND:
			BaseClass.foregroundSprites.add(self)

		self.image = image
		self.default_image = self.image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.gridX = x
		self.gridY = y
		self.width = width
		self.height = height
		self.walkX = x + (width / 2)
		self.walkY = y + height 
		self.centerX = self.walkX
		self.centerY = self.rect.y + (height / 2)

	def motion(self, x, y):
		self.rect.x = self.gridX + x
		self.rect.y = self.gridY + y

		self.walkX = self.rect.x + (self.width/2)
		self.walkY = self.rect.y + self.height
		self.centerX = self.walkX
		self.centerY = self.rect.y + (self.height / 2)

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
	DRIVING = 0
	ARRIVED = 1
	LOADING = 2
	UNLOADING = 3
	WAITING = 4
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.FOREGROUND)
		Truck.List.add(self)
		self.state = Truck.DRIVING
		self.targetSet = True
		self.targetX = 200
		self.xDir = 1
		self.xSpeed, self.ySpeed, self.acceleration = 0, 0, 0
		self.movementSpeed, self.maxSpeed = 2, 5

	def motion(self, x, y):
		self.rect.x = self.gridX + x + self.xSpeed
		self.rect.y = self.gridY + y + self.ySpeed

		self.xSpeed += self.acceleration
		self.xSpeed *= .9
		if abs(self.xSpeed) > self.maxSpeed:
			self.xSpeed = self.maxSpeed * self.xDir

		# tX = self.targetX + x
		# self.targetX = tX

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
			targetXReached = True
		elif self.walkX > self.targetX:
			self.acceleration = -self.movementSpeed
		else:
			targetXReached = True
			self.acceleration = 0

		if targetXReached:
			self.state = Truck.UNLOADING
			self.xSpeed = 0
			self.targetSet = False

class Customer(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.FOREGROUND)
		Customer.List.add(self)
		#MOTION
		self.xSpeed, self.ySpeed = 0, 0
		self.movementSpeed, self.xDir, self.yDir = 3, 1, 1

		#INTERACTION
		self.targetX, self.targetY = 0, 0
		self.isHolding = False
		self.holdingObject = None

		#PATHFINDING
		self.targetSet = False
		self.targetTile = None
		self.currentTile = self.getCurrentTile()
		self.nextTile = None
		self.path = Queue.Queue()

		#ANIMATION
		self.STANDING = 0
		self.WALKING = 1
		self.state = self.STANDING

		img = sprite.getSpriteSheet(images.employee_1, (0,0,30,30), 3)
		self.sprite_front = img[0]
		self.sprite_side = img[1]
		self.sprite_back = img[2]
		


	def getNextTile(self):
		(x, y) = self.path.pop()

		for obj in Terrain.List:
			if obj.gridPos == (x, y):
				if obj.walkable == False or obj == None:
					self.targetSet = False
					return None
				return obj

	def getCurrentTile(self):
		for obj in Terrain.List:
			if Collision.contains(obj, self.rect.x + self.width, self.rect.y + self.height):
				return obj

	def setTarget(self, obj, grid):
		if not obj or not obj.walkable:
			return
		else:
			self.targetTile = obj

			self.targetSet = True
			self.path = self.getPath(self.targetTile, grid)
			if self.path == None:
				self.targetSet = False
				return 

			for p in self.path:
				for obj in Terrain.List:
					if obj.gridPos == p:
						obj.image = images.path

			self.nextTile = self.getNextTile()

	def motion(self, x, y):
		self.gridX += self.xSpeed
		self.gridY += self.ySpeed

		self.rect.x = self.gridX + x
		self.rect.y = self.gridY + y

	def animate(self, state):	
		img = "img/customer/customer_1_front.png"

		if state == self.WALKING:
			img = self.sprite_side
			if self.yDir == -1:
				img = self.sprite_back
			self.image = img
			if self.xDir == 1:
				self.image = pygame.transform.flip(self.image, True, False)

		elif state == self.STANDING:
			img = self.sprite_front

			if self.yDir == -1 :
				img = self.sprite_back
			self.image = img

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
		if self.currentTile == None:
			print "~error: Current tile is none"
			return

		start = self.currentTile.gridPos
		goal = goalTile.gridPos

		parents, cost = AI.calculatePath(grid, start, goal)

		return AI.reconstructPath(parents, start, goal)

	def navigate(self):
		self.state = self.WALKING
		targetXReached, targetYReached = False, False

		if self.rect.x < self.nextTile.rect.x:
			self.xSpeed = self.movementSpeed
		elif self.rect.x > self.nextTile.rect.x:
			self.xSpeed = -self.movementSpeed
		else:
			targetXReached = True
			self.xSpeed = 0

		if self.rect.y < self.nextTile.rect.y - self.width / 2:
			self.ySpeed = self.movementSpeed
		elif self.rect.y > self.nextTile.rect.y - self.width / 2:
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
	zones = []
	def __init__(self, x, y, gridPos, width, height, image_string, walkable, buildable = True, palette=None):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.BACKGROUND)
		Terrain.List.add(self)
		self.gridPos = gridPos
		self.walkable = walkable
		self.buildable = buildable

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
	def __init__(self, x, y, gridPos):
		width = 30
		height = 30

		# RGB values are in reverse order, so (Blue, Green, Red)
		palette = [hexToBGR(0x8EAEE0), hexToBGR(0x5D7394), hexToBGR(0x5D7394), hexToBGR(0x354154)]

		Terrain.__init__(self, x, y, gridPos, width, height, images.grayScaleFloor, True, True, palette)

