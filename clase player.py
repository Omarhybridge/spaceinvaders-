import pygame
import sys
import os
import importlib.util
from Shipclass import Ship

# Importa la clase Bullet desde 'Clase bullet.py' de forma segura
Bullet = None
try:
	current_dir = os.path.dirname(__file__)
	bullet_spec = importlib.util.spec_from_file_location("clase_bullet", os.path.join(current_dir, "Clase bullet.py"))
	if bullet_spec and bullet_spec.loader:
		clase_bullet = importlib.util.module_from_spec(bullet_spec)
		bullet_spec.loader.exec_module(clase_bullet)
		Bullet = getattr(clase_bullet, "Bullet", None)
except Exception:
	Bullet = None

# Importa la clase Enemy desde 'Clase enemy.py' de forma segura
Enemy = None
try:
	current_dir = os.path.dirname(__file__)
	enemy_spec = importlib.util.spec_from_file_location("clase_enemy", os.path.join(current_dir, "Clase enemy.py"))
	if enemy_spec and enemy_spec.loader:
		clase_enemy = importlib.util.module_from_spec(enemy_spec)
		enemy_spec.loader.exec_module(clase_enemy)
		Enemy = getattr(clase_enemy, "Enemy", None)
except Exception:
	Enemy = None

class player(Ship):
	def __init__(self, x, y, ship_img=None, bullet_img=None, health=100, x_speed=0, y_speed=0, bullet_speed=10):
		super().__init__(x, y, health)
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.ship_img = ship_img
		self.bullet_img = bullet_img
		self.health = health
		self.bullet_speed = bullet_speed
		self.mask = pygame.mask.from_surface(self.ship_img) if self.ship_img else None

		self.max_bullets = 3
		self.max_amount_bullets = 3
		self.bullets = []
		self.fired_bullets = []
		self.creation_cooldown_counter = 0
		self.bullet_cooldown_counter = 0
		self.cool_down = 120

	def move(self, WIDTH, HEIGHT):
		keys = pygame.key.get_pressed()

		if (keys[pygame.K_UP] or keys[pygame.K_w]) and (self.y > 0):
			self.y -= self.y_speed
		elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (self.y < HEIGHT - self.ship_img.get_height() - 60):
			self.y += self.y_speed

		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (self.x < WIDTH - self.ship_img.get_width()):
			self.x += self.x_speed
		elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (self.x > 0):
			self.x -= self.x_speed

	def increase_speed(self):
		if self.x_speed < 10:
			self.x_speed += 1.25
			self.y_speed += 1.25
		elif self.x_speed >= 10:
			self.x_speed = 10
			self.y_speed = 8
		if self.cool_down > 25:
			self.cool_down *= 0.9

	def create_bullets(self):
		if (len(self.bullets) < self.max_amount_bullets) and (self.creation_cooldown_counter == 0):
			bullet = Bullet(self.x, self.y, self.bullet_img)
			self.bullets.append(bullet)
			self.creation_cooldown_counter = 1

		for bullet in self.fired_bullets[:]:
			if bullet.y <= -40:
				self.fired_bullets.remove(bullet)

	def update_cooldowns(self):
		if self.bullet_cooldown_counter >= 20:
			self.bullet_cooldown_counter = 0
		elif 0 < self.bullet_cooldown_counter < 20:
			self.bullet_cooldown_counter += 1

		if self.creation_cooldown_counter >= self.cool_down:
			self.creation_cooldown_counter = 0
		elif 0 < self.creation_cooldown_counter < self.cool_down:
			self.creation_cooldown_counter += 1

	def fire(self, window):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and len(self.bullets) > 0 and self.bullet_cooldown_counter == 0:
			bullet = self.bullets.pop(-1)
			bullet.x = self.x + (self.ship_img.get_width() - bullet.img.get_width()) // 2
			bullet.y = self.y - bullet.img.get_height() - 10
			self.fired_bullets.append(bullet)
			self.bullet_cooldown_counter = 1
			self.creation_cooldown_counter = 1

		for bullet in self.fired_bullets:
			bullet.move(-self.bullet_speed)
			bullet.draw(window)

	def hit(self, enemy):
		for bullet in self.fired_bullets[:]:
			if bullet.collision(enemy):
				self.creation_cooldown_counter = int(self.cool_down * 0.8)
				self.fired_bullets.remove(bullet)
				return True
		return False


def main():
	WIDTH, HEIGHT = 800, 600
	pygame.init()
	WIN = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Player Test")
	clock = pygame.time.Clock()

	current_dir = os.path.dirname(__file__)
	player_img = pygame.image.load(os.path.join(current_dir, 'img', 'player_image.png'))
	bullet_img = pygame.image.load(os.path.join(current_dir, 'img', 'bullet_image.png'))

	player_obj = player(
		WIDTH // 2 - player_img.get_width() // 2,
		HEIGHT - player_img.get_height() - 50,
		ship_img=player_img,
		bullet_img=bullet_img,
		x_speed=5,
		y_speed=5,
		bullet_speed=10
	)

	enemies = Enemy(1).create(5) if Enemy else []

	running = True
	while running:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		WIN.fill((0, 0, 0))

		player_obj.move(WIDTH, HEIGHT)
		player_obj.update_cooldowns()
		player_obj.create_bullets()
		player_obj.fire(WIN)

		for enemy in enemies:
			enemy.move()
			enemy.draw(WIN)
			if player_obj.hit(enemy):
				print("Enemy hit!")

		player_obj.draw(WIN)

		pygame.display.update()

	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()
