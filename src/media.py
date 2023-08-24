import pygame
import platformdetect
path = platformdetect.getPath()

pygame.font.init()

def resize(image, width, height):
    return pygame.transform.scale(image, (width, height))

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
DAYSTREAK = pygame.image.load(f"{path}media/daystreak.png")
NODAYSTREAK = pygame.image.load(f"{path}media/nodaystreak.png")


BTN0 = resize(pygame.image.load(f"{path}media/btn0.png"), 80, 80)
BTN1 = resize(pygame.image.load(f"{path}media/btn1.png"), 80, 80)
BTN2 = resize(pygame.image.load(f"{path}media/btn2.png"), 80, 80)
BTN3 = resize(pygame.image.load(f"{path}media/btn3.png"), 80, 80)
BTN4 = resize(pygame.image.load(f"{path}media/btn4.png"), 80, 80)
BTN5 = resize(pygame.image.load(f"{path}media/btn5.png"), 80, 80)
BTN6 = resize(pygame.image.load(f"{path}media/btn6.png"), 80, 80)
BTN7 = resize(pygame.image.load(f"{path}media/btn7.png"), 80, 80)
BTN8 = resize(pygame.image.load(f"{path}media/btn8.png"), 80, 80)
BTN9 = resize(pygame.image.load(f"{path}media/btn9.png"), 80, 80)
BTN10 = resize(pygame.image.load(f"{path}media/btn10.png"), 80, 80)
BTN11 = resize(pygame.image.load(f"{path}media/btn11.png"), 80, 80)
BTN12 = resize(pygame.image.load(f"{path}media/btn12.png"), 80, 80)
BTNANS1 = resize(pygame.image.load(f"{path}media/btnanswer1.png"), 80, 80)
BTNANS2 = resize(pygame.image.load(f"{path}media/btnanswer2.png"), 80, 80)

# Fonts
NORMAL_FONT = pygame.font.Font(f"{path}media/SimplyMono-Bold.ttf", 25)
BIG_FONT = pygame.font.Font(f"{path}media/SimplyMono-Bold.ttf", 70)








