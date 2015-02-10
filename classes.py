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

	def update(self):
		self.animate(0)
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
			self.xSpeed = -self.movementSpeed
		elif self.rect.x > rect.x:
			self.xSpeed = self.movementSpeed
			pass
		if self.rect.y < rect.y:
			self.ySpeed = -self.movementSpeed
		elif self.rect.y > rect.y:
			self.ySpeed = self.movementSpeed
			pass

	def navigate(self, x, y):
		if self.rect.x < x:
			self.xSpeed = -self.movementSpeed
		elif self.rect.x > x:
			self.xSpeed = self.movementSpeed
			pass
		if self.rect.y < y:
			self.ySpeed = -self.movementSpeed
		elif self.rect.y > y:
			self.ySpeed = self.movementSpeed
			pass

