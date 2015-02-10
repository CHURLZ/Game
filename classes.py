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
	Employee.List.add(self)

class Customer(BaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
	Customer.List.add(self)