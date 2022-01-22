import pygame 
from support import import_folder


class Tile(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		super().__init__()
		self.image = pygame.Surface((size, size))
		self.rect = self.image.get_rect(topleft=(x, y))

	def update(self, shift):
		self.rect.x += shift


# static object

class StaticTile(Tile):
	def __init__(self, size, x, y, surface):
		super().__init__(size, x, y)
		self.image = surface 


# objects with different collision variations

class Crate(StaticTile):
	def __init__(self, path, size, x, y):
		super().__init__(size, x, y, pygame.image.load(path).convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Ladder(StaticTile):
	def __init__(self, path, size, x, y):
		super().__init__(size, x, y, pygame.image.load(path).convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft=(x, offset_y))


# animated objects

class AnimatedTile(Tile):
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self, shift):
		self.animate()
		self.rect.x += shift


class AnimatedCoin(AnimatedTile):
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y, path)
		self.rect = self.image.get_rect(center=(x + int(size / 2), y + int(size / 2)))


class Ridge(AnimatedTile):
	def __init__(self, size, x, y, path, offset):
		super().__init__(size, x, y, path)
		self.rect.topleft = (x, y - offset)