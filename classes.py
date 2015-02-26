import random, threading, Queue
import pygame, math
import os
import images
from sprites import *
from collision import *
from ai import AI
from God import *
from taskManager import *
from task import *
from gui import TextBox

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
		self.owner = None
		self.awaitingOwner = False

	def getCurrentTile(self):
		for obj in Terrain.List:
			if Collision.contains(obj, self.rect.x + self.width/2, self.rect.y + self.height/2):
				return obj

	def update(self):
		if self.owner == None:
			return
		self.rect.x = self.owner.rect.x + (self.owner.width / 2) * self.owner.xDir
		self.rect.y = self.owner.rect.y - 10

	def motion(self, x, y):
		if self.owner:
			self.gridX = self.owner.rect.x - x
			self.gridY = self.owner.rect.y - y + 10

		self.rect.x = self.gridX + x
		self.rect.y = self.gridY + y

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
		self.cargo = {Box(0, 200, 30, 30, images.boxClosed), Box(0, 200, 30, 30, images.boxClosed), Box(0, 200, 30, 30, images.boxClosed), Box(0, 200, 30, 30, images.boxClosed), Box(0, 200, 30, 30, images.boxClosed), Box(0, 200, 30, 30, images.boxClosed)}
		for c in self.cargo:
			c.owner = self
		self.targetSet = True
		self.targetX = 200
		self.xDir = 1
		self.xSpeed, self.ySpeed, self.acceleration = 0, 0, 1
		self.movementSpeed, self.maxSpeed = 2, 5

	def motion(self, x, y):
		self.xSpeed += self.acceleration
		self.xSpeed *= .9
		self.rect.x = self.gridX + x
		self.rect.y = self.gridY + y
		self.gridX += self.xSpeed

		if abs(self.xSpeed) > self.maxSpeed:
			self.xSpeed = self.maxSpeed * -self.xDir

		self.walkX = self.rect.x + (self.width/2)
		self.walkY = self.rect.y + self.height

	def update(self):
		if(self.targetSet):
			self.navigate()

		if self.xSpeed < 0:
			self.xDir = 1
		elif self.xSpeed > 0:
			self.xDir = -1
		else:
			self.xDir = 0

		temp = self.cargo.copy()
		for c in temp:
			c.update()
			if c.owner != self:
				self.cargo.remove(c)

		if len(self.cargo) == 0:
			self.state = Truck.DRIVING
			self.targetSet = True
			self.targetX = -100

		if self.state == Truck.DRIVING and self.rect.x <= -100:
			self.kill()

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
			for i, c in enumerate(self.cargo):
				TaskManager.addTask(Task.MOVE_OBJECT, self.getCurrentTile(), None, c)
			self.xSpeed = 0
			self.targetSet = False

	def getCurrentTile(self):
		for obj in Terrain.List:
			if Collision.contains(obj, self.rect.x + self.width, self.rect.y + self.height):
				return obj


class Customer(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.FOREGROUND)
		Customer.List.add(self)
		#MOTION
		self.xSpeed, self.ySpeed = 0, 0
		self.movementSpeed, self.xDir, self.yDir = 3, 1, 1
		
		#PATHFINDING
		self.targetSet = False
		self.targetTile = None
		self.currentTile = self.getCurrentTile()
		self.nextTile = None
		self.path = Queue.Queue()

		#TASKING
		self.task = None
		self.currentAction = None

		#INTERACTION
		self.holdingObject = None
		self.textBubble = None

		#ANIMATION
		self.STANDING = 0
		self.WALKING = 1
		self.state = self.STANDING

		img = sprite.getSpriteSheet(images.employee_1, (0,0,30,30), 3)
		self.sprite_front = img[0]
		self.sprite_side = img[1]
		self.sprite_back = img[2]
		
	def assignTask(self, task):
		self.task = task
		self.task.owner = self
		self.currentAction = task.takeAction()
		self.targetSet = False

	def isBusy(self):
		if self.task == None:
			return False
		else:		
			return self.task.actions.empty()
	
	def playTask(self, grid):
		if self.currentAction == None:
			return

		if self.currentAction.actionType == Task.MOVE_TO:
			if not self.targetSet:
				self.setTargetTile(self.currentAction.interactTo, grid)
			self.navigate()

		if self.currentAction.actionType == Task.MOVE_OBJECT:
			while not self.currentAction.interactTo or self.currentAction.interactTo.occupied:
				self.targetSet = False
				newTo = Terrain.getVacantTileInZone(Terrain.DELIVERABLES)
				if not newTo:
					newTo = Terrain.getTileAtGridPos(((int)(random.random()*15), (int)(random.random()*9)))
				self.currentAction.interactTo = newTo

			if not self.targetSet:
				self.setTargetTile(self.currentAction.interactTo, grid)
			
			self.navigate()

		elif self.currentAction.actionType == Task.PICK_UP_OBJECT:
			self.holdingObject = self.currentAction.interactionObject
			self.holdingObject.getCurrentTile().occupied = False
			self.currentAction.interactionObject.owner = self
			self.currentAction.isDone = True

		elif self.currentAction.actionType == Task.DROP_OBJECT:
			self.holdingObject.rect.x = self.getCurrentTile().rect.x
			self.holdingObject.rect.y = self.getCurrentTile().rect.y
			self.getCurrentTile().occupied = True
			self.currentAction.interactionObject.owner = None
			self.currentAction.interactionObject.awaitingOwner = False
			self.holdingObject = None
			self.currentAction.isDone = True

		if self.currentAction.isDone:
			if not self.task.isDone():
				self.currentAction = self.task.takeAction()
				if self.textBubble:
					self.textBubble.kill()
				self.textBubble = TextBox(300, 342, "work", self.currentAction.names[self.currentAction.actionType])
			else:
				self.task = None
				self.targetSet = False

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

	def setTargetTile(self, obj, grid):
		if not obj or not obj.walkable:
			return None
		else:
			self.targetTile = obj

			self.targetSet = True
			self.path = self.getPath(self.targetTile, grid)
			if self.path == None:
				self.targetSet = False
				return None

			self.nextTile = self.getNextTile()

			return True

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

	def update(self, grid):
		self.animate(self.state)
		#if(self.targetSet):
		#	self.navigate()
		if self.task != None:
			self.playTask(grid)

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

		if self.textBubble:
			self.textBubble.update(self.rect.x, self.rect.y, self.width, self.height)

		if self.holdingObject:
			self.holdingObject.update()

	def getPath(self, goalTile, grid):
		self.currentTile = self.getCurrentTile()
		if self.currentTile == None:
			print "~error: Current tile is None"
			return

		start = self.currentTile.gridPos
		goal = goalTile.gridPos
		parents, cost = AI.calculatePath(grid, start, goal)

		return AI.reconstructPath(parents, start, goal)

	def navigate(self):
		if not self.nextTile:
			print "~error in navigate(self): nextTile"
			return
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
				self.currentAction.isDone = True

class Terrain(BaseClass):
	List = pygame.sprite.Group()
	zones = []
	DELIVERABLES = 0
	GARBAGE = 1
	def __init__(self, x, y, gridPos, width, height, image_string, walkable, buildable = True, palette=None):
		BaseClass.__init__(self, x, y, width, height, image_string, BaseClass.BACKGROUND)
		Terrain.List.add(self)
		self.gridPos = gridPos
		self.walkable = walkable
		self.buildable = buildable
		self.occupied = False
		self.zone = None

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

	@staticmethod
	def getTileAtGridPos(pos):
		for tile in Terrain.List:
			if tile.gridPos == pos:
				return tile

	@staticmethod
	def getZoneAtGridPos(pos):
		for tile in Terrain.List:
			if tile.gridPos == pos:
				return tile.zone

	@staticmethod
	def getVacantTileInZone(zone):
		list = []
		r = None
		for tile in Terrain.List:
			if tile.zone == zone and not tile.occupied:
				list.append(tile)
		if len(list) > 0: 
			r = list[(int)(random.random()* len(list))]
		return r

class BlueFloor(Terrain):
	def __init__(self, x, y, gridPos):
		width = 30
		height = 30

		# RGB values are in reverse order, so (Blue, Green, Red)
		palette = [hexToBGR(0x8EAEE0), hexToBGR(0x5D7394), hexToBGR(0x5D7394), hexToBGR(0x354154)]

		Terrain.__init__(self, x, y, gridPos, width, height, images.grayScaleFloor, True, True, palette)

