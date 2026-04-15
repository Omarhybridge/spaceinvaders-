import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Ejemplo de Pygame Mixer")

pygame.mixer.music.load("09 The Swagga.mp3")
pygame.mixer.music.play(-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((158, 158, 226))

    pygame.display.flip()

pygame.quit()
sys.exit()