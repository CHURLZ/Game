import pygame, sys, math, random
from classes import *
from maps import *
from builder import *
from ai import AI

pygame.init()

# SETTINGS

FULLSCREEN = False
if FULLSCREEN:
	screenInfo = pygame.display.Info()
	SCREEN_WIDTH, SCREEN_HEIGHT = screenInfo.current_w, screenInfo.current_h
	FLAGS = pygame.FULLSCREEN | pygame.DOUBLEBUF
else: 
	SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
	FLAGS = pygame.DOUBLEBUF

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS, 32)
screen.set_alpha(None)
clock = pygame.time.Clock()
FPS = 40
fiveSecondinterval = FPS * 5
totalFrames = 0
# SETTINGS

# TERRAIN
TILE_SIZE = 30
matrix = [[0 for i in xrange((SCREEN_WIDTH+TILE_SIZE) / TILE_SIZE)] for i in xrange((SCREEN_HEIGHT+TILE_SIZE) / TILE_SIZE)]
matrix = loadMap(matrix)
generateMap(matrix)
#TERRAIN

# AI
grid = GridWithWeights(matrix)
# AI

# MISC
# MISC

# BUILD
initBuild = False
buildFrom = None
buildTo = None
# BUILD

# UNITS
for i in xrange(1, 2):
	Customer(150, 150, 30, 30, "img/customer/customer_1_front.png")

Truck(1920, 495, 60, 30, "img/truck.png")

# UNITS

# ---------- MAIN GAME LOOP -------------
while True:
	totalFrames += 1	

	for event in pygame.event.get():  
			if event.type == pygame.QUIT:  
				pygame.quit()  
				sys.exit() 	

			if event.type == pygame.MOUSEBUTTONDOWN:
				initBuild = True
				x, y = pygame.mouse.get_pos()
				buildFrom = Collision.getObjectAt(Terrain.List, x, y)

			if event.type == pygame.MOUSEBUTTONUP:
				x, y = pygame.mouse.get_pos()
				#obj = Collision.getObjectAt(Terrain.List, x, y)
				#Box(obj.rect.x, obj.rect.y, 30, 30, "img/box_full.png")
				if initBuild:
					buildTo = Collision.getObjectAt(Terrain.List, x, y)
					buildPlan = builder.calculatePath(buildFrom, buildTo, Terrain.List)
					initBuild - False
					dX = abs(buildFrom.rect.x - buildTo.rect.x)
					dY = abs(buildFrom.rect.y - buildTo.rect.y)
					if dX < dY:
						img = "img/BrickWallVertical.png"
					else:
						img = "img/BrickWallHorizontal.png"
					for tile in buildPlan:
						tile.image = pygame.image.load(img)
						tile.default_image = img
						tile.walkable = False
				for c in Customer.List:
					c.setTarget(c.targetTile, grid)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

	for c in Customer.List:
		x = (int)(random.random() * SCREEN_WIDTH)
		y = (int)(random.random() * SCREEN_HEIGHT)

		obj = Collision.getObjectAt(Terrain.List, x, y)
		if c.targetSet == False and obj != None:
			c.setTarget(obj, grid)

	#LOGIC
	for c in Customer.List:
		c.motion()
		c.update()

	for t in Truck.List:
		t.motion()
		t.update()
	grid.update(Terrain.List)
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