#Main game file, run this file to run the game


import pygame as pg
import random
import sys
from settings import *
from sprites import *
from os import path
vec = pg.math.Vector2

class Game:
	def __init__(self):
		self.running = True
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((width, height))
		pg.display.set_caption("Dodger")
		self.clock = pg.time.Clock()
		self.font_name = pg.font.match_font(font_name)
		self.load_data()

	def load_data(self):
		self.dir = path.dirname(__file__)
		img_dir = path.join(self.dir, 'img')
		self.snd_dir = path.join(self.dir, 'snd')

		self.spritesheet = SpriteSheet(path.join(img_dir, spritesheet))

		self.image = pg.image.load(path.join(img_dir, bg)).convert()
		self.rect = self.image.get_rect()

	def new(self):
		self.score = 0
		self.all_sprites = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.player = Player(self)
		self.mob_list = []
		self.playing = True
		pg.mixer.music.load(path.join(self.snd_dir, 'music.ogg'))
		self.run()

	def run(self):
		pg.mixer.music.play(loops=-1)
		while self.playing:
			self.clock.tick(fps)
			self.events()
			self.update()
			self.draw()
		pg.mixer.music.fadeout(800)

	def update(self):
		self.all_sprites.update()
		self.drop_enemies()

		#Collision Check
		hits = pg.sprite.spritecollide(self.player, self.mobs, False)
		if hits: 
			self.player.hide()
			

		if self.player.lives == 0:
			self.player.kill()
			self.playing = False

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
				sys.exit()

	def draw(self):
		self.screen.fill(white)
		self.screen.blit(self.image, self.rect)
		self.all_sprites.draw(self.screen)
		self.draw_text(str(self.score), 48, white, width - 50, height - 50)
		pg.display.flip()

	def show_start_screen(self):
		pg.mixer.music.load(path.join(self.snd_dir, 'menu.wav'))
		pg.mixer.music.play(loops=-1)
		self.screen.fill(white)
		self.screen.blit(self.image, self.rect)
		self.draw_text("Dodger", 48, white, width/2, 100)
		self.draw_text("Left and Right Arrows to Move", 24, white, width/2, 200)
		self.draw_text("Dodge the Meteors!", 24, white, width/2, 250)
		self.draw_text("Press SPACE to Begin", 24, white, width/2, 300)
		pg.display.flip()
		self.wait_for_key()
		pg.mixer.music.fadeout(500)

	def wait_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(fps)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = True
					self.running = False
				if event.type == pg.KEYUP:
					if event.key == pg.K_SPACE:
						waiting = False

	def show_go_screen(self):
		pg.mixer.music.load(path.join(self.snd_dir, 'menu.wav'))
		pg.mixer.music.play(loops=-1)
		self.screen.fill(white)
		self.screen.blit(self.image, self.rect)
		self.draw_text("GAME OVER", 48, white, width/2, height/4)
		self.draw_text("Score: " + str(self.score), 22, white, width/2, height*3/4)
		self.draw_text("Press SPACE to play again", 22, white, width/2, height * 3/4 + 25)
		if not self.running:
			return None

		pg.display.flip()
		self.wait_for_key()
		pg.mixer.music.fadeout(500)

	def draw_text(self, text, size, color, x, y):
		font = pg.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

	def drop_enemies(self):
		if len(self.mobs) > 5:
			pass
		elif len(self.mobs) < 5:
			delay = random.random()
			if delay < 0.07:
				m = Mob(self)
				self.mob_list.append(m)

g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_go_screen()

pg.quit()

