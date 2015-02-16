import pygame, sys, math, random
from classes import *
from maps import *
from ai import AI, GridWithWeights

pygame.init()

# SETTINGS

FULLSCREEN = False
if FULLSCREEN:
	screenInfo = pygame.display.Info()
	SCREEN_WIDTH, SCREEN_HEIGHT = screenInfo.current_w, screenInfo.current_h
	FLAGS = pygame.FULLSCREEN | pygame.DOUBLEBUF
else: 
	SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
	FLAGS = pygame.DOUBLEBUF

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS, 32)
screen.set_alpha(None)
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

#AI
grid = GridWithWeights(matrix)

# AI TESTS
# parents, cost = AI.aStarSearch(grid, (1, 1), (10, 10))
# path = AI.reconstructPath(parents, (1, 1), (10, 10))
# grid.printPath((1, 1), (10, 10), path)

# AI

# MISC
# MISC

# UNITS
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")
Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")

#UNITS
# ---------- MAIN GAME LOOP -------------
while True:
	totalframes += 1	

	for event in pygame.event.get():  
			if event.type == pygame.QUIT:  
				pygame.quit()  
				sys.exit() 	

		#	if event.type == pygame.MOUSEBUTTONUP:
		#		x, y = pygame.mouse.get_pos()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

	for c in Customer.List:
		x = (int)(random.random() * SCREEN_WIDTH)
		y = (int)(random.random() * SCREEN_HEIGHT)

		obj = Collision.getTileAt(Terrain.List, x, y)
		if c.targetSet == False and obj != None:
			c.setTarget(obj, grid)

	#LOGIC
	for c in Customer.List:
		c.motion()
		c.update()
	#LOGIC

	#COLLISION 

	#COLLISION 


	#MISC

	#MISC


	#DRAW
	screen.fill((255, 255, 255))
	BaseClass.backgroundSprites.draw(screen)
	BaseClass.foregroundSprites.draw(screen)
	pygame.display.flip()	
	#DRAW

	#LOGIC
	clock.tick(FPS)
	#LOGIC