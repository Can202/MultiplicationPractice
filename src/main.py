import pygame
import constant
import media
import objects
import random
import sound
import platformdetect

pygame.init()

class Game:
    def __init__(self) -> None:

        self.window = pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.RESIZABLE)
        
        pygame.display.set_caption("Game")

        self.clock = pygame.time.Clock()
        self.running = True

        self.mouseposX = 0
        self.mouseposY = 0
        self.realmouseposX = 0
        self.realmouseposY = 0

        self.deltaTime = 0

        self.xoffset = 0
        self.offset = pygame.Vector2(0, 0)
        self.fix = 1
        self.mousepressed = False

        self.mainGame = GameLogic(False)
        self.mainMenu = Menu()
        self.settingsMenu = ConfigurationMenu(False)

        self.sound_channel = pygame.mixer.Channel(2)
        self.musicallowed = True
        self.hardmode = False





    def mainloop(self):
        while self.running:
            self.mousepressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousepressed = True
                    self.realmouseposX, self.realmouseposY = event.pos
                    self.mouseposX = (self.realmouseposX - self.offset.x) / self.fix
                    self.mouseposY = (self.realmouseposY - self.offset.y) / self.fix
                    pygame.mouse.get_rel()
                elif platformdetect.platform() != "android":
                    self.realmouseposX, self.realmouseposY = pygame.mouse.get_pos()
                    self.mouseposX = (self.realmouseposX - self.offset.x) / self.fix
                    self.mouseposY = (self.realmouseposY - self.offset.y) / self.fix
                #if event.type == pygame.MOUSEBUTTONUP:
                #    self.mousepressed = False
            self.keys = pygame.key.get_pressed()

            if self.sound_channel.get_busy() == False and self.musicallowed:
                self.sound_channel.play(sound.SONG)
            
            if self.musicallowed == False:
                self.sound_channel.stop()
                
            if self.mainGame.running:
                self.mainGame.mainloop(self.fix, self.offset,
                                    self.deltaTime,
                                    self.mouseposX, self.mouseposY,
                                    self.mousepressed, self.hardmode)
            if self.mainMenu.running:
                self.mainMenu.mainloop(self.fix, self.offset,
                                    self.deltaTime,
                                    self.mouseposX, self.mouseposY,
                                    self.mousepressed)
            if self.settingsMenu.running:
                self.settingsMenu.mainloop(self.fix, self.offset,
                                    self.deltaTime,
                                    self.mouseposX, self.mouseposY,
                                    self.mousepressed)
            
            if self.mainMenu.playbtn.get_pressed:
                self.mainMenu.playbtn.get_pressed = False
                self.mainMenu.running = False
                self.mainGame.running = True
                self.mainGame.goods = 0
            elif self.mainGame.quitbtn.get_pressed:
                self.mainGame.quitbtn.get_pressed = False
                self.mainGame.goods = 0
                self.mainMenu.running = True
                self.mainGame.running = False
                self.mainMenu.quitTime.timing = True
            elif self.mainMenu.quitbtn.get_pressed:
                if self.mainMenu.quitTime.timing == False:
                    self.running = False
                self.mainMenu.quitbtn.get_pressed = False

            elif self.mainMenu.settingsbtn.get_pressed:
                self.mainMenu.running = False
                self.mainMenu.settingsbtn.get_pressed = False
                self.settingsMenu.running = True
            elif self.settingsMenu.quitbtn.get_pressed:
                self.mainMenu.running = True
                self.settingsMenu.quitbtn.get_pressed = False
                self.settingsMenu.running = False

            '''
            if self.mainMenu.hardbtn.get_pressed:
                self.mainMenu.hardbtn.get_pressed = False
                if self.mainMenu.hardbtntime.timing == False:
                    self.mainMenu.hardbtntime.timing = True
                    if self.hardmode:
                        self.hardmode = False
                        self.mainMenu.hardmode.image = media.resize(media.ERROR,40,40)
                    else:
                        self.hardmode = True
                        self.mainMenu.hardmode.image = media.resize(media.TICKET,40,40)
            if self.mainMenu.musicbtn.get_pressed:
                self.mainMenu.musicbtn.get_pressed = False
                if self.mainMenu.musicbtntime.timing == False:
                    self.mainMenu.musicbtntime.timing = True
                    if self.musicallowed:
                        self.musicallowed = False
                        self.mainMenu.musicmode.image = media.resize(media.ERROR,40,40)
                    else:
                        self.musicallowed = True
                        self.mainMenu.musicmode.image = media.resize(media.TICKET,40,40)
            '''

            self.screenfix()
            self.deltaTime = self.clock.tick(60) / 1000.0


            self.window.fill((0, 0, 0))
            if self.mainGame.running:
                self.window.blit(pygame.transform.scale(
                    self.mainGame.screen, (int(constant.WIDTH*self.fix), int(constant.HEIGHT*self.fix))), 
                    self.offset)
            if self.mainMenu.running:
                self.window.blit(pygame.transform.scale(
                    self.mainMenu.screen, (int(constant.WIDTH*self.fix), int(constant.HEIGHT*self.fix))), 
                    self.offset)
            if self.settingsMenu.running:
                self.window.blit(pygame.transform.scale(
                    self.settingsMenu.screen, (int(constant.WIDTH*self.fix), int(constant.HEIGHT*self.fix))), 
                    self.offset)

            pygame.display.update()
    
    def screenfix(self):
        height = self.window.get_height()
        width = self.window.get_width()
        if (height / 9) <= (width/16):
            self.fix = (height / constant.HEIGHT)
            self.offset.x = (width - (constant.WIDTH * self.fix)) / 2
            self.offset.y = 0
        else:
            self.fix = (width / constant.WIDTH)
            self.offset.x = 0
            self.offset.y = (height - (constant.HEIGHT * self.fix)) / 2

class GameLogic:
    def __init__(self, _running=True) -> None:

        self.running = _running
        
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.correctanswer = objects.Text("12 x 12",pygame.Vector2((constant.WIDTH - 250)/2, (constant.HEIGHT-40)/2), constant.WHITE, media.BIG_FONT)
        self.background = objects.Node(pygame.Vector2(0,0), media.BACKGROUND)
        self.numberlist = [1,2,3,4,5,6,7,8,9,10,11,12]
        self.maxnumber = 12

        self.btn1 = objects.Button(pygame.Vector2(20,200), _text="As")
        self.btn2 = objects.Button(pygame.Vector2(950,200), _text="As2")
        self.btn3 = objects.Button(pygame.Vector2(20,500), _text="As3")
        self.btn4 = objects.Button(pygame.Vector2(950,500), _text="As4")
        



        self.shuffle = True
        self.correctbtnnumber = random.randint(1,4)
        self.correctbtn = objects.Multiplication(10)

        self.otherbtn1 = objects.Multiplication(10)
        self.otherbtn2 = objects.Multiplication(10)
        self.otherbtn3 = objects.Multiplication(10)

        self.quitbtn = objects.Button(pygame.Vector2(55,70),
                                    media.resize(media.ERROR,40,40), "",
                                    media.resize(media.ERROR,40,40),media.resize(media.ERROR,40,40))
        

        self.goods = 0
        self.goodstext = objects.Text(str(self.goods),
                                      pygame.Vector2(constant.WIDTH-80,20),
                                      constant.WHITE, media.NORMAL_FONT)
        self.good = 0
        self.timegood = objects.Timer(.5)
        self.ticketonScreen = objects.Node(
            pygame.Vector2((constant.WIDTH - media.TICKET.get_width())/2, constant.HEIGHT),
            media.TICKET)
        self.ticketanimation = False

        self.erroronScreen = objects.Node(
            pygame.Vector2((constant.WIDTH - media.ERROR.get_width())/2, constant.HEIGHT),
            media.ERROR)
        self.erroranimation = False

    def mainloop(self, _fix, _offset, _dt, _mpx, _mpy, _mp, _hm):

        self.fix = _fix
        self.offset = _offset
        self.deltaTime = _dt
        self.mouseposX = _mpx
        self.mouseposY = _mpy

        self.mousepressed = _mp 
        self.hardmode = _hm

        self.update()
        self.draw()
    
    def update(self):
        if self.shuffle:
            self.correctbtnnumber = random.randint(1,4)
            self.correctbtn.newSet(self.numberlist, self.maxnumber)
            self.otherbtn1.newSet(self.numberlist, self.maxnumber)
            self.otherbtn2.newSet(self.numberlist, self.maxnumber)
            self.otherbtn3.newSet(self.numberlist, self.maxnumber)
            while self.otherbtn1.getStr() == self.correctbtn.getStr():
                self.otherbtn1.newSet(self.numberlist, self.maxnumber)
            while self.otherbtn2.getStr() == self.correctbtn.getStr():
                self.otherbtn2.newSet(self.numberlist, self.maxnumber)
            while self.otherbtn3.getStr() == self.correctbtn.getStr():
                self.otherbtn3.newSet(self.numberlist, self.maxnumber)
            
            self.correctanswer.text = self.correctbtn.getStr("factor")

            self.shuffle = False


        if self.correctbtnnumber == 1:
            self.btn1.text.text = self.correctbtn.getStr()

            self.btn2.text.text = self.otherbtn1.getStr()
            self.btn3.text.text = self.otherbtn2.getStr()
            self.btn4.text.text = self.otherbtn3.getStr()
        elif self.correctbtnnumber == 2:
            self.btn2.text.text = self.correctbtn.getStr()

            self.btn1.text.text = self.otherbtn1.getStr()
            self.btn3.text.text = self.otherbtn2.getStr()
            self.btn4.text.text = self.otherbtn3.getStr()
        elif self.correctbtnnumber == 3:
            self.btn3.text.text = self.correctbtn.getStr()

            self.btn1.text.text = self.otherbtn1.getStr()
            self.btn2.text.text = self.otherbtn2.getStr()
            self.btn4.text.text = self.otherbtn3.getStr()
        elif self.correctbtnnumber == 4:
            self.btn4.text.text = self.correctbtn.getStr()

            self.btn1.text.text = self.otherbtn1.getStr()
            self.btn2.text.text = self.otherbtn2.getStr()
            self.btn3.text.text = self.otherbtn3.getStr()


        self.background.update(self.deltaTime)
        self.ticketonScreen.update(self.deltaTime)
        self.erroronScreen.update(self.deltaTime)
        self.goodstext.text = str(self.goods)

        self.btn1.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn2.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn3.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn4.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        
        self.quitbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)

        if self.btn1.get_pressed:
            if self.timegood.time == 0:
                if self.correctbtnnumber == 1:
                    self.good = 1
                else:
                    self.good = -1
            self.btn1.get_pressed = False
        elif self.btn2.get_pressed:
            if self.timegood.time == 0:
                if self.correctbtnnumber == 2:
                    self.good = 1
                else:
                    self.good = -1
            self.btn2.get_pressed = False
        elif self.btn3.get_pressed:
            if self.timegood.time == 0:
                if self.correctbtnnumber == 3:
                    self.good = 1
                else:
                    self.good = -1
            self.btn3.get_pressed = False
        elif self.btn4.get_pressed:
            if self.timegood.time == 0:
                if self.correctbtnnumber == 4:
                    self.good = 1
                else:
                    self.good = -1
            self.btn4.get_pressed = False
        
        if self.good == 1:
            sound.GOOD.play()
            self.shuffle = True
            self.timegood.timing = True
            self.goods += 1
            self.good = 0
            self.ticketanimation = True
        elif self.good == -1:
            if self.hardmode:
                self.goods = 0
            sound.BAD.play()
            self.timegood.timing = True
            self.good = 0
            self.erroranimation = True

        if self.ticketanimation:
            if self.timegood.time < .125:
                self.ticketonScreen.position.y -= 3316 * self.deltaTime
            if self.timegood.time > .375:
                self.ticketonScreen.position.y += 3316 * self.deltaTime
        
        if self.erroranimation:
            if self.timegood.time < .125:
                self.erroronScreen.position.y -= 3312*self.deltaTime
            if self.timegood.time > .375:
                self.erroronScreen.position.y += 3312*self.deltaTime
        if self.timegood.timing == False:
            self.ticketonScreen.position.y = constant.HEIGHT
            self.ticketanimation = False
            self.erroronScreen.position.y = constant.HEIGHT
            self.erroranimation = False


        self.timegood.update(self.deltaTime)

    def draw(self):
        self.background.draw(self.screen)
        self.correctanswer.draw(self.screen)
        self.ticketonScreen.draw(self.screen)
        self.erroronScreen.draw(self.screen)
        self.goodstext.draw(self.screen)

        self.btn1.draw(self.screen)
        self.btn2.draw(self.screen)
        self.btn3.draw(self.screen)
        self.btn4.draw(self.screen)

        self.quitbtn.draw(self.screen)

class Menu:
    def __init__(self, _running = True) -> None:
        
        self.running = _running
        
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.menuphoto = objects.Node(pygame.Vector2(300,20),
                                      media.MENU)

        self.background = objects.Node(pygame.Vector2(0,0), media.BACKGROUND)
        self.playbtn = objects.Button(
            pygame.Vector2((constant.WIDTH-310)/2, (constant.HEIGHT+300)/2),
            _text="  touch to play")
        
        self.quitbtn = objects.Button(pygame.Vector2(55,70),
                                    media.resize(media.ERROR,40,40), "",
                                    media.resize(media.ERROR,40,40),media.resize(media.ERROR,40,40))
        self.quitTime = objects.Timer(.3)



        self.settingsbtn = objects.Button(pygame.Vector2(1170,50),
                                    media.resize(media.IMG_SETTINGS,60,60), "",
                                    media.resize(media.IMG_SETTINGS,60,60),media.resize(media.IMG_SETTINGS,60,60))
        self.settingsbtnTime = objects.Timer(.3)

    def mainloop(self, _fix, _offset, _dt, _mpx, _mpy, _mp):

        self.fix = _fix
        self.offset = _offset
        self.deltaTime = _dt
        self.mouseposX = _mpx
        self.mouseposY = _mpy

        self.mousepressed = _mp 

        self.update()
        self.draw()
    
    def update(self):
        self.quitTime.update(self.deltaTime)
        self.settingsbtnTime.update(self.deltaTime)

        self.playbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.quitbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.settingsbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)


    def draw(self):
        self.background.draw(self.screen)
        self.menuphoto.draw(self.screen)
        self.playbtn.draw(self.screen)
        self.quitbtn.draw(self.screen)
        self.settingsbtn.draw(self.screen)


class ConfigurationMenu:
    def __init__(self, _running = True) -> None:
        
        self.running = _running
        
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.background = objects.Node(pygame.Vector2(0,0), media.BACKGROUND)

        self.quitbtn = objects.Button(pygame.Vector2(55,70),
                                    media.resize(media.ERROR,40,40), "",
                                    media.resize(media.ERROR,40,40),media.resize(media.ERROR,40,40))
        self.quitTime = objects.Timer(.3)


        self.musicbtn = objects.Button(pygame.Vector2(1170,70),
                                    media.resize(media.MUSICMODE,80,80), "",
                                    media.resize(media.MUSICMODE,80,80),media.resize(media.MUSICMODE,80,80))
        self.hardbtn = objects.Button(pygame.Vector2(1170,180),
                                    media.resize(media.HARDMODE,80,80), "",
                                    media.resize(media.HARDMODE,80,80),media.resize(media.HARDMODE,80,80))
        self.musicmode = objects.Node(pygame.Vector2(1120,90),media.resize(media.TICKET,40,40))
        self.hardmode = objects.Node(pygame.Vector2(1120,200),media.resize(media.ERROR,40,40))
        self.musicbtntime = objects.Timer(.3)
        self.hardbtntime = objects.Timer(.3)
    def mainloop(self, _fix, _offset, _dt, _mpx, _mpy, _mp):

        self.fix = _fix
        self.offset = _offset
        self.deltaTime = _dt
        self.mouseposX = _mpx
        self.mouseposY = _mpy

        self.mousepressed = _mp 

        self.update()
        self.draw()
    
    def update(self):
        self.quitTime.update(self.deltaTime)
        self.quitbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.hardbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.musicbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.musicbtntime.update(self.deltaTime)
        self.hardbtntime.update(self.deltaTime)

    def draw(self):
        self.background.draw(self.screen)
        self.quitbtn.draw(self.screen)
        self.musicbtn.draw(self.screen)
        self.hardbtn.draw(self.screen)
        self.musicmode.draw(self.screen)
        self.hardmode.draw(self.screen)

if __name__ == "__main__":
    game = Game()
    game.mainloop()
