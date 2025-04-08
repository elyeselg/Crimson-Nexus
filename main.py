import pygame
from ui.menu import run_menu



pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/music/menu_theme.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Crimson Nexus – Menu")

run_menu(screen)
