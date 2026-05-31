import pygame
import os
import importlib.util

# Intento importar una clase Game desde GameClass.py si existe (seguro)
Game = None
try:
	current_dir = os.path.dirname(__file__)
	game_spec = importlib.util.spec_from_file_location("GameClass", os.path.join(current_dir, "GameClass.py"))
	if game_spec and game_spec.loader:
		game_mod = importlib.util.module_from_spec(game_spec)
		game_spec.loader.exec_module(game_mod)
		Game = getattr(game_mod, "Game", None)
except Exception:
	Game = None

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

# Importa la clase Ship desde 'clase Ship.py' de forma segura
Ship = None
try:
	current_dir = os.path.dirname(__file__)
	ship_spec = importlib.util.spec_from_file_location("clase_ship", os.path.join(current_dir, "clase Ship.py"))
	if ship_spec and ship_spec.loader:
		clase_ship = importlib.util.module_from_spec(ship_spec)
		ship_spec.loader.exec_module(clase_ship)
		Ship = getattr(clase_ship, "Ship", None)
except Exception:
	Ship = None

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

current_dir = os.path.dirname(__file__)
BACKGROUND = pygame.image.load(os.path.join(current_dir, 'img', 'background.png'))
PLAYER_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'player_image.png'))
BULLET_IMAGE = pygame.Surface((5, 20))
BULLET_IMAGE.fill((255, 255, 255))

WIDTH, HEIGHT = 800, 600


class Drawing:
	def __init__(self, window):
		self.window = window
		self.background = BACKGROUND

	def draw_background(self):
		if self.background and self.window:
			self.window.blit(self.background, (0, 0))

	def drawing(self, game, player, enemies, FPS):
		# Drawing the background
		self.window.blit(BACKGROUND, (0, 0))

		for enemy in enemies[:]:
			enemy.draw(self.window)
		
		game.draw_HUD()

		pygame.display.update()


def main():
	pygame.init()
	WIN = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Space Invaders")

	run = True
	clock = pygame.time.Clock()

	drawing = Drawing(WIN)
	enemies = Enemy(1).create(5) if Enemy else []
	game = None
	if Game:
		game = Game(pygame.font.SysFont('comicsans', 30), 60, 3, WIN, WIDTH, HEIGHT, 4)

	player = None
	if Ship:
		player = Ship(WIDTH // 2 - PLAYER_IMAGE.get_width() // 2, HEIGHT - 100, 100)
		player.ship_img = PLAYER_IMAGE
		player.mask = pygame.mask.from_surface(player.ship_img)

	bullet_example = None
	if Bullet:
		bullet_example = Bullet(400, 300, BULLET_IMAGE)

	# Ejemplo de uso de los objetos creados
	while run:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for enemy in enemies:
			enemy.move()

		if drawing and game is not None and player is not None:
			drawing.drawing(game, player, enemies, 60)
		else:
			# Fallback si no hay game o player
			if drawing:
				drawing.draw_background()
				for enemy in enemies:
					enemy.draw(WIN)
				pygame.display.update()

		if bullet_example:
			bullet_example.draw(WIN)

		pygame.display.update()

	pygame.quit()


if __name__ == '__main__':
	main()


# Crear instancias de las clases disponibles
drawing_instance = None
enemy_instance = None
game_instance = None
bullet_instance = None

try:
	pygame.init()
	window = pygame.display.set_mode((800, 600))
	drawing_instance = Drawing(window)

	if Enemy:
		enemy_instance = Enemy(speed=2)

	if Game:
		font = pygame.font.Font(None, 30)
		game_instance = Game(font=font, FPS=60, lives=3, window=window,
					 screen_width=800, screen_height=600, bullets=10)

	if Bullet:
		bullet_surface = pygame.Surface((5, 20))
		bullet_surface.fill((255, 255, 255))
		bullet_instance = Bullet(0, 0, bullet_surface)
except Exception:
	drawing_instance = drawing_instance


