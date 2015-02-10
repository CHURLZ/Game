import math

class Collision:
	@staticmethod	
	def collide(objA, objB):
		if objA.rect.x > objB.rect.x+objB.width:
			return False
		if objA.rect.x + objA.width < objB.rect.x:
			return False
		if objA.rect.y > objB.rect.y+objB.height:
			return False	
		if objA.rect.y + objA.height < objB.rect.y:
			return False

		return True

	@staticmethod	
	def contains(objA, x, y):

		if x > objA.rect.x + objA.width:
			return False
		if x < objA.rect.x:
			return False
		if y > objA.rect.y + objA.height:
			return False
		if y < objA.rect.y:
			return False

		return True
