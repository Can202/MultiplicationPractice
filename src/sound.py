import pygame
import platformdetect
path = platformdetect.getPath()

pygame.mixer.init()

BAD = pygame.mixer.Sound(f"{path}media/bad.mp3")
GOOD = pygame.mixer.Sound(f"{path}media/good.mp3")

SONG = pygame.mixer.Sound(f"{path}media/song.mp3")