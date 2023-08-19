import pygame
import platformdetect
path = platformdetect.getPath()

pygame.font.init()


# Images
BACKGROUND = pygame.image.load(f"{path}media/Background.png")
IMG_SETTINGS = pygame.image.load(f"{path}media/settings.png")
BTN = pygame.image.load(f"{path}media/btn.png")
BTN_HOVER = pygame.image.load(f"{path}media/btnhover.png")
BTN_PRESSED = pygame.image.load(f"{path}media/btnpressed.png")
TICKET = pygame.image.load(f"{path}media/ticket.png")
ERROR = pygame.image.load(f"{path}media/error.png")
HARDMODE = pygame.image.load(f"{path}media/hard.png")
MUSICMODE = pygame.image.load(f"{path}media/music.png")
BLANK = pygame.image.load(f"{path}media/blank.png")
MENU = pygame.image.load(f"{path}media/menu.png")

# Fonts
NORMAL_FONT = pygame.font.Font(f"{path}media/SimplyMono-Bold.ttf", 25)
BIG_FONT = pygame.font.Font(f"{path}media/SimplyMono-Bold.ttf", 70)









def resize(image, width, height):
    return pygame.transform.scale(image, (width, height))