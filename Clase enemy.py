import pygame
import random
import os
from Shipclass import Ship

current_dir = os.path.dirname(__file__)
BULLET_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'bullet_image.png'))
ENEMY_BLUE_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'enemy_blue_image.png'))
ENEMY_GREEN_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'enemy_green_image.png'))
ENEMY_PURPLE_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'enemy_purple_image.png'))
SHOT_BLUE_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'shot_blue.png'))
SHOT_GREEN_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'shot_green.png'))
SHOT_PURPLE_IMAGE = pygame.image.load(os.path.join(current_dir, 'img', 'shot_purple.png'))

WIDTH, HEIGHT = 800, 600
#===================================
class Enemy(Ship):
    COLOR = {
        'blue': (ENEMY_BLUE_IMAGE, SHOT_BLUE_IMAGE),
        'green': (ENEMY_GREEN_IMAGE, SHOT_GREEN_IMAGE),
        'purple': (ENEMY_PURPLE_IMAGE, SHOT_PURPLE_IMAGE)
    }

    def __init__(self, speed, x=50, y=50, color='blue', health=100):
        super().__init__(x, y, health)
        self.ship_img, self.bullet_img = self.COLOR[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.speed = speed

    def move(self):
        self.y += self.speed

    def increase_speed(self):
        self.speed *= 1.02

    def create(self, amount):
        enemies = []
        for i in range(amount):
            enemy = Enemy(x=random.randrange(20, WIDTH - ENEMY_BLUE_IMAGE.get_width() - 20),
                          y=random.randrange(-1000, -100),
                          color=random.choice(['blue', 'green', 'purple']),
                          speed=self.speed)
            enemies.append(enemy)
        return enemies


def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()

    # Crea una lista de enemigos usando el método create() de Enemy
    enemy_creator = Enemy(speed=2)
    enemies = enemy_creator.create(10)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for enemy in enemies:
            enemy.move()

        window.fill((0, 0, 0))
        for enemy in enemies:
            enemy.draw(window)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
