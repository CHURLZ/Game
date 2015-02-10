import random, threading
import pygame, math

class BaseClass(pygame.sprite.Sprite):
	allSprites = pygame.sprite.Group()

	def __init__(self, x, y, width, height, image_string):
		pygame.sprite.Sprite.__init__(self)
		BaseClass.allSprites.add(self)

		self.image = pygame.image.load(image_string)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height

class Terrain(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string, platform):
		BaseClass.__init__(self, x, y, width, height, image_string)
		Terrain.List.add(self)

class Employee(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string)
		Employee.List.add(self)

class Customer(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		BaseClass.__init__(self, x, y, width, height, image_string)
		self.xSpeed, self.ySpeed = 0, 0
		self.movementSpeed, self.xDir, self.yDir = 0, 1, 1
		Customer.List.add(self)

	def motion(self):
		#CONTROLLERS
		self.xSpeed = self.movementSpeed
		self.ySpeed = self.movementSpeed 
		self.rect.x += self.xSpeed
		self.rect.y += self.ySpeed
		#CONTROLLERS

	def animate(self, state):
		flipped = ""
		if self.xDir == 1:
			flipped ="_flipped"
		if self.animCounter % 10 == 0:
			if self.state == BaseClass.STATE_WALKING:
				self.image = pygame.image.load("img/player/player"+flipped+".png")
			
			if self.state == BaseClass.STATE_STANDING:
				self.image = pygame.image.load("img/player/player"+flipped+".png")

	def update(self):
		self.animate(self.state)
		if self.xSpeed < 0:
			self.xDir = -1
		elif self.xSpeed > 0:
			self.xDir = 1
		if self.ySpeed < 0:
			self.yDir = -1
		elif self.ySpeed > 0:
			self.yDir = 1

	def navigate(self, rect):
		if self.rect.x < rect.x:
			xSpeed = -movementSpeed
		elif self.rect.x > rect.x:
			xSpeed = movementSpeed
			pass
		if self.rect.y < rect.y:
			ySpeed = -movementSpeed
		elif self.rect.y > rect.y:
			ySpeed = movementSpeed
			pass

