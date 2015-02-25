import pygame, images, threading
from sprites import *
from player import *

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 30

class GUIBaseClass(pygame.sprite.Sprite):
	allSprites = pygame.sprite.OrderedUpdates()

	def __init__(self, x, y, width, height, image):
		pygame.sprite.Sprite.__init__(self)
		GUIBaseClass.allSprites.add(self)
		self.image = image
		self.image.set_alpha(128)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height
		self.active = False

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
		self.killIn(2000)

	def update(self, x, y, w, h):
		self.rect.x = x - w * 3 - 10 
		self.rect.y = y - (20 + h)

	def killIn(self, ms):
		threading.Timer(ms/1000, self.kill).start()


class CashBar(GUIBaseClass):
	lastCash = Player.cash
	textOffsetX = 30
	textOffsetY = 7
	width = 50
	height = 30

	def __init__(self, x, y):
		if not pygame.font.get_init():
			pygame.font.init()
		# Set up font and textlabel
		self.font = pygame.font.SysFont(None, 20)
		text = self.font.render(str(Player.cash), True, (0, 0, 0))
		textRect = text.get_rect()

		self.image = images.cashBar.copy()
		imageRect = self.image.get_rect()

		self.image.blit(text, (imageRect.width - (textRect.width + self.textOffsetX), self.textOffsetY, textRect.width, textRect.height))

		GUIBaseClass.__init__(self, x, y, CashBar.width, CashBar.height, self.image)


	def update(self):
		if Player.cash != self.lastCash:
		 	text = self.font.render(str(Player.cash), True, (0, 0, 0))
		 	textRect = text.get_rect()
		 	self.image = images.cashBar.copy()
		 	imageRect = self.image.get_rect()

		 	self.image.blit(text, (imageRect.width - (textRect.width + self.textOffsetX), self.textOffsetY, textRect.width, textRect.height))

		 	self.lastCash = Player.cash

class ActionPanel(GUIBaseClass):
	buttons = pygame.sprite.Group()
	cashBar = CashBar(700, 0)
	active = None # TO HIGHLIGHT ACTIVE BUTTON
	def __init__(self, x, y, width, height, image):
		image = image.convert()
		image.set_alpha(100)
		GUIBaseClass.__init__(self, x, y, width, height, image)
		self.buttons.add(ZoningButton(self.rect.x + 10, self.rect.y + 20, BUTTON_WIDTH, BUTTON_HEIGHT, None))
		self.buttons.add(WallingButton(self.rect.x + 10, self.rect.y + BUTTON_HEIGHT + 40, BUTTON_WIDTH, BUTTON_HEIGHT, None))
		active = None

	@staticmethod
	def updatePanel():
		ActionPanel.cashBar.update()
		for button in ActionPanel.buttons:
			if button == ActionPanel.active and not button.active:
				button.image.set_alpha(255)
				button.active = True
			elif button != ActionPanel.active and button.active:
				button.image.set_alpha(175)
				button.active = False

class ActionButton(ActionPanel):
	def __init__(self, x, y, width, height, image):
		GUIBaseClass.__init__(self, x, y, width, height, image)
		image = image.convert()
		image.set_alpha(175)
		
	def onClick(self):
		ActionPanel.active = self
		return

class WallingButton(ActionButton):
	def __init__(self, x, y, width, height, image):
		ActionButton.__init__(self, x, y, width, height,  images.zoneButton)

	def onClick(self, builder):
		ActionPanel.active = self
		ActionPanel.updatePanel()
		builder.state = builder.WALL

class ZoningButton(ActionButton):
	def __init__(self, x, y, width, height, image):
		ActionButton.__init__(self, x, y, width, height, images.wallButton)

	def onClick(self, builder):
		ActionPanel.active = self
		ActionPanel.updatePanel()
		builder.state = builder.ZONE