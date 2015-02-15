import pygame, sys, math
from classes import *
from maps import *

pygame.init()

# SETTINGS
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()
FPS = 40
fivesecondinterval = FPS * 5
totalframes = 0
#SETTINGS

#TERRAIN
TILE_SIZE = 30
matrix = [[0 for i in xrange((SCREEN_WIDTH+TILE_SIZE) / TILE_SIZE)] for i in xrange((SCREEN_HEIGHT+TILE_SIZE) / TILE_SIZE)]
matrix = loadMap(matrix)
generateMap(matrix)
#TERRAIN

#MISC
x, y = 0, 0 #Mouse coordinates
#MISC

#UNITS
c = Customer(150, 150, 30, 30, "img/customer/coin.png")
#UNITS
# ---------- MAIN GAME LOOP -------------
while True:
	
	c.motion()
	c.update()
	
	totalframes += 1	

	for event in pygame.event.get():  
			if event.type == pygame.QUIT:  
				pygame.quit()  
				sys.exit() 	

			if event.type == pygame.MOUSEBUTTONUP:
				x, y = pygame.mouse.get_pos()
				for obj in Terrain.List:
					if Collision.contains(obj, x, y):
						c.setTarget(obj)

	#LOGIC
	#for c in Customer.List:
		#c.motion()
		#c.update()
	#LOGIC

	#COLLISION 

	#COLLISION 


	#MISC

	#MISC


	#DRAW
	screen.fill((255, 255, 255))
	BaseClass.backgroundSprites.draw(screen)
	pygame.display.update()	
	BaseClass.foregroundSprites.draw(screen)
	pygame.display.flip()	
	#DRAW

	#LOGIC
	clock.tick(FPS)
	#LOGIC