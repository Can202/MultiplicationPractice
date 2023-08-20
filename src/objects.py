import pygame
import constant
import media
import random
import platformdetect
pygame.font.init()

class Node:
    def __init__(self, _position = pygame.Vector2(0, 0), _image =media.IMG_SETTINGS) -> None:
        self.position = _position
        self.image = _image
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.drawing = True
    def update(self, deltaTime):
        self.velocity += self.acceleration * deltaTime
        self.position += self.velocity * deltaTime
    def draw(self, screen):
        if self.drawing:
            screen.blit(self.image, self.position)  

class Button(Node):
    def __init__(self,
                 _position=pygame.Vector2(0, 0),
                 _image=media.BTN,
                 _text = "no text given",
                 _imagehover=media.BTN_HOVER,
                 _imagepressed=media.BTN_PRESSED) -> None:
        super().__init__(_position, _image)
        self.text = Text(_text, _position + pygame.Vector2(25,56))
        self.get_pressed = False
        self.normal_image = self.image
        self.image_hover = _imagehover
        self.image_pressed = _imagepressed
    
    def update(self, deltaTime, mousepressed = False, mouseposX = 0, mouseposY = 0, fix=1, offset=pygame.Vector2(0,0)):
        super().update(deltaTime)
        self.rect = self.image.get_rect()
        self.rect.left += self.position.x
        self.rect.top += self.position.y
        mouse_position_X,mouse_position_Y = mouseposX, mouseposY
        if (self.rect.left < mouse_position_X < self.rect.right) and (self.rect.top < mouse_position_Y < self.rect.bottom):
            if platformdetect.platform() != "android":
                self.image = self.image_hover
            else:
                self.image = self.normal_image
            if mousepressed:
                self.image = self.image_pressed
                self.get_pressed = True
        elif (self.rect.left < mouseposX < self.rect.right) and (self.rect.top < mouseposY < self.rect.bottom):
            if platformdetect.platform() != "android":
                self.image = self.image_hover
            else:
                self.image = self.normal_image
            if mousepressed:
                self.image = self.image_pressed
                self.get_pressed = True
        else:
            self.image = self.normal_image

    
    def draw(self, screen, fix: float = 1, xoffset = 0):
        super().draw(screen)
        self.text.draw(screen)

class Text():
    def __init__(self, 
        _text = "A",
        _position = pygame.Vector2(0,0),
        _color = constant.BLACK,
        _font = media.NORMAL_FONT) -> None:
        self.text = _text
        self.position = _position
        self.font = _font
        self.color = _color

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.position)
            

class Timer:
    def __init__(self, _count_to) -> None:
        self.time = 0
        self.timing = False
        self.count_to = _count_to

    def update(self, deltaTime):
        if self.timing:
            if self.time > self.count_to:
                self.timing = False
                self.time = 0
            self.time += 1 * deltaTime
        else:
            self.time = 0

class Multiplication:
    def __init__(self, max) -> None:
        self.MAX = max
        self.firstFactor = random.randint(1,max)
        self.secondFactor = random.randint(1,max)
    def getTuple(self):
        return (self.firstFactor, self.secondFactor)
    def newSet(self, posiblenumbers = [2,3,4,5,6,7,8,9,10], max = 12, factor = 0):
        if factor == 0:
            self.firstFactor = random.choice(posiblenumbers)
        else:
            self.firstFactor = factor
        self.secondFactor = random.randint(1,max)
    def getStr(self, _form = "product"):
        if _form == "product":
            return f"{self.firstFactor * self.secondFactor}"
        else:
            return f"{self.firstFactor} x {self.secondFactor}"