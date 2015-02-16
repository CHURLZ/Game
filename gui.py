import pygame

class GUIBaseClass(pygame.sprite.Sprite):
	allSprites = pygame.sprite.OrderedUpdates()

	def __init__(self, x, y, width, height, image_string):
		pygame.sprite.Sprite.__init__(self)

		GUIBaseClass.allSprites.add(self)

		self.image = pygame.image.load(image_string).convert_alpha()
		self.image.set_alpha(128)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height
		self.walkX = x + (width / 2)
		self.walkY = y + height 
		self.centerX = self.walkX
		self.centerY = self.rect.y + (height / 2)

class ActionPanel(GUIBaseClass):
	List = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image_string):
		GUIBaseClass.__init__(self, x, y, width, height, image_string)
		ActionPanel.List.add(self)
