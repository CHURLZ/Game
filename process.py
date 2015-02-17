import pygame, sys
from builder import *


def process(god):
	for event in pygame.event.get():  
		if event.type == pygame.QUIT:  
			pygame.quit()  
			sys.exit() 	

		if event.type == pygame.MOUSEBUTTONDOWN:
			tX, tY = pygame.mouse.get_pos()
			x, y = tX + god.CAMERA_X, tY + god.CAMERA_Y
			if event.button == 1:
				builder.initBuild = True
				builder.buildFrom = Collision.getObjectAt(Terrain.List, x, y)
			if event.button == 3:
				builder.initRemove = True
				builder.buildFrom = Collision.getObjectAt(Terrain.List, x, y)

		if event.type == pygame.MOUSEBUTTONUP:
				tX, tY = pygame.mouse.get_pos()
				x, y = tX + god.CAMERA_X, tY + god.CAMERA_Y

				if event.button == 1:
					builder.buildWall(x, y)
					
				elif(event.button == 3):
					builder.destroyWall(x, y)


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == pygame.K_w:
				god.key_w = True

			if event.key == pygame.K_s:
				god.key_s = True

			if event.key == pygame.K_d:
				god.key_d = True

			if event.key == pygame.K_a:
				god.key_a = True

			if event.key == pygame.K_LSHIFT:
				god.key_LSHIFT = True

		if event.type == pygame.KEYUP:		
			if event.key == pygame.K_w:
				god.key_w = False

			if event.key == pygame.K_s:
				god.key_s = False

			if event.key == pygame.K_d:
				god.key_d = False

			if event.key == pygame.K_a:
				god.key_a = False

			if event.key == pygame.K_LSHIFT:
				god.key_LSHIFT = False
