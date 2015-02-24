import pygame, images
from sprites import *

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 30

class GUIBaseClass(pygame.sprite.Sprite):
	allSprites = pygame.sprite.OrderedUpdates()

	def __init__(self, x, y, width, height, image):
		pygame.sprite.Sprite.__init__(self)

		GUIBaseClass.allSprites.add(self)

		self.image = image.convert_alpha()
		self.image.set_alpha(100)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height
		self.walkX = x + (width / 2)
		self.walkY = y + height 
		self.centerX = self.walkX
		self.centerY = self.rect.y + (height / 2)

class TextBox(GUIBaseClass):
	def __init__(self, x, y, title, body, width = 0, height = 0):
		TILE_SIZE = 15

		tiles = sprite.getSpriteSheet(images.textBox, (0, 0, TILE_SIZE, TILE_SIZE), 9)

		# Set up font and textlabel
		font = pygame.font.SysFont(None, 12)
		text = font.render(body, True, (0, 0, 0))
		textRect = text.get_rect()
		
		if width == 0 or height == 0:
			width = textRect.width + TILE_SIZE * 3
			height = textRect.height + TILE_SIZE * 3

		image = pygame.Surface((width, height), pygame.SRCALPHA)
			
		# Draw corners on to the image		
		image.blit(tiles[0], (0, 0, TILE_SIZE, TILE_SIZE))
		image.blit(tiles[2], (width - TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
		image.blit(tiles[4], (width - TILE_SIZE, height - (TILE_SIZE * 2), TILE_SIZE, TILE_SIZE))
		image.blit(tiles[6], (0, height - (TILE_SIZE * 2), TILE_SIZE, TILE_SIZE))

		# Draw straight stuffs 
		for i in xrange(1, (width / TILE_SIZE)):
			image.blit(tiles[1], (TILE_SIZE * i, 0, TILE_SIZE, TILE_SIZE))
			image.blit(tiles[5], (TILE_SIZE * i, height - (TILE_SIZE * 2), TILE_SIZE, TILE_SIZE))

		for i in xrange(1, (height / TILE_SIZE) - 1):
			image.blit(tiles[3], (width - TILE_SIZE, TILE_SIZE * i, TILE_SIZE, TILE_SIZE))
			image.blit(tiles[7], (0, TILE_SIZE * i, TILE_SIZE, TILE_SIZE))
		
		for i in xrange(1, (height / TILE_SIZE) - 1):
			for j in xrange(1, width / TILE_SIZE):
				image.blit(tiles[8], (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))	

		# Draw arrow!
		image.blit(images.textBoxArrow, (width - (TILE_SIZE * 2), height - (TILE_SIZE * 2) + 7, TILE_SIZE, TILE_SIZE))

		# Draw Text
		image.blit(text, ((width - textRect.width) / 2, height / 2 - textRect.height - 2, width, height))

		GUIBaseClass.__init__(self, x, y, width, height, image)



class ActionPanel(GUIBaseClass):
	buttons = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image):
		GUIBaseClass.__init__(self, x, y, width, height, image)

		self.buttons.add(ZoningButton(self.rect.x + 10, self.rect.y + 20, BUTTON_WIDTH, BUTTON_HEIGHT, images.zoneButton))
		self.buttons.add(WallingButton(self.rect.x + 10, self.rect.y + BUTTON_HEIGHT + 40, BUTTON_WIDTH, BUTTON_HEIGHT, images.wallButton))

class ActionButton(ActionPanel):
	def __init__(self, x, y, width, height, image):
		GUIBaseClass.__init__(self, x, y, width, height, image)

		ActionPanel.buttons.add(self)
		
	def onClick(self):
		return

class WallingButton(ActionButton):
	def __init__(self, x, y, width, height, image):
		ActionButton.__init__(self, x, y, width, height, image)

	def onClick(self, builder):
		builder.state = builder.WALL
		print "WALLING"

class ZoningButton(ActionButton):
	def __init__(self, x, y, width, height, image):
		ActionButton.__init__(self, x, y, width, height, image)

	def onClick(self, builder):
		builder.state = builder.ZONE
		print "ZONING"
