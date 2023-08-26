import pygame
import constant
import media
import objects
import random
import os
import sound
import platformdetect
import datetime
import shutil

pygame.init()

class Game:
    def __init__(self) -> None:

        if platformdetect.platform() == "android":
            self.window = pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption("Multiplication Practice")

        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        self.gotchangedonandroidH = False
        self.gotchangedonandroidW = False
        self.changenexttofullscreen = False

        self.lgoods = 0

        self.current_date = datetime.date.today()
        self.current_date_since_started = datetime.date.today()
        self.yesterday_date = self.current_date - datetime.timedelta(days=1)
        self.lastdate = datetime.date.today() - datetime.timedelta(days=10)
        self.gotDaystreakToday = False
        self.daystreak = 0
        self.daystreak_goal = 10
        self.profile = ""
        self.profiles = [None]
        self.pointsC = 0
        self.getProfile()
        self.writeProfile()
        self.updateDayStreak()

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
        self.renameMenu = RenameMenu(False, self.profile)

        self.sound_channel = pygame.mixer.Channel(2)
        self.musicallowed = True
        self.hardmode = False


        self.mainGame.numberlist = None
        self.mainGame.numberlist = self.settingsMenu.returnlistfromnumbers()
        self.musicallowed, self.hardmode, self.mainGame.maxnumber, self.typeanswer = self.settingsMenu.returnvalues()
        
        self.savecounter = 5
        self.savecounterTime = objects.Timer(10)




    def mainloop(self):
        while self.running:

            self.settingsMenu.pointsC = self.pointsC
            self.current_date = datetime.date.today()
            if self.current_date > self.current_date_since_started:
                print("Day Changed")
                self.yesterday_date = self.current_date - datetime.timedelta(days=1)
                self.updateDayStreak()

            if self.gotchangedonandroidH == False and platformdetect.platform() == "android":
                if self.window.get_height() < self.window.get_width():
                    self.gotchangedonandroidH = True
                    self.changenexttofullscreen = True
                    pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.RESIZABLE)

                    
            if self.changenexttofullscreen:
                if self.window.get_height() < self.window.get_width():
                    self.changenexttofullscreen = False
                    pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.FULLSCREEN)

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
                    if event.key == pygame.K_f:
                        if event.key == pygame.K_f:  # Press 'f' to toggle fullscreen
                            self.fullscreen = not self.fullscreen  # Toggle fullscreen flag
                            if self.fullscreen:
                                pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.FULLSCREEN)
                            else:
                                pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.RESIZABLE)
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
            self.settingsMenu.daystreak = self.daystreak
            self.settingsMenu.lastdate = self.lastdate
            self.mainMenu.daystreakText.text = str(self.daystreak)

            if self.mainGame.goods == 0:
                self.lgoods = 0

            if self.lgoods < self.mainGame.goods:
                print("Got 1 pts")
                self.pointsC += 1

            self.lgoods = self.mainGame.goods
            if self.gotDaystreakToday:
                self.mainMenu.daystreakIcon.image = media.DAYSTREAK
            else:
                self.mainMenu.daystreakIcon.image = media.NODAYSTREAK
                if self.mainGame.goods >= self.daystreak_goal:
                    self.mainGame.gotdaystreak=True
                    self.daystreak += 1
                    print ("Got 9 more, should be 10 total")
                    self.pointsC += 9
                    self.gotDaystreakToday = True
                    self.lastdate = datetime.date.today()
                    self.settingsMenu.lastdate = self.lastdate
                    self.settingsMenu.daystreak = self.daystreak
                    self.settingsMenu.writeData()
                    
                
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
            if self.renameMenu.running:
                self.renameMenu.mainloop(self.fix, self.offset,
                                    self.deltaTime,
                                    self.mouseposX, self.mouseposY,
                                    self.mousepressed)
                

            self.savecounterTime.update(self.deltaTime)     
            if self.savecounterTime.timing == False:
                self.savecounter = 5
                self.mainMenu.saveremovetext.text = f""        
            
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
                self.settingsMenu.writeData()
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
            
            if self.mainMenu.addprbtn.get_pressed:
                self.mainMenu.addprbtn.get_pressed = False
                self.writenewProfile()
            if self.mainMenu.removeprbtn.get_pressed:
                self.mainMenu.removeprbtn.get_pressed = False
                if len(self.profiles) > 1:
                    self.savecounterTime.timing = True
                    self.savecounterTime.time = 0
                    self.savecounter -= 1
                    self.mainMenu.saveremovetext.text = f"{self.savecounter} left"
                    if self.savecounter <= 0:
                        self.removecurrentProfile()
                        self.savecounter = 5
                        self.mainMenu.saveremovetext.text = f""
            if self.mainMenu.renameprbtn.get_pressed:
                self.mainMenu.renameprbtn.get_pressed = False
                self.mainMenu.running = False
                self.renameMenu.running = True
                self.renameMenu.profile = self.profile
                self.renameMenu.currentWritingName.text = ""
            if self.renameMenu.quitbtn.get_pressed:
                self.renameMenu.quitbtn.get_pressed = False
                self.mainMenu.running = True
                self.renameMenu.running = False
            if self.renameMenu.btnSEND.get_pressed:
                self.renameMenu.btnSEND.get_pressed = False
                if not self.checkifProfileexists(self.renameMenu.currentWritingName.text) and self.renameMenu.currentWritingName.text != "":
                    lastprofile = self.profile
                    index = self.profiles.index(lastprofile)
                    self.profile = self.renameMenu.currentWritingName.text
                    self.profiles[index] = self.profile
                    # Change .dat
                    self.changedatnamefrom(lastprofile, self.profile)
                    self.updateProfileData()
                    self.renameMenu.quitbtn.get_pressed = True


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
            if self.renameMenu.running:
                self.window.blit(pygame.transform.scale(
                    self.renameMenu.screen, (int(constant.WIDTH*self.fix), int(constant.HEIGHT*self.fix))), 
                    self.offset)

            pygame.display.update()
    
    def updateConfig(self):
        self.musicallowed, self.hardmode, self.mainGame.maxnumber, self.typeanswer = self.settingsMenu.returnvalues()
    def updateListConfig(self):
        self.mainGame.numberlist = self.settingsMenu.returnlistfromnumbers()

    def updateDayStreak(self):
        self.readDayStreak()
        if self.lastdate == self.current_date:
            self.gotDaystreakToday = True
        else:
            self.gotDaystreakToday = False
        if self.lastdate < self.yesterday_date:
            self.daystreak = 0

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

    def checkifProfileexists(self, profile):
        if profile in self.profiles:
            return True
        else:
            return False

    def getProfile(self):
        if os.path.exists(f"{platformdetect.getSavePath()}data/profiles.dat"):
            jsonfile = platformdetect.readFile(f"{platformdetect.getSavePath()}data/profiles.dat")

            self.profile = platformdetect.getjsondataifexists("User", jsonfile, "current_profile")
            self.profiles = platformdetect.getjsondataifexists(self.profiles, jsonfile, "profiles")
        else:
            self.profile = "User"
            self.profiles = ["User"]
    def writenewProfile(self):
        i = 0
        cont = True
        while cont:
            if i == 0:
                if not "User" in self.profiles:
                    self.profiles.append("User")
                    self.profile = "User"
                    cont = False
            else:
                if not f"User{i}" in self.profiles:
                    self.profiles.append(f"User{i}")
                    self.profile = f"User{i}"
                    cont = False
            i+=1
        self.updateProfileData()
    def removecurrentProfile(self):
        profiletodelete = self.profile
        self.changeProfile()

        if profiletodelete in self.profiles:
            self.profiles.remove(profiletodelete)
            print(self.profiles)
        if os.path.exists(f"{platformdetect.getSavePath()}data/{profiletodelete}-data.dat"):
            os.remove(f"{platformdetect.getSavePath()}data/{profiletodelete}-data.dat")
        self.updateProfileData()

    def changedatnamefrom(self, start, end):
        if os.path.exists(f"{platformdetect.getSavePath()}data/{end}-data.dat"):
            os.remove(f"{platformdetect.getSavePath()}data/{end}-data.dat")

        if os.path.exists(f"{platformdetect.getSavePath()}data/{start}-data.dat"):
            shutil.copy(f"{platformdetect.getSavePath()}data/{start}-data.dat", f"{platformdetect.getSavePath()}data/{end}-data.dat")
            os.remove(f"{platformdetect.getSavePath()}data/{start}-data.dat")


    def updateProfileData(self):
        self.writeProfile()

        self.mainMenu.profile = self.profile
        self.settingsMenu.profile = self.profile
        self.settingsMenu.readData()
        self.mainMenu.Profilebtn.text.text = self.profile

        self.updateListConfig()
        self.updateConfig()
        self.updateTypeAnswer()
        self.updateDayStreak()

        print(f"Change to {self.profile}")
    def writeProfile(self):
        data = {}
        data["current_profile"] = self.profile
        data["profiles"] = self.profiles
        platformdetect.writeFile(f"{platformdetect.getSavePath()}data/profiles.dat", data)
    
    def readDayStreak(self):
        if os.path.exists(f"{platformdetect.getSavePath()}data/{self.profile}-data.dat"):
            jsonfile = platformdetect.readFile(f"{platformdetect.getSavePath()}data/{self.profile}-data.dat")

            self.daystreak = platformdetect.getjsondataifexists(0, jsonfile, "daystreak")
            self.pointsC = platformdetect.getjsondataifexists(0, jsonfile, "points")
            lastdate = platformdetect.getjsondataifexists("w0", jsonfile, "lastdaystreakday")
            if lastdate != "w0":
                self.lastdate = datetime.datetime.fromisoformat(lastdate).date()
        else:
            self.daystreak = 0
            self.lastdate = datetime.date.today() - datetime.timedelta(days=10)
            self.pointsC = 0

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
        self.updateDayStreak()

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
        
        self.gotdaystreak = False


        self.shuffle = True
        self.correctbtnnumber = random.randint(1,4)
        self.correctbtn = objects.Multiplication(10)

        self.otherbtn1 = objects.Multiplication(10)
        self.otherbtn2 = objects.Multiplication(10)
        self.otherbtn3 = objects.Multiplication(10)

        self.quitbtn = objects.Button(pygame.Vector2(45,60),
                                    media.resize(media.ERROR,60,60), "",
                                    media.resize(media.ERROR,60,60),media.resize(media.ERROR,60,60))
        

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
        else:
            self.typebtn0.get_pressed = False
            self.typebtn1.get_pressed = False
            self.typebtn2.get_pressed = False
            self.typebtn3.get_pressed = False
            self.typebtn4.get_pressed = False
            self.typebtn5.get_pressed = False
            self.typebtn6.get_pressed = False
            self.typebtn7.get_pressed = False
            self.typebtn8.get_pressed = False
            self.typebtn9.get_pressed = False
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
            ticket = media.TICKET
            if self.gotdaystreak:
                ticket = media.TICKETDAYSTREAK
            if self.timegood.time < .25:
                self.ticketonScreen.image = media.resize(ticket, abs(int(ticket.get_width() * self.timegood.time/0.25)),abs(int(ticket.get_height() * self.timegood.time/0.25)))
                self.ticketonScreen.position = pygame.Vector2((constant.WIDTH - self.ticketonScreen.image.get_width())/2, (constant.HEIGHT - self.ticketonScreen.image.get_height())/2)
            if self.timegood.time > .25:
                temp = .5 - self.timegood.time
                self.ticketonScreen.image = media.resize(ticket, abs(int(ticket.get_width() * temp/0.25)),abs(int(ticket.get_height() * temp/0.25)))
                self.ticketonScreen.position = pygame.Vector2((constant.WIDTH - self.ticketonScreen.image.get_width())/2, (constant.HEIGHT - self.ticketonScreen.image.get_height())/2)

        else:
            self.ticketonScreen.image = media.resize(media.TICKET, 0, 0)
            self.gotdaystreak = False
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
        
        self.quitbtn = objects.Button(pygame.Vector2(45,60),
                                    media.resize(media.ERROR,60,60), "",
                                    media.resize(media.ERROR,60,60),media.resize(media.ERROR,60,60))
        self.quitTime = objects.Timer(.3)


        self.Profilebtn = objects.Button((450,25),
                                         media.resize(media.BTN, 155,70), self.profile,
                                         media.resize(media.BTN_HOVER, 155,70), media.resize(media.BTN_PRESSED, 155,70),
                                         pygame.Vector2(20,20))
        self.daystreakIcon = objects.Node(pygame.Vector2(620, 28), media.DAYSTREAK)
        self.daystreakText = objects.Text("0", pygame.Vector2(690, 45), constant.WHITE, media.NORMAL_FONT)

        K = 200
        self.addprbtn = objects.Button((K, 28),
                                         media.ADD, "",
                                         media.ADD, media.ADD)
        self.removeprbtn = objects.Button((K + 80, 28),
                                         media.REMOVE, "",
                                         media.REMOVE, media.REMOVE)
        self.renameprbtn = objects.Button((K + 160, 28),
                                         media.RENAME, "",
                                         media.RENAME, media.RENAME)
        self.saveremovetext = objects.Text("", (K + 100, 100), constant.WHITE, media.NORMAL_FONT)

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
        self.addprbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.removeprbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.renameprbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)




    def draw(self):
        self.background.draw(self.screen)
        self.menuphoto.draw(self.screen)
        self.playbtn.draw(self.screen)
        self.quitbtn.draw(self.screen)
        self.settingsbtn.draw(self.screen)
        self.Profilebtn.draw(self.screen)
        self.daystreakIcon.draw(self.screen)
        self.daystreakText.draw(self.screen)
        self.addprbtn.draw(self.screen)
        self.removeprbtn.draw(self.screen)
        self.renameprbtn.draw(self.screen)
        self.saveremovetext.draw(self.screen)


class ConfigurationMenu:
    def __init__(self, _running = True, _profile="") -> None:
        self.profile = _profile
        self.running = _running
        self.daystreak = 0
        self.pointsC = 0
        self.lastdate = datetime.date.today() - datetime.timedelta(days=10)
        
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.background = objects.Node(pygame.Vector2(0,0), media.BACKGROUND)

        self.quitbtn = objects.Button(pygame.Vector2(45,60),
                                    media.resize(media.ERROR,60,60), "",
                                    media.resize(media.ERROR,60,60),media.resize(media.ERROR,60,60))
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
        if os.path.exists(f"{platformdetect.getSavePath()}data/{self.profile}-data.dat"):
            jsonfile = platformdetect.readFile(f"{platformdetect.getSavePath()}data/{self.profile}-data.dat")
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

        data["daystreak"] = self.daystreak
        data["lastdaystreakday"] = self.lastdate.isoformat()
        data["points"] = self.pointsC
        platformdetect.writeFile(f"{platformdetect.getSavePath()}data/{self.profile}-data.dat", data)
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

class RenameMenu:
    def __init__(self, _running = True, _profile="") -> None:
        self.profile = _profile
        self.running = _running
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.background = objects.Node(pygame.Vector2(0,0), media.BACKGROUND)

        self.quitbtn = objects.Button(pygame.Vector2(45,60),
                                    media.resize(media.ERROR,60,60), "",
                                    media.resize(media.ERROR,60,60),media.resize(media.ERROR,60,60))
        self.quitTime = objects.Timer(.3)

        self.previousName = objects.Text("", (500,20), constant.WHITE, media.NORMAL_FONT)
        self.currentWritingNameBLANK = objects.Node((540, 55), media.resize(media.BLANK, 200, 50))
        self.currentWritingName = objects.Text("", (550,60), constant.BLACK, media.NORMAL_FONT)

        self.mayus = False

        KW = 150
        KH = 300
        AKW = 90
        AKH = 90
        ASZ = 70
        DSZ = pygame.Vector2(25,20)

        self.btn1 = objects.Button((KW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "1",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn2 = objects.Button((KW + AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "2",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn3 = objects.Button((KW + 2*AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "3",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn4 = objects.Button((KW + 3*AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "4",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn5 = objects.Button((KW + 4*AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "5",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn6 = objects.Button((KW + 5*AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "6",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn7 = objects.Button((KW + 6*AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "7",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn8 = objects.Button((KW + 7*AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "8",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn9 = objects.Button((KW + 8*AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "9",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btn0 = objects.Button((KW + 9*AKW, KH - AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "0",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnQ = objects.Button((KW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "Q",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnW = objects.Button((KW + AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "W",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnE = objects.Button((KW + 2*AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "E",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnR = objects.Button((KW + 3*AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "R",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnT = objects.Button((KW + 4*AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "T",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnY = objects.Button((KW + 5*AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "Y",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnU = objects.Button((KW + 6*AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "U",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnI = objects.Button((KW + 7*AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "I",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnO = objects.Button((KW + 8*AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "O",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnP = objects.Button((KW + 9*AKW, KH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "P",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)

        self.btnA = objects.Button((KW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "A",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnS = objects.Button((KW + AKW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "S",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnD = objects.Button((KW + 2*AKW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "D",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnF = objects.Button((KW + 3*AKW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "F",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnG = objects.Button((KW + 4*AKW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "G",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnH = objects.Button((KW + 5*AKW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "H",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnJ = objects.Button((KW + 6*AKW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "J",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnK = objects.Button((KW + 7*AKW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "K",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnL = objects.Button((KW + 8*AKW, KH + AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "L",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        

        self.btnMAYUS = objects.Button((KW, KH + 2*AKH), 
                                   media.resize(media.BLANK,ASZ + AKW,ASZ), "Mayus",
                                   media.resize(media.BLANK,ASZ + AKW,ASZ), media.resize(media.BLANK,ASZ + AKW,ASZ),
                                   DSZ)

        self.btnZ = objects.Button((KW + 2*AKW, KH + 2*AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "Z",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnX = objects.Button((KW + 3*AKW, KH + 2*AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "X",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnC = objects.Button((KW + 4*AKW, KH + 2*AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "C",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnV = objects.Button((KW + 5*AKW, KH + 2*AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "V",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnB = objects.Button((KW + 6*AKW, KH + 2*AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "B",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnN = objects.Button((KW + 7*AKW, KH + 2*AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "N",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        self.btnM = objects.Button((KW + 8*AKW, KH + 2*AKH), 
                                   media.resize(media.BLANK,ASZ,ASZ), "M",
                                   media.resize(media.BLANK,ASZ,ASZ), media.resize(media.BLANK,ASZ,ASZ),
                                   DSZ)
        
        self.btnERASE = objects.Button((KW + 9*AKW, KH + AKH), 
                                   media.resize(media.ERROR,ASZ,ASZ), "",
                                   media.resize(media.ERROR,ASZ,ASZ), media.resize(media.ERROR,ASZ,ASZ),
                                   DSZ)
        self.btnSEND = objects.Button((KW + 9*AKW, KH + 2*AKH), 
                                   media.resize(media.TICKET,ASZ,ASZ), "",
                                   media.resize(media.TICKET,ASZ,ASZ), media.resize(media.TICKET,ASZ,ASZ),
                                   DSZ)


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

        self.previousName.text = f"Change {self.profile} to..."
        self.btn1.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn2.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn3.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn4.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn5.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn6.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn7.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn8.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn9.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btn0.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)


        self.btnQ.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnW.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnE.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnR.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnT.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnY.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnU.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnI.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnO.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnP.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)

        self.btnA.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnS.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnD.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnF.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnG.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnH.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnJ.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnK.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnL.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)

        self.btnMAYUS.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)

        self.btnZ.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnX.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnC.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnV.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnB.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnN.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnM.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)

        self.btnERASE.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)
        self.btnSEND.update(self.deltaTime,self.mousepressed,self.mouseposX,self.mouseposY,self.fix,self.offset)

        if self.btnERASE.get_pressed:
            self.btnERASE.get_pressed = False
            self.currentWritingName.text = ""
        if self.btnMAYUS.get_pressed:
            self.btnMAYUS.get_pressed = False
            self.mayus = not self.mayus
        elif len(self.currentWritingName.text) <= 11:
            if self.btn0.get_pressed:
                self.btn0.get_pressed = False
                self.currentWritingName.text += "0"
            elif self.btn1.get_pressed:
                self.btn1.get_pressed = False
                self.currentWritingName.text += "1"
            elif self.btn2.get_pressed:
                self.btn2.get_pressed = False
                self.currentWritingName.text += "2"
            elif self.btn3.get_pressed:
                self.btn3.get_pressed = False
                self.currentWritingName.text += "3"
            elif self.btn4.get_pressed:
                self.btn4.get_pressed = False
                self.currentWritingName.text += "4"
            elif self.btn5.get_pressed:
                self.btn5.get_pressed = False
                self.currentWritingName.text += "5"
            elif self.btn6.get_pressed:
                self.btn6.get_pressed = False
                self.currentWritingName.text += "6"
            elif self.btn7.get_pressed:
                self.btn7.get_pressed = False
                self.currentWritingName.text += "7"
            elif self.btn8.get_pressed:
                self.btn8.get_pressed = False
                self.currentWritingName.text += "8"
            elif self.btn9.get_pressed:
                self.btn9.get_pressed = False
                self.currentWritingName.text += "9"
            elif self.btnQ.get_pressed:
                self.btnQ.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "Q"
                else:
                    self.currentWritingName.text += "Q".lower()
            elif self.btnW.get_pressed:
                self.btnW.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "W"
                else:
                    self.currentWritingName.text += "W".lower()
            elif self.btnE.get_pressed:
                self.btnE.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "E"
                else:
                    self.currentWritingName.text += "E".lower()
            elif self.btnR.get_pressed:
                self.btnR.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "R"
                else:
                    self.currentWritingName.text += "R".lower()
            elif self.btnT.get_pressed:
                self.btnT.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "T"
                else:
                    self.currentWritingName.text += "T".lower()
            elif self.btnY.get_pressed:
                self.btnY.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "Y"
                else:
                    self.currentWritingName.text += "Y".lower()
            elif self.btnU.get_pressed:
                self.btnU.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "U"
                else:
                    self.currentWritingName.text += "U".lower()
            elif self.btnI.get_pressed:
                self.btnI.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "I"
                else:
                    self.currentWritingName.text += "I".lower()
            elif self.btnO.get_pressed:
                self.btnO.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "O"
                else:
                    self.currentWritingName.text += "O".lower()
            elif self.btnP.get_pressed:
                self.btnP.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "P"
                else:
                    self.currentWritingName.text += "P".lower()
            elif self.btnA.get_pressed:
                self.btnA.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "A"
                else:
                    self.currentWritingName.text += "A".lower()
            elif self.btnS.get_pressed:
                self.btnS.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "S"
                else:
                    self.currentWritingName.text += "S".lower()
            elif self.btnD.get_pressed:
                self.btnD.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "D"
                else:
                    self.currentWritingName.text += "D".lower()
            elif self.btnF.get_pressed:
                self.btnF.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "F"
                else:
                    self.currentWritingName.text += "F".lower()
            elif self.btnG.get_pressed:
                self.btnG.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "G"
                else:
                    self.currentWritingName.text += "G".lower()
            elif self.btnH.get_pressed:
                self.btnH.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "H"
                else:
                    self.currentWritingName.text += "H".lower()
            elif self.btnJ.get_pressed:
                self.btnJ.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "J"
                else:
                    self.currentWritingName.text += "J".lower()
            elif self.btnK.get_pressed:
                self.btnK.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "K"
                else:
                    self.currentWritingName.text += "K".lower()
            elif self.btnL.get_pressed:
                self.btnL.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "L"
                else:
                    self.currentWritingName.text += "L".lower()
            elif self.btnZ.get_pressed:
                self.btnZ.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "Z"
                else:
                    self.currentWritingName.text += "Z".lower()
            elif self.btnX.get_pressed:
                self.btnX.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "X"
                else:
                    self.currentWritingName.text += "X".lower()
            elif self.btnC.get_pressed:
                self.btnC.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "C"
                else:
                    self.currentWritingName.text += "C".lower()
            elif self.btnV.get_pressed:
                self.btnV.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "V"
                else:
                    self.currentWritingName.text += "V".lower()
            elif self.btnB.get_pressed:
                self.btnB.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "B"
                else:
                    self.currentWritingName.text += "B".lower()
            elif self.btnN.get_pressed:
                self.btnN.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "N"
                else:
                    self.currentWritingName.text += "N".lower()
            elif self.btnM.get_pressed:
                self.btnM.get_pressed = False
                if self.mayus:
                    self.currentWritingName.text += "M"
                else:
                    self.currentWritingName.text += "M".lower()
        else:
            self.btn1.get_pressed = False
            self.btn2.get_pressed = False
            self.btn3.get_pressed = False
            self.btn4.get_pressed = False
            self.btn5.get_pressed = False
            self.btn6.get_pressed = False
            self.btn7.get_pressed = False
            self.btn8.get_pressed = False
            self.btn9.get_pressed = False
            self.btn0.get_pressed = False
            self.btnQ.get_pressed = False
            self.btnW.get_pressed = False
            self.btnE.get_pressed = False
            self.btnR.get_pressed = False
            self.btnT.get_pressed = False
            self.btnY.get_pressed = False
            self.btnU.get_pressed = False
            self.btnI.get_pressed = False
            self.btnO.get_pressed = False
            self.btnP.get_pressed = False
            self.btnA.get_pressed = False
            self.btnS.get_pressed = False
            self.btnD.get_pressed = False
            self.btnF.get_pressed = False
            self.btnG.get_pressed = False
            self.btnH.get_pressed = False
            self.btnJ.get_pressed = False
            self.btnK.get_pressed = False
            self.btnL.get_pressed = False
            self.btnZ.get_pressed = False
            self.btnX.get_pressed = False
            self.btnC.get_pressed = False
            self.btnV.get_pressed = False
            self.btnB.get_pressed = False
            self.btnN.get_pressed = False
            self.btnM.get_pressed = False


    def draw(self):
        self.background.draw(self.screen)
        self.quitbtn.draw(self.screen)
        self.previousName.draw(self.screen)
        self.currentWritingNameBLANK.draw(self.screen)
        self.currentWritingName.draw(self.screen)

        self.btn1.draw(self.screen)
        self.btn2.draw(self.screen)
        self.btn3.draw(self.screen)
        self.btn4.draw(self.screen)
        self.btn5.draw(self.screen)
        self.btn6.draw(self.screen)
        self.btn7.draw(self.screen)
        self.btn8.draw(self.screen)
        self.btn9.draw(self.screen)
        self.btn0.draw(self.screen)

        self.btnQ.draw(self.screen)
        self.btnW.draw(self.screen)
        self.btnE.draw(self.screen)
        self.btnR.draw(self.screen)
        self.btnT.draw(self.screen)
        self.btnY.draw(self.screen)
        self.btnU.draw(self.screen)
        self.btnI.draw(self.screen)
        self.btnO.draw(self.screen)
        self.btnP.draw(self.screen)

        self.btnA.draw(self.screen)
        self.btnS.draw(self.screen)
        self.btnD.draw(self.screen)
        self.btnF.draw(self.screen)
        self.btnG.draw(self.screen)
        self.btnH.draw(self.screen)
        self.btnJ.draw(self.screen)
        self.btnK.draw(self.screen)
        self.btnL.draw(self.screen)

        self.btnMAYUS.draw(self.screen)

        self.btnZ.draw(self.screen)
        self.btnX.draw(self.screen)
        self.btnC.draw(self.screen)
        self.btnV.draw(self.screen)
        self.btnB.draw(self.screen)
        self.btnN.draw(self.screen)
        self.btnM.draw(self.screen)

        self.btnERASE.draw(self.screen)
        self.btnSEND.draw(self.screen)

            



if __name__ == "__main__":
    game = Game()
    game.mainloop()
