import random, threading, Queue
import pygame, math
import os
import images
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
		self.width = width
		self.height = height
		self.walkX = x + (width / 2)
		self.walkY = y + height 
		self.centerX = self.walkX
		self.centerY = self.rect.y + (height / 2)

	def motion(self, x, y):
		dX = self.rect.x + x
		dY = self.rect.y + y

		self.rect.x = dX
		self.rect.y = dY

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

	def motion(self, x, y):
		dX = self.rect.x + x
		dY = self.rect.y + y

		self.rect.x = dX
		self.rect.y = dY

		self.xSpeed += self.acceleration
		self.xSpeed *= .9
		if abs(self.xSpeed) > self.maxSpeed:
			self.xSpeed = self.maxSpeed * self.xDir

		self.rect.x += self.xSpeed
		self.rect.y += self.ySpeed

		tX = self.targetX + x
		self.targetX = tX

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

		employee_1 = images.employee_1
		employee_1.set_clip(pygame.Rect(0, 0, 30, 30)) #Locate the sprite you want
		self.employee_front = employee_1.subsurface(employee_1.get_clip()) #Extract the sprite you want
		employee_1.set_clip(pygame.Rect(30, 0, 30, 30)) #Locate the sprite you want
		self.employee_side = employee_1.subsurface(employee_1.get_clip())
		employee_1.set_clip(pygame.Rect(60, 0, 30, 30)) #Locate the sprite you want
		self.employee_back = employee_1.subsurface(employee_1.get_clip())
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

	def motion(self, x, y):
		dX = self.rect.x + x
		dY = self.rect.y + y

		self.rect.x = dX
		self.rect.y = dY
		self.rect.x += self.xSpeed
		self.rect.y += self.ySpeed

		self.walkX = self.rect.x + (self.width/2)
		self.walkY = self.rect.y + self.height

	def animate(self, state):	
		img = "img/customer/customer_1_front.png"

		if state == self.WALKING:
			img = self.employee_side
			if self.yDir == -1:
				img = self.employee_back
			self.image = img
			if self.xDir == 1:
				self.image = pygame.transform.flip(self.image, True, False)

		elif state == self.STANDING:
			img = self.employee_front
			if self.yDir == -1 :
				img = self.employee_back
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
	FLOOR = 1
	VERTICAL = 2
	HORIZONTAL = 3
	TOP_LEFT_CORNER = 4
	TOP_RIGHT_CORNER = 5
	BOTTOM_LEFT_CORNER = 6
	BOTTOM_RIGHT_CORNER = 7
	HORIZONTAL_LEFT_END = 8
	HORIZONTAL_RIGHT_END = 9
	VERTICAL_TOP_END = 10
	VERTICAL_BOTTOM_END = 11
	INTERSECTION = 12
	TOP_CONNECTION = 14
	BOTTOM_CONNECTION = 15
	SIDEWALK = 21

	def __init__(self, x, y, width, height, image_string, walkable, buildable = True, palette=None):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.BACKGROUND)
		Terrain.List.add(self)
		self.walkable = walkable
		self.buildable = buildable
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

		Terrain.__init__(self, x, y, width, height, images.grayScaleFloor, True, True, palette)

