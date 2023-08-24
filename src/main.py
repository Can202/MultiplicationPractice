import pygame
import constant
import media
import objects
import random
import os
import sound
import platformdetect
import datetime

pygame.init()

class Game:
    def __init__(self) -> None:

        self.window = pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.FULLSCREEN)
        
        pygame.display.set_caption("Game")

        self.clock = pygame.time.Clock()
        self.running = True


        self.current_date = datetime.date.today()
        self.yesterday_date = self.current_date - datetime.timedelta(days=1)
        self.daystreak = 0
        self.daystreak_goal = 10
        self.profile = ""
        self.profiles = [None]
        self.getProfile()
        self.writeProfile()

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
        self.mainMenu = Menu(True, self.profile)
        self.settingsMenu = ConfigurationMenu(False, self.profile)

        self.sound_channel = pygame.mixer.Channel(2)
        self.musicallowed = True
        self.hardmode = False


        self.mainGame.numberlist = None
        self.mainGame.numberlist = self.settingsMenu.returnlistfromnumbers()
        self.musicallowed, self.hardmode, self.mainGame.maxnumber, self.typeanswer = self.settingsMenu.returnvalues()





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
                if event.type == pygame.KEYDOWN:
                    if self.typeanswer == "write":
                        if len(self.mainGame.typenumber) < 11:
                            if event.key == pygame.K_0 or event.key == pygame.K_KP_0:
                                if self.mainGame.typenumber != "":
                                    self.mainGame.typenumber += "0"
                            if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                                self.mainGame.typenumber += "1"
                            if event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                                self.mainGame.typenumber += "2"
                            if event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                                self.mainGame.typenumber += "3"
                            if event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                                self.mainGame.typenumber += "4"
                            if event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                                self.mainGame.typenumber += "5"
                            if event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                                self.mainGame.typenumber += "6"
                            if event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                                self.mainGame.typenumber += "7"
                            if event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                                self.mainGame.typenumber += "8"
                            if event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                                self.mainGame.typenumber += "9"
                        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                            self.mainGame.typesend.get_pressed = True
                        if event.key == pygame.K_BACKSPACE:
                            self.mainGame.typeerase.get_pressed = True
                    if event.key == pygame.K_RETURN and self.mainMenu.running:
                        self.mainMenu.playbtn.get_pressed = True
                    if event.key == pygame.K_ESCAPE and self.mainMenu.running:
                        self.mainMenu.quitbtn.get_pressed = True
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
            
            if self.mainMenu.Profilebtn.get_pressed:
                self.mainMenu.Profilebtn.get_pressed = False
                self.changeProfile()


            if self.mainMenu.playbtn.get_pressed:
                self.mainMenu.playbtn.get_pressed = False
                self.mainMenu.running = False
                self.mainGame.running = True
                self.mainGame.shuffle = True
                self.mainGame.typenumber = ""
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
                self.settingsMenu.quitbtn.get_pressed = False
                self.mainGame.numberlist = None
                self.updateListConfig()
                if self.mainGame.numberlist:

                    self.updateConfig()

                    self.settingsMenu.writeData()

                    self.mainMenu.running = True
                    self.settingsMenu.running = False
            self.updateTypeAnswer()
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
    
    def updateConfig(self):
        self.musicallowed, self.hardmode, self.mainGame.maxnumber, self.typeanswer = self.settingsMenu.returnvalues()
    def updateListConfig(self):
        self.mainGame.numberlist = self.settingsMenu.returnlistfromnumbers()


    def updateTypeAnswer(self):
        if self.typeanswer == "multipleanswer":
            self.mainGame.btn1.working, self.mainGame.btn1.drawing = True, True
            self.mainGame.btn2.working, self.mainGame.btn2.drawing = True, True
            self.mainGame.btn3.working, self.mainGame.btn3.drawing = True, True
            self.mainGame.btn4.working, self.mainGame.btn4.drawing = True, True
            self.mainGame.typebtn0.working, self.mainGame.typebtn0.drawing = False, False
            self.mainGame.typebtn1.working, self.mainGame.typebtn1.drawing = False, False
            self.mainGame.typebtn2.working, self.mainGame.typebtn2.drawing = False, False
            self.mainGame.typebtn3.working, self.mainGame.typebtn3.drawing = False, False
            self.mainGame.typebtn4.working, self.mainGame.typebtn4.drawing = False, False
            self.mainGame.typebtn5.working, self.mainGame.typebtn5.drawing = False, False
            self.mainGame.typebtn6.working, self.mainGame.typebtn6.drawing = False, False
            self.mainGame.typebtn7.working, self.mainGame.typebtn7.drawing = False, False
            self.mainGame.typebtn8.working, self.mainGame.typebtn8.drawing = False, False
            self.mainGame.typebtn9.working, self.mainGame.typebtn9.drawing = False, False
            self.mainGame.typesend.working, self.mainGame.typesend.drawing = False, False
            self.mainGame.typeerase.working, self.mainGame.typeerase.drawing = False, False
            self.mainGame.Rtypebtn0.working, self.mainGame.Rtypebtn0.drawing = False, False
            self.mainGame.Rtypebtn1.working, self.mainGame.Rtypebtn1.drawing = False, False
            self.mainGame.Rtypebtn2.working, self.mainGame.Rtypebtn2.drawing = False, False
            self.mainGame.Rtypebtn3.working, self.mainGame.Rtypebtn3.drawing = False, False
            self.mainGame.Rtypebtn4.working, self.mainGame.Rtypebtn4.drawing = False, False
            self.mainGame.Rtypebtn5.working, self.mainGame.Rtypebtn5.drawing = False, False
            self.mainGame.Rtypebtn6.working, self.mainGame.Rtypebtn6.drawing = False, False
            self.mainGame.Rtypebtn7.working, self.mainGame.Rtypebtn7.drawing = False, False
            self.mainGame.Rtypebtn8.working, self.mainGame.Rtypebtn8.drawing = False, False
            self.mainGame.Rtypebtn9.working, self.mainGame.Rtypebtn9.drawing = False, False
            self.mainGame.Rtypesend.working, self.mainGame.Rtypesend.drawing = False, False
            self.mainGame.Rtypeerase.working, self.mainGame.Rtypeerase.drawing = False, False
            self.mainGame.typetextBlank.drawing = False
            self.mainGame.typetext.drawing = False
        elif self.typeanswer == "write":
            self.mainGame.btn1.working, self.mainGame.btn1.drawing = False, False
            self.mainGame.btn2.working, self.mainGame.btn2.drawing = False, False
            self.mainGame.btn3.working, self.mainGame.btn3.drawing = False, False
            self.mainGame.btn4.working, self.mainGame.btn4.drawing = False, False
            self.mainGame.typebtn0.working, self.mainGame.typebtn0.drawing = True, True
            self.mainGame.typebtn1.working, self.mainGame.typebtn1.drawing = True, True
            self.mainGame.typebtn2.working, self.mainGame.typebtn2.drawing = True, True
            self.mainGame.typebtn3.working, self.mainGame.typebtn3.drawing = True, True
            self.mainGame.typebtn4.working, self.mainGame.typebtn4.drawing = True, True
            self.mainGame.typebtn5.working, self.mainGame.typebtn5.drawing = True, True
            self.mainGame.typebtn6.working, self.mainGame.typebtn6.drawing = True, True
            self.mainGame.typebtn7.working, self.mainGame.typebtn7.drawing = True, True
            self.mainGame.typebtn8.working, self.mainGame.typebtn8.drawing = True, True
            self.mainGame.typebtn9.working, self.mainGame.typebtn9.drawing = True, True
            self.mainGame.typesend.working, self.mainGame.typesend.drawing = True, True
            self.mainGame.typeerase.working, self.mainGame.typeerase.drawing = True, True
            self.mainGame.Rtypebtn0.working, self.mainGame.Rtypebtn0.drawing = True, True
            self.mainGame.Rtypebtn1.working, self.mainGame.Rtypebtn1.drawing = True, True
            self.mainGame.Rtypebtn2.working, self.mainGame.Rtypebtn2.drawing = True, True
            self.mainGame.Rtypebtn3.working, self.mainGame.Rtypebtn3.drawing = True, True
            self.mainGame.Rtypebtn4.working, self.mainGame.Rtypebtn4.drawing = True, True
            self.mainGame.Rtypebtn5.working, self.mainGame.Rtypebtn5.drawing = True, True
            self.mainGame.Rtypebtn6.working, self.mainGame.Rtypebtn6.drawing = True, True
            self.mainGame.Rtypebtn7.working, self.mainGame.Rtypebtn7.drawing = True, True
            self.mainGame.Rtypebtn8.working, self.mainGame.Rtypebtn8.drawing = True, True
            self.mainGame.Rtypebtn9.working, self.mainGame.Rtypebtn9.drawing = True, True
            self.mainGame.Rtypesend.working, self.mainGame.Rtypesend.drawing = True, True
            self.mainGame.Rtypeerase.working, self.mainGame.Rtypeerase.drawing = True, True
            self.mainGame.typetextBlank.drawing = True
            self.mainGame.typetext.drawing = True
    
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

    def getProfile(self):
        if os.path.exists(f"{platformdetect.getSavePath()}media/profiles.dat"):
            jsonfile = platformdetect.readFile(f"{platformdetect.getSavePath()}media/profiles.dat")

            self.profile = platformdetect.getjsondataifexists("User", jsonfile, "current_profile")
            self.profiles = platformdetect.getjsondataifexists(self.profiles, jsonfile, "profiles")
        else:
            self.profile = "User"
            self.profiles = ["User"]
    def writeProfile(self):
        data = {}
        data["current_profile"] = self.profile
        data["profiles"] = self.profiles
        platformdetect.writeFile(f"{platformdetect.getSavePath()}media/profiles.dat", data)
    
    def changeProfile(self):
        index = self.profiles.index(self.profile) + 1
        if index == len(self.profiles):
            index = 0
        self.profile = self.profiles[index]
        self.writeProfile()
        self.mainMenu.profile = self.profile
        self.settingsMenu.profile = self.profile
        self.settingsMenu.readData()
        self.mainMenu.Profilebtn.text.text = self.profile

        self.updateListConfig()
        self.updateConfig()
        self.updateTypeAnswer()

        print(f"Change to {self.profile}")
        





class GameLogic:
    def __init__(self, _running=True) -> None:

        self.running = _running
        
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.correctanswer = objects.Text("12 x 12",pygame.Vector2((constant.WIDTH - 250)/2, (constant.HEIGHT-90)/2), constant.WHITE, media.BIG_FONT)
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
            pygame.Vector2((constant.WIDTH - media.TICKET.get_width())/2, (constant.HEIGHT - media.TICKET.get_height())/2),
            media.TICKET)
        self.ticketanimation = False

        self.erroronScreen = objects.Node(
            pygame.Vector2((constant.WIDTH - media.ERROR.get_width())/2, (constant.HEIGHT - media.ERROR.get_height())/2), 
        media.ERROR)
        self.erroranimation = False


        # Typed numbers
        self.typebtn0 = objects.Button(pygame.Vector2(220,500), media.BTN0, "", media.BTN0, media.BTN0)
        self.typebtn1 = objects.Button(pygame.Vector2(120,400), media.BTN1, "", media.BTN1, media.BTN1)
        self.typebtn2 = objects.Button(pygame.Vector2(220,400), media.BTN2, "", media.BTN2, media.BTN2)
        self.typebtn3 = objects.Button(pygame.Vector2(320,400), media.BTN3, "", media.BTN3, media.BTN3)
        self.typebtn4 = objects.Button(pygame.Vector2(120,300), media.BTN4, "", media.BTN4, media.BTN4)
        self.typebtn5 = objects.Button(pygame.Vector2(220,300), media.BTN5, "", media.BTN5, media.BTN5)
        self.typebtn6 = objects.Button(pygame.Vector2(320,300), media.BTN6, "", media.BTN6, media.BTN6)
        self.typebtn7 = objects.Button(pygame.Vector2(120,200), media.BTN7, "", media.BTN7, media.BTN7)
        self.typebtn8 = objects.Button(pygame.Vector2(220,200), media.BTN8, "", media.BTN8, media.BTN8)
        self.typebtn9 = objects.Button(pygame.Vector2(320,200), media.BTN9, "", media.BTN9, media.BTN9)

        self.typesend = objects.Button(pygame.Vector2(120,500), media.resize(media.TICKET, 80, 80), "", media.resize(media.TICKET, 80, 80), media.resize(media.TICKET, 80, 80))
        self.typeerase = objects.Button(pygame.Vector2(320,500), media.resize(media.ERROR, 80, 80), "", media.resize(media.ERROR, 80, 80), media.resize(media.ERROR, 80, 80))

        self.typetextBlank = objects.Node((530, 80), media.resize(media.BLANK, 200, 45))
        self.typetext = objects.Text("9", (550, 85), constant.BLACK, media.NORMAL_FONT)
        self.typenumber = ""

        self.Rtypebtn0 = objects.Button(pygame.Vector2(970,500), media.BTN0, "", media.BTN0, media.BTN0)
        self.Rtypebtn1 = objects.Button(pygame.Vector2(870,400), media.BTN1, "", media.BTN1, media.BTN1)
        self.Rtypebtn2 = objects.Button(pygame.Vector2(970,400), media.BTN2, "", media.BTN2, media.BTN2)
        self.Rtypebtn3 = objects.Button(pygame.Vector2(1070,400), media.BTN3, "", media.BTN3, media.BTN3)
        self.Rtypebtn4 = objects.Button(pygame.Vector2(870,300), media.BTN4, "", media.BTN4, media.BTN4)
        self.Rtypebtn5 = objects.Button(pygame.Vector2(970,300), media.BTN5, "", media.BTN5, media.BTN5)
        self.Rtypebtn6 = objects.Button(pygame.Vector2(1070,300), media.BTN6, "", media.BTN6, media.BTN6)
        self.Rtypebtn7 = objects.Button(pygame.Vector2(870,200), media.BTN7, "", media.BTN7, media.BTN7)
        self.Rtypebtn8 = objects.Button(pygame.Vector2(970,200), media.BTN8, "", media.BTN8, media.BTN8)
        self.Rtypebtn9 = objects.Button(pygame.Vector2(1070,200), media.BTN9, "", media.BTN9, media.BTN9)
        self.Rtypesend = objects.Button(pygame.Vector2(870,500), media.resize(media.TICKET, 80, 80), "", media.resize(media.TICKET, 80, 80), media.resize(media.TICKET, 80, 80))
        self.Rtypeerase = objects.Button(pygame.Vector2(1070,500), media.resize(media.ERROR, 80, 80), "", media.resize(media.ERROR, 80, 80), media.resize(media.ERROR, 80, 80))



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
        
        self.typebtn0.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn1.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn2.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn3.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn4.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn5.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn6.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn7.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn8.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typebtn9.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typesend.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.typeerase.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)

        self.Rtypebtn0.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn1.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn2.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn3.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn4.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn5.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn6.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn7.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn8.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypebtn9.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypesend.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.Rtypeerase.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)


        self.typetext.text = self.typenumber

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
        

        # Type
        if self.Rtypebtn0.get_pressed:
            self.Rtypebtn0.get_pressed = False
            self.typebtn0.get_pressed = True
        elif self.Rtypebtn1.get_pressed:
            self.Rtypebtn1.get_pressed = False
            self.typebtn1.get_pressed = True
        elif self.Rtypebtn2.get_pressed:
            self.Rtypebtn2.get_pressed = False
            self.typebtn2.get_pressed = True
        elif self.Rtypebtn3.get_pressed:
            self.Rtypebtn3.get_pressed = False
            self.typebtn3.get_pressed = True
        elif self.Rtypebtn4.get_pressed:
            self.Rtypebtn4.get_pressed = False
            self.typebtn4.get_pressed = True
        elif self.Rtypebtn5.get_pressed:
            self.Rtypebtn5.get_pressed = False
            self.typebtn5.get_pressed = True
        elif self.Rtypebtn6.get_pressed:
            self.Rtypebtn6.get_pressed = False
            self.typebtn6.get_pressed = True
        elif self.Rtypebtn7.get_pressed:
            self.Rtypebtn7.get_pressed = False
            self.typebtn7.get_pressed = True
        elif self.Rtypebtn8.get_pressed:
            self.Rtypebtn8.get_pressed = False
            self.typebtn8.get_pressed = True
        elif self.Rtypebtn9.get_pressed:
            self.Rtypebtn9.get_pressed = False
            self.typebtn9.get_pressed = True
        elif self.Rtypesend.get_pressed:
            self.Rtypesend.get_pressed = False
            self.typesend.get_pressed = True
        elif self.Rtypeerase.get_pressed:
            self.Rtypeerase.get_pressed = False
            self.typeerase.get_pressed = True
        if len(self.typenumber) < 11:
            if self.typebtn0.get_pressed:
                self.typebtn0.get_pressed = False
                if self.typenumber != "":
                    self.typenumber += "0"
            elif self.typebtn1.get_pressed:
                self.typebtn1.get_pressed = False
                self.typenumber += "1"
            elif self.typebtn2.get_pressed:
                self.typebtn2.get_pressed = False
                self.typenumber += "2"
            elif self.typebtn3.get_pressed:
                self.typebtn3.get_pressed = False
                self.typenumber += "3"
            elif self.typebtn4.get_pressed:
                self.typebtn4.get_pressed = False
                self.typenumber += "4"
            elif self.typebtn5.get_pressed:
                self.typebtn5.get_pressed = False
                self.typenumber += "5"
            elif self.typebtn6.get_pressed:
                self.typebtn6.get_pressed = False
                self.typenumber += "6"
            elif self.typebtn7.get_pressed:
                self.typebtn7.get_pressed = False
                self.typenumber += "7"
            elif self.typebtn8.get_pressed:
                self.typebtn8.get_pressed = False
                self.typenumber += "8"
            elif self.typebtn9.get_pressed:
                self.typebtn9.get_pressed = False
                self.typenumber += "9"
        if self.typeerase.get_pressed:
            self.typeerase.get_pressed = False
            self.typenumber = ""
        if self.typesend.get_pressed:
            self.typesend.get_pressed = False
            if self.typenumber != "":
                if self.correctbtn.getStr() == self.typenumber:
                    self.good = 1
                else:
                    self.good = -1




        if self.good == 1:
            sound.GOOD.play()
            self.shuffle = True
            self.timegood.timing = True
            self.goods += 1
            self.good = 0
            self.ticketanimation = True
            self.typenumber = ""
        elif self.good == -1:
            if self.hardmode:
                self.goods = 0
            sound.BAD.play()
            self.timegood.timing = True
            self.good = 0
            self.erroranimation = True
            self.typenumber = ""

        if self.ticketanimation:
            if self.timegood.time < .25:
                self.ticketonScreen.image = media.resize(media.TICKET, abs(int(media.TICKET.get_width() * self.timegood.time/0.25)),abs(int(media.TICKET.get_height() * self.timegood.time/0.25)))
                self.ticketonScreen.position = pygame.Vector2((constant.WIDTH - self.ticketonScreen.image.get_width())/2, (constant.HEIGHT - self.ticketonScreen.image.get_height())/2)
            if self.timegood.time > .25:
                temp = .5 - self.timegood.time
                self.ticketonScreen.image = media.resize(media.TICKET, abs(int(media.TICKET.get_width() * temp/0.25)),abs(int(media.TICKET.get_height() * temp/0.25)))
                self.ticketonScreen.position = pygame.Vector2((constant.WIDTH - self.ticketonScreen.image.get_width())/2, (constant.HEIGHT - self.ticketonScreen.image.get_height())/2)

        else:
            self.ticketonScreen.image = media.resize(media.TICKET, 0, 0)
        if self.erroranimation:
            if self.timegood.time < .25:
                self.erroronScreen.image = media.resize(media.ERROR, abs(int(media.ERROR.get_width() * self.timegood.time/0.25)),abs(int(media.ERROR.get_height() * self.timegood.time/0.25)))
                self.erroronScreen.position = pygame.Vector2((constant.WIDTH - self.erroronScreen.image.get_width())/2, (constant.HEIGHT - self.erroronScreen.image.get_height())/2)
            if self.timegood.time > .25:
                temp = .5 - self.timegood.time
                self.erroronScreen.image = media.resize(media.ERROR, abs(int(media.ERROR.get_width() * temp/0.25)),abs(int(media.ERROR.get_height() * temp/0.25)))
                self.erroronScreen.position = pygame.Vector2((constant.WIDTH - self.erroronScreen.image.get_width())/2, (constant.HEIGHT - self.erroronScreen.image.get_height())/2)
        else:
            self.erroronScreen.image = media.resize(media.ERROR, 0, 0)
        if self.timegood.timing == False:
            self.ticketanimation = False
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

        self.typebtn0.draw(self.screen)
        self.typebtn1.draw(self.screen)
        self.typebtn2.draw(self.screen)
        self.typebtn3.draw(self.screen)
        self.typebtn4.draw(self.screen)
        self.typebtn5.draw(self.screen)
        self.typebtn6.draw(self.screen)
        self.typebtn7.draw(self.screen)
        self.typebtn8.draw(self.screen)
        self.typebtn9.draw(self.screen)
        self.typeerase.draw(self.screen)
        self.typesend.draw(self.screen)

        self.Rtypebtn0.draw(self.screen)
        self.Rtypebtn1.draw(self.screen)
        self.Rtypebtn2.draw(self.screen)
        self.Rtypebtn3.draw(self.screen)
        self.Rtypebtn4.draw(self.screen)
        self.Rtypebtn5.draw(self.screen)
        self.Rtypebtn6.draw(self.screen)
        self.Rtypebtn7.draw(self.screen)
        self.Rtypebtn8.draw(self.screen)
        self.Rtypebtn9.draw(self.screen)
        self.Rtypeerase.draw(self.screen)
        self.Rtypesend.draw(self.screen)

        self.typetextBlank.draw(self.screen)
        self.typetext.draw(self.screen)

        self.quitbtn.draw(self.screen)

class Menu:
    def __init__(self, _running = True, _profile = "") -> None:
        
        self.profile = _profile

        self.running = _running
        
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.menuphoto = objects.Node(pygame.Vector2(0,0),
                                      media.MENU)

        self.background = objects.Node(pygame.Vector2(0,0), media.BACKGROUND)
        self.playbtn = objects.Button(
            pygame.Vector2((constant.WIDTH-310)/2, (constant.HEIGHT+300)/2),
            _text="  touch to play")
        
        self.quitbtn = objects.Button(pygame.Vector2(55,70),
                                    media.resize(media.ERROR,40,40), "",
                                    media.resize(media.ERROR,40,40),media.resize(media.ERROR,40,40))
        self.quitTime = objects.Timer(.3)


        self.Profilebtn = objects.Button((450,25),
                                         media.resize(media.BTN, 155,70), self.profile,
                                         media.resize(media.BTN_HOVER, 155,70), media.resize(media.BTN_PRESSED, 155,70),
                                         pygame.Vector2(20,20))
        self.daystreakIcon = objects.Node(pygame.Vector2(620, 25), media.DAYSTREAK)
        self.daystreakText = objects.Text("0", pygame.Vector2(690, 45), constant.WHITE, media.NORMAL_FONT)


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
        self.Profilebtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)




    def draw(self):
        self.background.draw(self.screen)
        self.menuphoto.draw(self.screen)
        self.playbtn.draw(self.screen)
        self.quitbtn.draw(self.screen)
        self.settingsbtn.draw(self.screen)
        self.Profilebtn.draw(self.screen)
        self.daystreakIcon.draw(self.screen)
        self.daystreakText.draw(self.screen)


class ConfigurationMenu:
    def __init__(self, _running = True, _profile="") -> None:
        self.profile = _profile
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
        self.musicbtnstatus = objects.Node(pygame.Vector2(1190,90),media.resize(media.ERROR,40,40))

        self.hardbtn = objects.Button(pygame.Vector2(1170,180),
                                    media.resize(media.HARDMODE,80,80), "",
                                    media.resize(media.HARDMODE,80,80),media.resize(media.HARDMODE,80,80))
        self.hardbtnstatus = objects.Node(pygame.Vector2(1190,200),media.resize(media.ERROR,40,40))

        self.btnbase = objects.Button(pygame.Vector2(1170,290), media.BTN10, "", media.BTN12, media.BTN12)        
        
        self.btnanswermode = objects.Button(pygame.Vector2(1170,400), media.BTNANS1, "", media.BTNANS1, media.BTNANS1)


        self.btn1 = objects.Button(pygame.Vector2(30,180), media.BTN1, "", media.BTN1, media.BTN1)
        self.btn1status = objects.Node(pygame.Vector2(50,200),media.resize(media.ERROR,40,40))

        self.btn2 = objects.Button(pygame.Vector2(30,300), media.BTN2, "", media.BTN2, media.BTN2)
        self.btn2status = objects.Node(pygame.Vector2(50,320),media.resize(media.ERROR,40,40))

        self.btn3 = objects.Button(pygame.Vector2(30,420), media.BTN3, "", media.BTN3, media.BTN3)
        self.btn3status = objects.Node(pygame.Vector2(50,440),media.resize(media.ERROR,40,40))

        self.btn4 = objects.Button(pygame.Vector2(140,180), media.BTN4, "", media.BTN4, media.BTN4)
        self.btn4status = objects.Node(pygame.Vector2(160,200),media.resize(media.ERROR,40,40))

        self.btn5 = objects.Button(pygame.Vector2(140,300), media.BTN5, "", media.BTN5, media.BTN5)
        self.btn5status = objects.Node(pygame.Vector2(160,320),media.resize(media.ERROR,40,40))

        self.btn6 = objects.Button(pygame.Vector2(140,420), media.BTN6, "", media.BTN6, media.BTN6)
        self.btn6status = objects.Node(pygame.Vector2(160,440),media.resize(media.ERROR,40,40))

        self.btn7 = objects.Button(pygame.Vector2(250,180), media.BTN7, "", media.BTN7, media.BTN7)
        self.btn7status = objects.Node(pygame.Vector2(270,200),media.resize(media.ERROR,40,40))

        self.btn8 = objects.Button(pygame.Vector2(250,300), media.BTN8, "", media.BTN8, media.BTN8)
        self.btn8status = objects.Node(pygame.Vector2(270,320),media.resize(media.ERROR,40,40))

        self.btn9 = objects.Button(pygame.Vector2(250,420), media.BTN9, "", media.BTN9, media.BTN9)
        self.btn9status = objects.Node(pygame.Vector2(270,440),media.resize(media.ERROR,40,40))

        self.btn10 = objects.Button(pygame.Vector2(360,180), media.BTN10, "", media.BTN10, media.BTN10)
        self.btn10status = objects.Node(pygame.Vector2(380,200),media.resize(media.ERROR,40,40))

        self.btn11 = objects.Button(pygame.Vector2(360,300), media.BTN11, "", media.BTN11, media.BTN11)
        self.btn11status = objects.Node(pygame.Vector2(380,320),media.resize(media.ERROR,40,40))

        self.btn12 = objects.Button(pygame.Vector2(360,420), media.BTN12, "", media.BTN12, media.BTN12)
        self.btn12status = objects.Node(pygame.Vector2(380,440),media.resize(media.ERROR,40,40))


        self.status1 = True
        self.status2 = True
        self.status3 = True
        self.status4 = True
        self.status5 = True
        self.status6 = True
        self.status7 = True
        self.status8 = True
        self.status9 = True
        self.status10 = True
        self.status11 = False
        self.status12 = False
        self.statushard = True
        self.statusmusic = True

        self.statusmode = "multipleanswer"
        self.statusbase = 10

        self.readData()


        self.musicbtntime = objects.Timer(.3)
        self.hardbtntime = objects.Timer(.3)

    def readData(self):
        if os.path.exists(f"{platformdetect.getSavePath()}media/{self.profile}-data.dat"):
            jsonfile = platformdetect.readFile(f"{platformdetect.getSavePath()}media/{self.profile}-data.dat")
            self.status1 = platformdetect.getjsondataifexists(self.status1, jsonfile, "status1")
            self.status2 = platformdetect.getjsondataifexists(self.status2, jsonfile, "status2")
            self.status3 = platformdetect.getjsondataifexists(self.status3, jsonfile, "status3")
            self.status4 = platformdetect.getjsondataifexists(self.status4, jsonfile, "status4")
            self.status5 = platformdetect.getjsondataifexists(self.status5, jsonfile, "status5")
            self.status6 = platformdetect.getjsondataifexists(self.status6, jsonfile, "status6")
            self.status7 = platformdetect.getjsondataifexists(self.status7, jsonfile, "status7")
            self.status8 = platformdetect.getjsondataifexists(self.status8, jsonfile, "status8")
            self.status9 = platformdetect.getjsondataifexists(self.status9, jsonfile, "status9")
            self.status10 = platformdetect.getjsondataifexists(self.status10, jsonfile, "status10")
            self.status11 = platformdetect.getjsondataifexists(self.status11, jsonfile, "status11")
            self.status12 = platformdetect.getjsondataifexists(self.status12, jsonfile, "status12")

            self.statusmusic = platformdetect.getjsondataifexists(self.statusmusic, jsonfile, "statusmusic")
            self.statushard = platformdetect.getjsondataifexists(self.statushard, jsonfile, "statushard")
            self.statusbase = platformdetect.getjsondataifexists(self.statusbase, jsonfile, "statusbase")
            self.statusmode = platformdetect.getjsondataifexists(self.statusmode, jsonfile, "statusmode")
    def writeData(self):
        data = {}
        data["status1"] = self.status1
        data["status2"] = self.status2
        data["status3"] = self.status3
        data["status4"] = self.status4
        data["status5"] = self.status5
        data["status6"] = self.status6
        data["status7"] = self.status7
        data["status8"] = self.status8
        data["status9"] = self.status9
        data["status10"] = self.status10
        data["status11"] = self.status11
        data["status12"] = self.status12

        data["statusmusic"] = self.statusmusic
        data["statushard"] = self.statushard
        data["statusbase"] = self.statusbase
        data["statusmode"] = self.statusmode
        platformdetect.writeFile(f"{platformdetect.getSavePath()}media/{self.profile}-data.dat", data)
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
        
        self.btnbase.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btnanswermode.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)


        self.btn1.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn2.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn3.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn4.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn5.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn6.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn7.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn8.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn9.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn10.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn11.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn12.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        
        self.buttons_changing_status()

        self.changeimageofbtns()


    def changeimageofbtns(self):
        if self.statusbase == 10:
            self.btnbase.image = media.BTN10
            self.btnbase.normal_image = media.BTN10
            self.btnbase.image_hover = media.BTN10
            self.btnbase.image_pressed = media.BTN10
        elif self.statusbase == 12:
            self.btnbase.image = media.BTN12
            self.btnbase.normal_image = media.BTN12
            self.btnbase.image_hover = media.BTN12
            self.btnbase.image_pressed = media.BTN12

        if self.statusmode == "multipleanswer":
            self.btnanswermode.image = media.BTNANS1
            self.btnanswermode.normal_image = media.BTNANS1
            self.btnanswermode.image_hover = media.BTNANS1
            self.btnanswermode.image_pressed = media.BTNANS1
        elif self.statusmode == "write":
            self.btnanswermode.image = media.BTNANS2
            self.btnanswermode.normal_image = media.BTNANS2
            self.btnanswermode.image_hover = media.BTNANS2
            self.btnanswermode.image_pressed = media.BTNANS2

    def buttons_changing_status(self):
        if self.btn1.get_pressed:
            self.btn1.get_pressed = False
            self.status1 = not self.status1
        if self.btn2.get_pressed:
            self.btn2.get_pressed = False
            self.status2 = not self.status2
        if self.btn3.get_pressed:
            self.btn3.get_pressed = False
            self.status3 = not self.status3
        if self.btn4.get_pressed:
            self.btn4.get_pressed = False
            self.status4 = not self.status4
        if self.btn5.get_pressed:
            self.btn5.get_pressed = False
            self.status5 = not self.status5
        if self.btn6.get_pressed:
            self.btn6.get_pressed = False
            self.status6 = not self.status6
        if self.btn7.get_pressed:
            self.btn7.get_pressed = False
            self.status7 = not self.status7
        if self.btn8.get_pressed:
            self.btn8.get_pressed = False
            self.status8 = not self.status8
        if self.btn9.get_pressed:
            self.btn9.get_pressed = False
            self.status9 = not self.status9
        if self.btn10.get_pressed:
            self.btn10.get_pressed = False
            self.status10 = not self.status10
        if self.btn11.get_pressed:
            self.btn11.get_pressed = False
            self.status11 = not self.status11
        if self.btn12.get_pressed:
            self.btn12.get_pressed = False
            self.status12 = not self.status12
        if self.musicbtn.get_pressed:
            self.musicbtn.get_pressed = False
            self.statusmusic = not self.statusmusic
        if self.hardbtn.get_pressed:
            self.hardbtn.get_pressed = False
            self.statushard = not self.statushard

        if self.btnbase.get_pressed:
            self.btnbase.get_pressed = False
            if self.statusbase == 10:
                self.statusbase = 12
            else:
                self.statusbase = 10
        if self.btnanswermode.get_pressed:
            self.btnanswermode.get_pressed = False
            if self.statusmode == "multipleanswer":
                self.statusmode = "write"
            else:
                self.statusmode = "multipleanswer"

    def returnvalues(self):
        return (self.statusmusic, self.statushard, self.statusbase, self.statusmode)

    def returnlistfromnumbers(self):
        list = []
        if self.status1:
            list.append(1)
        if self.status2:
            list.append(2)
        if self.status3:
            list.append(3)
        if self.status4:
            list.append(4)
        if self.status5:
            list.append(5)
        if self.status6:
            list.append(6)
        if self.status7:
            list.append(7)
        if self.status8:
            list.append(8)
        if self.status9:
            list.append(9)
        if self.status10:
            list.append(10)
        if self.status11:
            list.append(11)
        if self.status12:
            list.append(12)
        return list

    def draw(self):
        self.background.draw(self.screen)
        self.quitbtn.draw(self.screen)
        self.musicbtn.draw(self.screen)

        self.btnbase.draw(self.screen)
        self.btnanswermode.draw(self.screen)

        self.btn1.draw(self.screen)
        self.btn2.draw(self.screen)
        self.btn3.draw(self.screen)
        self.btn4.draw(self.screen)
        self.btn5.draw(self.screen)
        self.btn6.draw(self.screen)
        self.btn7.draw(self.screen)
        self.btn8.draw(self.screen)
        self.btn9.draw(self.screen)
        self.btn10.draw(self.screen)
        self.btn11.draw(self.screen)
        self.btn12.draw(self.screen)

        self.hardbtn.draw(self.screen)

        if not self.status1:
            self.btn1status.draw(self.screen)
        if not self.status2:
            self.btn2status.draw(self.screen)
        if not self.status3:
            self.btn3status.draw(self.screen)
        if not self.status4:
            self.btn4status.draw(self.screen)
        if not self.status5:
            self.btn5status.draw(self.screen)
        if not self.status6:
            self.btn6status.draw(self.screen)
        if not self.status7:
            self.btn7status.draw(self.screen)
        if not self.status8:
            self.btn8status.draw(self.screen)
        if not self.status9:
            self.btn9status.draw(self.screen)
        if not self.status10:
            self.btn10status.draw(self.screen)
        if not self.status11:
            self.btn11status.draw(self.screen)
        if not self.status12:
            self.btn12status.draw(self.screen)

        if not self.statusmusic:
            self.musicbtnstatus.draw(self.screen)
        if not self.statushard:
            self.hardbtnstatus.draw(self.screen)

if __name__ == "__main__":
    game = Game()
    game.mainloop()
