import pygame
import os
import sys
import importlib.util
from Shipclass import Ship

# Importar la clase player
current_dir = os.path.dirname(__file__)
player_spec = importlib.util.spec_from_file_location(
    "clase_player",
    os.path.join(current_dir, "clase_player.py")
)
clase_player = importlib.util.module_from_spec(player_spec)
player_spec.loader.exec_module(clase_player)
PlayerClass = clase_player.player

pygame.init()
pygame.mixer.init()

spec = importlib.util.spec_from_file_location(
    "clase_enemy",
    os.path.join(current_dir, "Clase_enemy.py")
)
clase_enemy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clase_enemy)
Enemy = clase_enemy.Enemy
BACKGROUND_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'background.png'))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (800, 600))
PLAYER_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'player_image.png'))
BULLET_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'bullet_image.png'))
ENEMY_BLUE_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'enemy_blue_image.png'))
ENEMY_GREEN_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'enemy_green_image.png'))
ENEMY_PURPLE_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'enemy_purple_image.png'))
SHOT_BLUE_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'shot_blue.png'))
SHOT_GREEN_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'shot_green.png'))
SHOT_PURPLE_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'shot_purple.png'))
class Game:
    def __init__(self, font, FPS, lives, window, screen_width, screen_height, bullets=0, clock=pygame.time.Clock()):
        self.font = font
        self.HEIGHT = screen_height
        self.WIDTH = screen_width
        self.FPS = FPS
        self.lives = lives
        self.level = 1
        self.count = 0
        self.window = window
        self.clock = clock
        self.bullets = bullets
        self.bullet_img = BULLET_IMAGE
    
    def escape (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        else:
            return False
    
    def over(self):
        if self.lives <= 0:
            lost_label = self.font.render("GAME OVER!", 1, (255, 61, 103))
            self.window.blit(lost_label, (int((self.WIDTH - lost_label.get_width()) / 2), int((self.HEIGHT - lost_label.get_height()) / 2)))
            return True
        else:
            return False
        
    def reload_bullets(self, bulllet):
        self.bullets = bulllet
    
    def draw_HUD(self):
        offset = 0
        lives_label =self.font.render(f'Lives: {self.lives}', 1, (18, 222, 200))
        level_label = self.font.render(f'Level: {self. level}', 1, (255, 255, 255))
        self.window.blit(level_label, (10, 10))
        self.window.blit(lives_label, (self.WIDTH - lives_label.get_width() - 10, 10))
        for i in range(self.bullets):
            offset += self.bullet_img.get_width()
            self.window.blit(self.bullet_img, (self.WIDTH - offset, self.HEIGHT - 50))
    
    def reload_bullet(self, bullet):
        self.bullets = bullet

#====================MAIN====================#
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
font = pygame.font.Font(None, 30)
game = Game(font=font, FPS=60, lives=3, window=window,
            screen_width=WIDTH, screen_height=HEIGHT, bullets=10)

player = PlayerClass(
    x=WIDTH // 2 - PLAYER_IMAGE.get_width() // 2,
    y=HEIGHT - 100,
    ship_img=PLAYER_IMAGE,
    bullet_img=BULLET_IMAGE,
    x_speed=5,
    y_speed=5,
    bullet_speed=10,
    health=100
)
player.mask = pygame.mask.from_surface(player.ship_img)

enemy_creator = Enemy(speed=2)
enemies = enemy_creator.create(10)

# Carga dinámica de la clase Drawing desde 'clase drawing.py' y la instancia
drawing = None
try:
    drawing_spec = importlib.util.spec_from_file_location("clase_drawing", os.path.join(current_dir, "clase drawing.py"))
    if drawing_spec and drawing_spec.loader:
        clase_drawing = importlib.util.module_from_spec(drawing_spec)
        drawing_spec.loader.exec_module(clase_drawing)
        Drawing = getattr(clase_drawing, "Drawing", None)
        if Drawing:
            drawing = Drawing(window)
except Exception:
    drawing = None

music_path = os.path.join(current_dir, 'music.mp3')
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)


def update_HUD():
    game.draw_HUD()
    pygame.display.update()

running = True
has_game_over = False
while running:
    game.clock.tick(game.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not has_game_over:
        player.move(WIDTH, HEIGHT)
        player.create_bullets()
        player.update_cooldowns()
    
    # Sincronizar el contador de balas del HUD con las balas disponibles del jugador
    game.bullets = len(player.bullets)

    if drawing and hasattr(drawing, 'draw_background'):
        drawing.draw_background()
    else:
        window.blit(BACKGROUND_IMAGE, (0, 0))
    player.draw(window)

    for enemy in enemies:
        if not has_game_over:
            enemy.move()
        enemy.draw(window)
        
        # Verificar colisión entre balas y enemigos
        if player.hit(enemy):
            if enemy in enemies:
                enemies.remove(enemy)
                print("¡Enemigo destruido!")
        
        offset = (int(enemy.x - player.x), int(enemy.y - player.y))
        if not has_game_over and enemy.mask.overlap(player.mask, offset):
            game.lives = 0
            has_game_over = True
            print("GAME OVER: El enemigo tocó a la nave")

    # Dibujar las balas al final para que aparezcan encima de todo
    if not has_game_over:
        player.fire(window)

    if game.over():
        has_game_over = True

    update_HUD()

pygame.quit()
sys.exit()  
