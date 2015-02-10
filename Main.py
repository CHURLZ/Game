import pygame, sys, math
from classes import *
from maps import *

pygame.init()

# SETTINGS
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()
FPS = 60
fivesecondinterval = FPS * 5
totalframes = 0
#SETTINGS

#UNITS
#player = Player(100, 0, 23, 30, "img/player/player.png")
#UNITS

#TERRAIN
TILE_SIZE = 30
matrix = [[0 for i in xrange((SCREEN_WIDTH+TILE_SIZE) / TILE_SIZE)] for i in xrange((SCREEN_HEIGHT+TILE_SIZE) / TILE_SIZE)]
matrix = loadMap(matrix)
generateMap(matrix)
#TERRAIN


# ---------- MAIN GAME LOOP -------------
while True:
	#process(player)
	
	totalframes += 1
	#player.motion()
	#player.update()
	x, y = 0, 0

	c = Customer(100, 0, 30, 30, "img/customer/coin.png")

	for event in pygame.event.get():  
			if event.type == pygame.QUIT:  
				pygame.quit()  
				sys.exit() 	

			if event.type == pygame.MOUSEBUTTONUP:
				x, y = pygame.mouse.get_pos()
				print "navigate customer to pos"
				#customer navigate to pos

	#LOGIC
	for c in Customer.List:
		c.motion()
		c.update()
		c.navigate(x, y)


	#COLLISION 

	#COLLISION 


	#MISC

	#MISC


	#DRAW
	screen.fill((255, 255, 255))
	BaseClass.allSprites.draw(screen)
	pygame.display.flip()	
	#DRAW

	#LOGIC
	clock.tick(FPS)
	#LOGIC