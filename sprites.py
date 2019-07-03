import pygame as pg
from settings import *
vec = pg.math.Vector2
import random

class SpriteSheet:
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert()

	def get_image(self, x, y, width,height):
		image = pg.Surface((width, height))
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		image = pg.transform.scale(image, (width//2, height//2))
		return image

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.load_images()
		self.image = self.car
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.center = (width/2, height - 50)
		self.pos = vec(width/2, height - 100)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.lives = 3
		self.hidden = False

	def load_images(self):
		self.car = self.game.spritesheet.get_image(211, 941, 99, 75).convert()

	def update(self):

		if self.hidden and pg.time.get_ticks() > 1500:
			self.hidden = False
			self.rect.center = (width/2, height - 50)

		self.acc = vec(0, 0)
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.acc.x += -player_acc
		if keys[pg.K_RIGHT]:
			self.acc.x += player_acc

		self.acc.x += self.vel.x * player_friction

		self.vel += self.acc
		self.pos += self.vel + self.acc

		self.rect.center = self.pos

		if self.rect.right > width:
			self.rect.right = width
		if self.rect.left< 0:
			self.rect.left = 0

	def hide(self):
		self.hidden = True
		self.hide_timer = pg.time.get_ticks()
		self.rect.center = (width/2, height + 200)
		self.lives -= 1

class Mob(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.all_sprites, game.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.load_images()
		pos_list = [50, 100, 150, 200, 250, 300, 350, 400, 450]
		w = pos_list[random.randrange(1, 9)]
		self.image = random.choice(self.mob_car_list)
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.center = (w, -50)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.pos = vec(w, 0)
		self.meteor_dir_x = random.random()

	def load_images(self):
		self.mob_car_list = [self.game.spritesheet.get_image(237, 452, 45, 40).convert(), self.game.spritesheet.get_image(224, 748, 101, 84).convert(), self.game.spritesheet.get_image(0, 520, 120, 98).convert()]

	def update(self):
		self.acc = vec(0, mob_gravity)
		self.vel.y += self.acc.y
		self.pos += self.vel + self.acc
		self.rect.center = self.pos

		if self.pos.y > height + 50:
			self.game.score += 10
			self.kill()

