import pygame
import os
import sys
from Shipclass import Ship

pygame.init()

BULLET_IMAGE = pygame.image.load(os.path.join('img', 'BULLET_IMAGE.png'))
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
            self.count = 0
            while True:
                self.clock.tick(self.FPS)
                lost_label = self.font.render("GAME OVER!", 1, (255, 61, 103))
                self.window.blit(lost_label, (self.WIDTH - lost_label.get_width()) /2, (self.HEIGHT - lost_label.get_height()) /2)

                pygame.display.update()
                self.count += 1
                if self.count > self.FPS * 3:
                    break
            return True
        else:
            return False
        
    def reload_bullets(self, bulllet):
        self.bullets = Bullet
    
    def draw_HUD(self):
        offset = 0
        lives_label =self.font.render(f'Lives: {self.lives}', 1, (18, 222, 200))
        level_label = self.font.render(f'Level: {self. level}', 1, (255, 255, 255))
        self.window.blit(level_label, (10, 10))
        self.window.blit(lives_label, (self.WIDTH - lives_label.get_width() - 10, 10))
        for i in range(self.bullets):
            offset += self.bullet_img.get_width()
            self.window.blit(self.bullet_img, (self.WIDTH - offset, self.HEIGHT - 50))

#====================MAIN====================#
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
font = pygame.font.Font(os.path.join('sprite', 'halo.ttf'), 30)
game = Game(font=font, FPS=60, lives=3, window=window,
            screen_width=WIDTH, screen_height=HEIGHT, bullets=10)

def update_HUD():
    game.draw_HUD()
    pygame.display.update()

running = True
while running:
    game.clock.tick(game.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if game.bullets > 0:
            game.bullets -= 1
            print(" QUEDAN {} BALAS".format(game.bullets))
        else:
            print("###NO QUEDAN BALAS###")
    
    window.fill((0, 0, 0))
    update_HUD()

    if game.over():
        running = False

    if game.escape():
        running = False 

pygame.quit()
sys.exit()  
