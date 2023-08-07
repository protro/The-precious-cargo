# Setup Python ----------------------------------------------- #
import pygame, sys, random, time, webbrowser, os
from datetime import datetime
# Version ---------------------------------------------------- #
Version = '1.0'
# Setup pygame/window ---------------------------------------- #
SCALE = 3
x = 100
y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.display.set_caption('Precious Cargo')
WINDOWWIDTH = 300*SCALE
WINDOWHEIGHT = 200*SCALE
Icon = pygame.image.load('Data/Images/Icon.png')
pygame.display.set_icon(Icon)
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
Display = pygame.Surface((300,200))
fullscreen=False
# Images ----------------------------------------------------- #
def LoadTileAnimation(path,cap):
    Images = []
    num = 0
    while num <= cap:
        Image = pygame.image.load(path + '_' + str(num) + '.png').convert()
        Image.set_colorkey((255,255,255))
        Images.append(Image.copy())
        num += 1
    return Images
def LoadIsland(path):
    file = open(path,'r')
    IslandMap = file.read()
    file.close()
    TrueMap = []
    x = 0
    y = 0
    for char in IslandMap:
        if char != '\r':
            if char != '\n':
                if char != '~':
                    TrueMap.append([char,(x*8,y*8)])
                x += 1
            else:
                y += 1
                x = 0
    return TrueMap
Scout_Ship = LoadIsland('Data/Structures/Scout_Ship.txt')
Ambush = LoadIsland('Data/Structures/Ambush.txt')
Speed_Bomber = LoadIsland('Data/Structures/Speed_Bomber.txt')
Carrier = LoadIsland('Data/Structures/Carrier.txt')
Fighter_Ship = LoadIsland('Data/Structures/Fighter_Ship.txt')
Mother_Ship = LoadIsland('Data/Structures/Mother_Ship.txt')
Platform = LoadIsland('Data/Structures/Platform.txt')
Island = LoadIsland('Data/Structures/Island.txt')
Tiles = {}
TILE_AMOUNT = 11
Tileset = pygame.image.load('Data/Images/Tileset.png').convert()
Tileset.set_colorkey((255,255,255))
num = 0
num2 = 0
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
while num < TILE_AMOUNT:
    Clip = pygame.Rect(num*9,0,8,8)
    Tileset.set_clip(Clip)
    TileImage = Tileset.subsurface(Tileset.get_clip())
    Tiles[str(num2)] = [False,TileImage,True]
    num += 1
    if num > 9:
        num2 = alphabet[num-10]
    else:
        num2 = num
Tiles['5'][2] = False
Tiles['a'][2] = False
Tiles['z'] = [True,LoadTileAnimation('Data/Images/Other Animations/Grass Tile/Grass',4),False]
Tiles['y'] = [True,LoadTileAnimation('Data/Images/Other Animations/Thruster/Thruster',2),False]
Tiles['x'] = [True,LoadTileAnimation('Data/Images/Other Animations/Thruster/Thruster',2),False]
Tiles['v'] = [True,LoadTileAnimation('Data/Images/Other Animations/Gun/Out',15),False]
num = 0
for Tile in Tiles['x'][1]:
    Tiles['x'][1][num] = pygame.transform.flip(Tile,True,False)
    num += 1
BackgroundImage = pygame.image.load('Data/Images/Background.png')
Player_0 = pygame.image.load('Data/Images/Player/Player_0.png').convert()
Player_1 = pygame.image.load('Data/Images/Player/Player_1.png').convert()
Player_2 = pygame.image.load('Data/Images/Player/Player_2.png').convert()
CrystalBase = pygame.image.load('Data/Images/Crystal/MiddleLayer.png').convert()
CrystalValueMain = pygame.image.load('Data/Images/Crystal/ValueLayer.png').convert()
CrystalTop = pygame.image.load('Data/Images/Crystal/TopLayer.png').convert()
WarningImage = pygame.image.load('Data/Images/Warning.png').convert()
ProgressBar = pygame.image.load('Data/Images/ProgressBar.png').convert()
Progress = pygame.image.load('Data/Images/Progress.png').convert()
SmashAnimation = LoadTileAnimation('Data/Images/Other Animations/Smash/Out',23)
SidePunch = LoadTileAnimation('Data/Images/Other Animations/Punch/Out',12)
OuterSmashAnimation = LoadTileAnimation('Data/Images/Other Animations/Smash/Outer/Out',9)
MeleePirate = LoadTileAnimation('Data/Images/Other Animations/Melee Pirate/Out',2)
MeleePirateDeath = LoadTileAnimation('Data/Images/Other Animations/Melee Pirate/Death/Out',6)
RunnerPirate = LoadTileAnimation('Data/Images/Other Animations/Runner Pirate/Out',2)
RunnerPirateDeath = LoadTileAnimation('Data/Images/Other Animations/Runner Pirate/Death/Out',6)
PowerParticle = pygame.image.load('Data/Images/PowerParticle.png').convert()
MovementHelp = LoadTileAnimation('Data/Images/Buttons/Movement',1)
CombatHelp = LoadTileAnimation('Data/Images/Buttons/Combat',1)
DestroyHelp = LoadTileAnimation('Data/Images/Buttons/Destroy',1)
BulletImage = pygame.image.load('Data/Images/Bullet.png')
TurnAnimation = LoadTileAnimation('Data/Images/Other Animations/Turn/Out',8)
JumpAnimation = LoadTileAnimation('Data/Images/Other Animations/Jump/Out',13)
StarImages = LoadTileAnimation('Data/Images/Stars/Star',6)
PowerParticle.set_colorkey((255,255,255))
Player_0.set_colorkey((255,255,255))
Player_1.set_colorkey((255,255,255))
Player_2.set_colorkey((255,255,255))
CrystalBase.set_colorkey((255,255,255))
CrystalValueMain.set_colorkey((255,255,255))
CrystalTop.set_colorkey((255,255,255))
WarningImage.set_colorkey((255,255,255))
ProgressBar.set_colorkey((255,255,255))
Progress.set_colorkey((255,255,255))
PlayerImages = [Player_0,Player_1,Player_2]
BISLANDTOTAL = 5
BIslandImages = LoadTileAnimation('Data/Images/Islands/Island',BISLANDTOTAL)
BIslandDistances = {0:0.025,1:0.05,2:0.07,3:0.08,4:0.02,5:0.03}
# Audio ------------------------------------------------------ #
Cicadas = pygame.mixer.Sound('Data/SFX/Cicadas.wav')
Engines = pygame.mixer.Sound('Data/SFX/Engines.wav')
Wind_1 = pygame.mixer.Sound('Data/SFX/Wind_1.wav')
Wind_2 = pygame.mixer.Sound('Data/SFX/Wind_2.wav')
Wind_3 = pygame.mixer.Sound('Data/SFX/Wind_3.wav')
ShipCrack_1 = pygame.mixer.Sound('Data/SFX/ShipCrack_1.wav')
ShipCrack_2 = pygame.mixer.Sound('Data/SFX/ShipCrack_2.wav')
Punch_1 = pygame.mixer.Sound('Data/SFX/Punch_1.wav')
Punch_2 = pygame.mixer.Sound('Data/SFX/Punch_2.wav')
ShipExplosion = pygame.mixer.Sound('Data/SFX/ShipExplosion.wav')
SmashCharge = pygame.mixer.Sound('Data/SFX/SmashCharge.wav')
WarningSound = pygame.mixer.Sound('Data/SFX/Warning.wav')
SmashSound = pygame.mixer.Sound('Data/SFX/Smash.wav')
MorePower = pygame.mixer.Sound('Data/SFX/MorePower.wav')
PunchAttempt = pygame.mixer.Sound('Data/SFX/PunchAttempt.wav')
Shoot = pygame.mixer.Sound('Data/SFX/Shoot.wav')
Track_1 = pygame.mixer.Sound('Data/SFX/Track_1.wav')
pygame.mixer.set_num_channels(18)
# Colors ----------------------------------------------------- #
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY3 = (105,105,105)
GRAY = (195,195,195)
GRAY2 = (127,127,127)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GOLD = (255,215,0)
PURPLE = (115,0,242)
WIND = (90,75,103)
# Variables -------------------------------------------------- #
Right = False
Left = False
Smash = False
SmashTimer = 0
SmashAnimationTimer = 0
SmashAnimationStage = 0
global IslandLoc
IslandLoc = [50,100]
ResetGravity = False
Gravity = 2
Direction = 'r'
PlayerAnimationTimer = 0
PlayerAnimationState = 0
Jumps = 1
BackgroundTimer = 0
Power = 5000
WarningTimer = 0
Distance = 76
Particles = []
PowerParticles = []
Ships = []
Pirates = []
frame = 0
PlayerXMomentum = 0
Punching = 0
Stage = 0
ShipNamesSetup = {'Scout_Ship':15,'Platform':25,'Ambush':1}
ShipNames = []
ButtonProgress = [1,0,0]
Bullets = []
BIslands = []
MovementParticles = []
Stars = []
WindParticles = []
WindParticles2 = []
for Star in range(20):
    Stars.append([random.randint(0,300),random.randint(0,90),random.choice(StarImages)])
SHIPCHANCE = 120
SHIPMAX = 4
OnAShip = False
for Name in ShipNamesSetup:
    for time in range(ShipNamesSetup[Name]):
        ShipNames.append(Name)
ShipDatabase = {'Scout_Ship':[Scout_Ship,-1.5],'Platform':[Platform,-2],'Ambush':[Ambush,-3],'Speed_Bomber':[Speed_Bomber,-5],'Carrier':[Carrier,-1],'Fighter_Ship':[Fighter_Ship,-1.8],'Mother_Ship':[Mother_Ship,-0.7]}
#           stage, timer, timer cap, stage cap
TileAnimationTimers = {'z':[0,0,20,4],'y':[0,0,3,2],'x':[0,0,3,2],'v':[0,0,2,15]}
# Physics ---------------------------------------------------- #
def CollisionTest(Object1,ObjectList):
    CollisionList = []
    for Object in ObjectList:
        ObjectRect = pygame.Rect(Object[0],Object[1],Object[2],Object[3])
        if ObjectRect.colliderect(Object1):
            CollisionList.append(ObjectRect)
    return CollisionList
class PhysicsObject(object):
    def __init__(self):
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(0,0,self.width,self.height)
    def Move(self,Movement,platforms):
        ResetGravity = False
        self.rect.x += Movement[0]
        block_hit_list = CollisionTest(self.rect,platforms)
        for block in block_hit_list:
            if Movement[0] > 0:
                self.rect.right = block.left
            elif Movement[0] < 0:
                self.rect.left = block.right
        self.rect.y += Movement[1]
        block_hit_list = CollisionTest(self.rect,platforms)
        for block in block_hit_list:
            if Movement[1] > 0:
                self.rect.bottom = block.top
                ResetGravity = True
            elif Movement[1] < 0:
                self.rect.top = block.bottom
            self.change_y = 0
        return ResetGravity
    def Draw(self):
        pygame.draw.rect(Display,(0,0,255),self.rect)
    def CollisionItem(self):
        CollisionInfo = [self.rect.x,self.rect.y,self.width,self.height]
        return CollisionInfo
def GetTileCollision(TileGroup):
    PhysicalTiles = []
    for Tile in TileGroup:
        if Tiles[Tile[0]][2] == True:
            PhysicalTiles.append([Tile[1][0]+IslandLoc[0],Tile[1][1]+IslandLoc[1],8,8])
    return PhysicalTiles
# Font ------------------------------------------------------- #
def GenerateFont(FontImage,FontSpacing,TileSize):
    FontOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','.','-',',',':','+','\'','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','!','?','0','1','2','3','4','5','6','7','8','9']
    FontImage = pygame.image.load(FontImage).convert()
    FontImage.set_colorkey((255,255,255))
    num = 0
    for char in FontOrder:
        FontImage.set_clip(pygame.Rect(((TileSize+1)*num),0,TileSize,TileSize))
        CharacterImage = FontImage.subsurface(FontImage.get_clip())
        FontSpacing[char].append(CharacterImage)
        num += 1
    FontSpacing['Height'] = TileSize
    return FontSpacing
def ShowText(Text,X,Y,Spacing,WidthLimit,Font):
    OriginalX = X
    OriginalY = Y
    CurrentWord = ''
    for char in Text:
        if char not in [' ','\n']:
            try:
                Image = Font[str(char)][1]
                CurrentWord += str(char)
            except KeyError:
                pass
        else:
            WordTotal = 0
            for char2 in CurrentWord:
                WordTotal += Font[char2][0]
                WordTotal += Spacing
            if WordTotal+X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
            for char2 in CurrentWord:
                Image = Font[str(char2)][1]
                Display.blit(Image,(X,Y))
                X += Font[char2][0]
                X += Spacing
            if char == ' ':
                X += Font['A'][0]
                X += Spacing
            else:
                X = OriginalX
                Y += Font['Height']
            CurrentWord = ''
        if X-OriginalX > WidthLimit:
            X = OriginalX
            Y += Font['Height']
    return X,Y
Font_0 = {'A':[6],'B':[6],'C':[6],'D':[6],'E':[6],'F':[6],'G':[6],'H':[6],'I':[6],'J':[6],'K':[6],'L':[6],'M':[6],'N':[6],'O':[6],'P':[6],'Q':[6],'R':[6],'S':[6],'T':[6],'U':[6],'V':[6],'W':[6],'X':[6],'Y':[6],'Z':[6],
          '.':[3],'-':[6],',':[3],':':[3],'+':[6],'\'':[3],
          'a':[6],'b':[6],'c':[6],'d':[6],'e':[6],'f':[5],'g':[6],'h':[6],'i':[2],'j':[5],'k':[5],'l':[3],'m':[6],'n':[5],'o':[6],'p':[6],'q':[6],'r':[5],'s':[5],'t':[5],'u':[5],'v':[6],'w':[6],'x':[6],'y':[6],'z':[6],
          '!':[2],'?':[6],
          '0':[6],'1':[3],'2':[6],'3':[6],'4':[6],'5':[6],'6':[6],'7':[6],'8':[6],'9':[6]}
Font_0 = GenerateFont('Data/Font/Font.png',Font_0,11)
# Setup ------------------------------------------------------ #
PhysicalTiles = GetTileCollision(Island)
player = PhysicsObject()
player.rect = pygame.Rect(66,108,6,8)
# Setup Background ------------------------------------------- #
def NewIslands(BISLANDTOTAL,BIslandDistances):
    BIslands = []
    for whatever in range(4200):
        if random.randint(1,1000) == 1:
            choice = random.randint(0,BISLANDTOTAL)
            BIslands.append([300,130+random.randint(0,40),choice,BIslandDistances[choice]])
        for BIsland in BIslands:
            BIsland[0] -= BIsland[3]
            if random.randint(1,150) == 1:
                if random.randint(1,2) == 1:
                    BIsland[1] -= 1
                else:
                    BIsland[1] += 1
            if BIsland[0] < -100:
                BIslands.remove(BIsland)
    return BIslands
BIslands = NewIslands(BISLANDTOTAL,BIslandDistances)
# FPS -------------------------------------------------------- #
FPS = 80
TrueFPSCount = 0
TrueFPS = 0
fpsOn = False
PrevNow = 0
# Text -------------------------------------------------------- #
def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    screen.blit(textobj, textrect)
# Intro ------------------------------------------------------ #
num = 0
num2 = 0
Text = ''
IntroText = 'your homeland\'s economy has been threatened... you have been sent to retrieve an extremely valuable asset from a far away island. on your way back you notice that you\'re running out of power...                                                press x'
EndIntro = False
while (EndIntro == False):
    Display.fill(BLACK)
    num += 1
    if num == 2:
        num = 0
        if num2 < len(IntroText):
            Text += IntroText[num2]
        num2 += 1
    TextTemp = Text + ' '
    ShowText(TextTemp,50,50,1,200,Font_0)
    #ShowText('Follow Plz!    DaFluffyPotato ',117,188,1,200,Font_0)
    #Display.blit(Twitter,(192,186))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == ord('x'):
                EndIntro = True
    screen.blit(pygame.transform.scale(Display,(300*SCALE,200*SCALE)),(0,0))
    pygame.display.update()
    mainClock.tick(40)
# Loop ------------------------------------------------------- #
Cicadas.play(10000)
Cicadas.set_volume(0.1)
Engines.play(10000)
Winds = [Wind_1,Wind_2,Wind_3]
Cracks = [ShipCrack_1,ShipCrack_2]
Punches = [Punch_1,Punch_2]
Wind_1.set_volume(0.15)
Wind_2.set_volume(0.15)
Wind_3.set_volume(0.15)
ShipCrack_1.set_volume(0.7)
ShipCrack_2.set_volume(0.7)
WarningSound.set_volume(0.2)
SmashSound.set_volume(0.3)
PunchAttempt.set_volume(0.1)
Shoot.set_volume(0.6)
Track_1.set_volume(0.9)
MorePower.set_volume(0.2)
Track_1.play(10000)
while True:
    # Background ---------------------------------------------- #
    if random.randint(1,80) == 1:
        random.choice(Winds).play()
    frame += 1
    Display.fill(BLACK)
    BackgroundTimer += 1
    if BackgroundTimer > 2:
        BackgroundTimer = 0
    Display.blit(BackgroundImage,(-BackgroundTimer,0))
    if random.randint(1,1000) == 1:
        choice = random.randint(0,BISLANDTOTAL)
        BIslands.append([300,130+random.randint(0,40),choice,BIslandDistances[choice]])
    for BIsland in BIslands:
        BIsland[0] -= BIsland[3]
        if random.randint(1,150) == 1:
            if random.randint(1,2) == 1:
                BIsland[1] -= 1
            else:
                BIsland[1] += 1
        Display.blit(BIslandImages[BIsland[2]],(BIsland[0],BIsland[1]))
        if BIsland[0] < -100:
            BIslands.remove(BIsland)
    for Star in Stars:
        if random.randint(1,150) == 1:
            Star[2] = random.choice(StarImages)
        Display.blit(Star[2],(Star[0],Star[1]))
    if random.randint(1,2) == 1:
        if random.randint(1,2) == 1:
            WindParticles.append([300,random.randint(0,200),random.randint(2,20),random.randint(5,9)])
        else:
            WindParticles2.append([300,random.randint(0,200),random.randint(2,20),random.randint(7,11)])
    for Particle in WindParticles:
        Particle[0] -= Particle[3]
        ParticleSurface = pygame.Surface((Particle[2],1))
        ParticleSurface.fill((255,255,255))
        ParticleSurface.set_alpha(50)
        Display.blit(ParticleSurface,(Particle[0],Particle[1]))
        if Particle[0] < -20:
            WindParticles.remove(Particle)
    # Update Tile Animations --------------------------------- #
    for Timer in TileAnimationTimers:
        TileAnimationTimers[Timer][1] += 1
        if TileAnimationTimers[Timer][1] >= TileAnimationTimers[Timer][2]:
            TileAnimationTimers[Timer][1] = 0
            TileAnimationTimers[Timer][0] += 1
            if TileAnimationTimers[Timer][0] > TileAnimationTimers[Timer][3]:
                TileAnimationTimers[Timer][0] = 0
    # Add Ships ---------------------------------------------- #
    if random.randint(1,SHIPCHANCE) == 1:
        if len(Ships) < SHIPMAX:
            ShipType = random.choice(ShipNames)
            Ships.append([ShipType,ShipDatabase[ShipType][0].copy(),ShipDatabase[ShipType][1]+random.randint(1,10)/10,300,random.randint(40,120),300])
    # Island Movement ---------------------------------------- #
    inum = 0
    if random.randint(1,50) == 1:
        inum = random.randint(3,4)
        if inum == 3:
            IslandLoc[1] += 1
        else:
            IslandLoc[1] -= 1
        if IslandLoc[1] < 95:
            IslandLoc[1] = 95
        if Power > 0:
            if IslandLoc[1] > 105:
                IslandLoc[1] -= 1
        PhysicalTiles = GetTileCollision(Island)
    # Ship Movement ------------------------------------------ #
    for Ship in Ships:
        Ship[5] = int(Ship[3])
        Ship[3] += Ship[2]
        if Ship[3] < - 200:
            Ships.remove(Ship)
        if Ship[3] > 300:
            Ships.remove(Ship)
        xChange = int(Ship[3])-Ship[5]
        Ship[5] = xChange
    # Display Tiles ------------------------------------------ #
    Shot = False
    for Ship in Ships:
        for Tile in Ship[1]:
            if Tile[0] not in ['w','u']:
                if Tiles[Tile[0]][0] != True:
                    Display.blit(Tiles[Tile[0]][1],(Tile[1][0]+int(Ship[3]),Tile[1][1]+Ship[4]))
                else:
                    Display.blit(Tiles[Tile[0]][1][TileAnimationTimers[Tile[0]][0]],(Tile[1][0]+int(Ship[3]),Tile[1][1]+Ship[4]))
                    if Tile[0] == 'v':
                        if TileAnimationTimers['v'][0] == 2:
                            if TileAnimationTimers['v'][1] == 0:
                                Bullets.append([Tile[1][0]+Ship[3],Tile[1][1]+Ship[4]+3])
                                if Shot == False:
                                    Shot = True
                                    Shoot.play()
            else:
                # x, y, type, animation timer, animation stage, direction, gravity, grounded, death
                if Tile[0] == 'w':
                    Pirates.append([Tile[1][0]+Ships[-1][3],Tile[1][1]+Ships[-1][4],'melee',0,0,'l',2,True,0])
                elif Tile[0] == 'u':
                    Pirates.append([Tile[1][0]+Ships[-1][3],Tile[1][1]+Ships[-1][4],'runner',0,0,'l',2,True,0])
                if ButtonProgress[1] == 0:
                    ButtonProgress[1] = 1
                Ship[1].remove(Tile)
    # Particles ---------------------------------------------- #
    for Particle in Particles:
        ParticleSurface = pygame.Surface((Particle[5][0],Particle[5][1]))
        ParticleSurface.fill(Particle[2])
        if Particle[4] < 0.1:
            Particle[4] += 0.005
        else:
            Particle[4] += 1
        if Particle[3][0] == 0:
            Particle[3][0] = 0.2
        Particle[0] += Particle[3][0]*Particle[4]
        Particle[1] += Particle[3][1]*Particle[4]
        Display.blit(ParticleSurface,(int(Particle[0]),int(Particle[1])))
        try:
            if Particle[0] > 300:
                Particles.remove(Particle)
            if Particle[0] < -10:
                Particles.remove(Particle)
            if Particle[1] > 200:
                Particles.remove(Particle)
            if Particle[1] < -10:
                Particles.remove(Particle)
        except ValueError:
            pass
        if Particle[4] > 12:
            if Particle[2] == (51,120,115,255):
                PowerParticles.append([Particle[0],Particle[1],(14-Particle[0])/100,(170-Particle[1])/100,1])
                try:
                    Particles.remove(Particle)
                except:
                    pass
    for Particle in PowerParticles:
        Particle[4] += 0.25
        Particle[0] += Particle[2]*Particle[4]
        Particle[1] += Particle[3]*Particle[4]
        Display.blit(PowerParticle,(int(Particle[0]),int(Particle[1])))
        PowerParticleR = pygame.Rect(Particle[0],Particle[1],4,4)
        CrystalR = pygame.Rect(10,165,8,26)
        if PowerParticleR.colliderect(CrystalR):
            Power += 200
            MorePower.play()
            PowerParticles.remove(Particle)
    for Particle in MovementParticles:
        if Particle[0] == 'turn':
            ParticleImage = TurnAnimation[int(Particle[4]/2)].copy()
            if Particle[3] == 'l':
                ParticleImage = pygame.transform.flip(ParticleImage,True,False)
            Display.blit(ParticleImage,(Particle[1],Particle[2]))
            Particle[4] += 1
            if Particle[4] > 16:
                MovementParticles.remove(Particle)
        if Particle[0] == 'jump':
            ParticleImage = JumpAnimation[int(Particle[4])].copy()
            if Particle[3] == 'l':
                ParticleImage = pygame.transform.flip(ParticleImage,True,False)
            Display.blit(ParticleImage,(Particle[1],Particle[2]))
            Particle[4] += 1
            if Particle[4] > 13:
                MovementParticles.remove(Particle)
    # Pirates ------------------------------------------------ #
    for Pirate in Pirates:
        PirateObj = PhysicsObject()
        PirateObj.rect = pygame.Rect(Pirate[0],Pirate[1],7,7)
        PreGrav = PirateObj.rect.y
        PirateMovement = [0,0]
        PirateMovement[1] += Pirate[6]
        DistanceX = player.rect.x-PirateObj.rect.x
        DistanceY = player.rect.y-PirateObj.rect.y
        SPEED = 2
        JUMP = 4
        if Pirate[2] == 'runner':
            SPEED = 6
            JUMP = 3
        if Pirate[8] == 0:
            if abs(DistanceX)+abs(DistanceY) < 130:
                if DistanceX < -4:
                    PirateMovement[0] = -SPEED
                    if Pirate[5] == 'r':
                        if Pirate[7] == True:
                            MovementParticles.append(['turn',PirateObj.rect.x+6,PirateObj.rect.y+3,'r',0])
                    Pirate[5] = 'l'
                elif DistanceX > 4:
                    PirateMovement[0] = SPEED
                    if Pirate[5] == 'l':
                        if Pirate[7] == True:
                            MovementParticles.append(['turn',PirateObj.rect.x-5,PirateObj.rect.y+3,'l',0])
                    Pirate[5] = 'r'
                else:
                    if Pirate[7] == True:
                        MovementParticles.append(['jump',PirateObj.rect.x-3,PirateObj.rect.y,'r',0])
                        PirateMovement[1] = -JUMP
                        Pirate[6] = -JUMP
                if Pirate[7] == True:
                    if DistanceY < -1:
                        MovementParticles.append(['jump',PirateObj.rect.x-3,PirateObj.rect.y,'r',0])
                        PirateMovement[1] = -JUMP
                        Pirate[6] = -JUMP
        PirateGravityReset = False
        PirateGravityReset = PirateObj.Move(PirateMovement,PhysicalTiles)
        for Ship in Ships:
            for Tile in Ship[1]:
                if Tile[0] in ['9','8','7']:
                    TileR = pygame.Rect(Tile[1][0]+int(Ship[3]),Tile[1][1]+Ship[4],8,8)
                    if PirateObj.rect.colliderect(TileR):
                        if PirateMovement[1] > 0:
                            if PreGrav < Tile[1][1]+Ship[4]-6:
                                PirateGravityReset = True
                                PirateObj.rect.y = Tile[1][1]+Ship[4]-8
                                PirateObj.rect.x += Ship[5]
        if PirateGravityReset == True:
            Pirate[7] = True
            Pirate[6] = 2
        else:
            Pirate[7] = False
        Pirate[6] += 0.25
        if Pirate[6] > 4:
            Pirate[6] = 4
        if Pirate[8] > 0:
            Pirate[8] += 1
        Pirate[3] += 1
        if Pirate[3] == 4:
            Pirate[3] = 0
            Pirate[4] += 1
            if Pirate[4] > 2:
                Pirate[4] = 0
        if PirateMovement[0] == 0:
            Pirate[4] = 0
            Pirate[3] = 3
        if Pirate[2] == 'melee':
            PirateImage = MeleePirate[Pirate[4]]
            if Pirate[8] > 0:
                DeathSub = Pirate[8]
                if DeathSub > 12:
                    DeathSub = 12
                PirateImage = MeleePirateDeath[int(DeathSub/2)]
            if PirateObj.rect.colliderect(player.rect):
                if Punching < 15:
                    if Pirate[8] == 0:
                        if SmashTimer == 0:
                            if Pirate[0] > player.rect.x:
                                PlayerXMomentum = -4
                            else:
                                PlayerXMomentum = 4
                            random.choice(Punches).play()
                else:
                    if Pirate[8] == 0:
                        random.choice(Punches).play()
                    if Pirate[8] == 0:
                        Pirate[8] = 1
                    Pirate[6] = -2
                    ButtonProgress[1] = 40
        if Pirate[2] == 'runner':
            PirateImage = RunnerPirate[Pirate[4]]
            if Pirate[8] > 0:
                DeathSub = Pirate[8]
                if DeathSub > 12:
                    DeathSub = 12
                PirateImage = RunnerPirateDeath[int(DeathSub/2)]
            if PirateObj.rect.colliderect(player.rect):
                if Punching < 15:
                    if Pirate[8] == 0:
                        if SmashTimer == 0:
                            if Pirate[0] > player.rect.x:
                                PlayerXMomentum = -3
                            else:
                                PlayerXMomentum = 3
                            random.choice(Punches).play()
                else:
                    if Pirate[8] == 0:
                        random.choice(Punches).play()
                    if Pirate[8] == 0:
                        Pirate[8] = 1
                    Pirate[6] = -2
                    ButtonProgress[1] = 40
        if Pirate[5] == 'l':
            PirateImage = PirateImage.copy()
            PirateImage = pygame.transform.flip(PirateImage,True,False)
        Display.blit(PirateImage,(int(PirateObj.rect.x),PirateObj.rect.y))
        Pirate[0] = PirateObj.rect.x
        Pirate[1] = PirateObj.rect.y
        if Pirate[1] > 200:
            Pirates.remove(Pirate)
        if Pirate[8] > 400:
            Pirates.remove(Pirate)
    # Bullets ------------------------------------------------ #
    for Bullet in Bullets:
        Bullet[0] -= 10
        Display.blit(BulletImage,(Bullet[0],Bullet[1]))
        BulletR = pygame.Rect(Bullet[0],Bullet[1],7,2)
        if player.rect.colliderect(BulletR):
            PlayerXMomentum = -7
            Bullets.remove(Bullet)
        elif Bullet[0] < -7:
            Bullets.remove(Bullet)
    # Player Movement ---------------------------------------- #
    if Punching > 0:
        Punching -= 1
    Movement = [0,0]
    if Right == True:
        Movement[0] += 2
        if Direction == 'l':
            if ResetGravity == True:
                MovementParticles.append(['turn',player.rect.x+1,player.rect.y+4,'l',0])
        Direction = 'r'
    if Left == True:
        Movement[0] -= 2
        if Direction == 'r':
            if ResetGravity == True:
                MovementParticles.append(['turn',player.rect.x+1,player.rect.y+4,'r',0])
        Direction = 'l'
    Movement[0] += PlayerXMomentum
    if PlayerXMomentum > 0:
        PlayerXMomentum -= 0.5
    elif PlayerXMomentum < 0:
        PlayerXMomentum += 0.5
    PreGrav = player.rect.y
    Movement[1] += int(Gravity)
    if ResetGravity == True:
        if inum == 4:
            player.rect.y -= 1
        if inum == 3:
            player.rect.y += 1
    if IslandLoc[1] > 105:
        if Power > 0:
            player.rect.y -= 2.5
    if SmashTimer != 0:
        if SmashTimer > 18:
            if random.randint(1,5) == 1:
                random.choice(Cracks).play()
        if SmashTimer == 8:
            ShipExplosion.play()
            SmashSound.play()
        SmashTimer -= 1
        Movement = [0,0]
    ResetGravity = False
    ResetGravity = player.Move(Movement,PhysicalTiles)
    OnAShip = False
    for Ship in Ships:
        SmashShip = False
        for Tile in Ship[1]:
            if Tile[0] in ['9','8','7']:
                TileR = pygame.Rect(Tile[1][0]+int(Ship[3]),Tile[1][1]+Ship[4],8,8)
                if player.rect.colliderect(TileR):
                    if Movement[1] > 0:
                        if PreGrav < Tile[1][1]+Ship[4]-7:
                            ResetGravity = True
                            OnAShip = True
                            if ButtonProgress[2] == 0:
                                ButtonProgress[2] = 1
                            Gravity = 2
                            Jumps = 1
                            player.rect.y = Tile[1][1]+Ship[4]-8
                            player.rect.x += Ship[5]
                            if Smash == True:
                                ButtonProgress[2] = 40
                                random.choice(Cracks).play()
                                SmashCharge.play()
                                SmashShip = True
                                SmashTimer = 66
                                SmashAnimationTimer = 0
                                SmashAnimationStage = 0
        if SmashShip == True:
            PARTICLE_PER_TILE = 64
            for Tile in Ship[1]:
                x = 0
                y = 0
                for whatever in range(PARTICLE_PER_TILE):
                    try:
                        Color = Tiles[Tile[0]][1].get_at((x,y))
                    except AttributeError:
                        Color = Tiles[Tile[0]][1][0].get_at((x,y))
                    if Color[0] != 255:
                        # x, y, color, direction, speed, size
                        Particles.append([Tile[1][0]+Ship[3]+x,Tile[1][1]+Ship[4]+y,Color,[(random.randint(1,20)-10)/10,(random.randint(1,20)-10)/10],-0.2,[1,1]])
                    x += 1
                    if x > 7:
                        x = 0
                        y += 1
            Ships.remove(Ship)
    if SmashTimer == 0:
        if ResetGravity == True:
            Gravity = 2
            Jumps = 1
        else:
            Gravity += 0.25
            if Gravity > 4:
                Gravity = 4
    PlayerAnimationTimer += 1
    if PlayerAnimationTimer == 4:
        PlayerAnimationTimer = 0
        PlayerAnimationState += 1
        if PlayerAnimationState > 2:
            PlayerAnimationState = 0
    if Movement[0] == 0:
        PlayerAnimationState = 0
        PlayerAnimationTimer = 3
    PlayerImage = PlayerImages[PlayerAnimationState]
    if Punching > 12:
        PunchingImage = SidePunch[25-Punching].copy()
    if Direction == 'l':
        PlayerImage = PlayerImage.copy()
        PlayerImage = pygame.transform.flip(PlayerImage,True,False)
        if Punching > 12:
            PunchingImage = PunchingImage.copy()
            PunchingImage = pygame.transform.flip(PunchingImage,True,False)
    Display.blit(PlayerImage,(int(player.rect.x),player.rect.y))
    if Punching > 12:
        Display.blit(PunchingImage,(int(player.rect.x)-2,player.rect.y))
    if SmashTimer != 0:
        SmashAnimationTimer += 1
        if SmashAnimationTimer == 3:
            SmashAnimationTimer = 0
            SmashAnimationStage += 1
            if SmashAnimationStage > 22:
                SmashAnimationStage = 22
        if SmashAnimationStage >= 19:
            Display.blit(OuterSmashAnimation[OuterTimer],(int(player.rect.x)-1,player.rect.y-2))
            OuterTimer += 1
            if OuterTimer > 9:
                OuterTimer = 9
        Display.blit(SmashAnimation[SmashAnimationStage],(int(player.rect.x),player.rect.y+2))
    else:
        OuterTimer = 0
    # Display Tiles ------------------------------------------ #
    for Tile in Island:
        if Tiles[Tile[0]][0] != True:
            Display.blit(Tiles[Tile[0]][1],(Tile[1][0]+IslandLoc[0],Tile[1][1]+IslandLoc[1]))
        else:
            Display.blit(Tiles[Tile[0]][1][TileAnimationTimers[Tile[0]][0]],(Tile[1][0]+IslandLoc[0],Tile[1][1]+IslandLoc[1]))
    # Wind --------------------------------------------------- #
    for Particle in WindParticles2:
        Particle[0] -= Particle[3]
        ParticleSurface = pygame.Surface((Particle[2],1))
        ParticleSurface.fill((255,255,255))
        ParticleSurface.set_alpha(50)
        Display.blit(ParticleSurface,(Particle[0],Particle[1]))
        if Particle[0] < -20:
            WindParticles2.remove(Particle)
    # Show Help ---------------------------------------------- #
    if ButtonProgress[0] > 0:
        if ButtonProgress[0] < 40:
            ButtonProgress[0] += 1
            if ButtonProgress[0] == 40:
                ButtonProgress[0] = 1
            if ButtonProgress[0] < 20:
                Display.blit(MovementHelp[0],(player.rect.x-9,player.rect.y-9))
            else:
                Display.blit(MovementHelp[1],(player.rect.x-9,player.rect.y-9))
    if ButtonProgress[1] > 0:
        if ButtonProgress[1] < 40:
            ButtonProgress[1] += 1
            if ButtonProgress[1] == 40:
                ButtonProgress[1] = 1
            if ButtonProgress[1] < 20:
                Display.blit(CombatHelp[0],(player.rect.x-9,player.rect.y-9))
            else:
                Display.blit(CombatHelp[1],(player.rect.x-9,player.rect.y-9))
    if ButtonProgress[2] > 0:
        if ButtonProgress[2] < 40:
            ButtonProgress[2] += 1
            if ButtonProgress[2] == 40:
                ButtonProgress[2] = 1
            num = 0
            if ButtonProgress[1] > 0:
                if ButtonProgress[1] < 40:
                    num = 10
            if ButtonProgress[2] < 20:
                Display.blit(DestroyHelp[0],(player.rect.x,player.rect.y-9-num))
            else:
                Display.blit(DestroyHelp[1],(player.rect.x,player.rect.y-9-num))
            if OnAShip == False:
                ButtonProgress[2] = 0
    # Display Progress Bar ----------------------------------- #
    Display.blit(ProgressBar,(200,4))
    Display.blit(Progress,(278-int(Distance),5))
    if Distance < 50:
        if Stage == 0:
            Stage = 1
            ShipNamesSetup = {'Scout_Ship':15,'Platform':20,'Ambush':3,'Speed_Bomber':20,'Fighter_Ship':10}
            ShipNames = []
            for Name in ShipNamesSetup:
                for time in range(ShipNamesSetup[Name]):
                    ShipNames.append(Name)
        if Distance < 40:
            if Stage == 1:
                Stage = 2
                ShipNamesSetup = {'Scout_Ship':15,'Platform':20,'Ambush':2,'Speed_Bomber':30,'Carrier':8,'Fighter_Ship':30}
                ShipNames = []
                for Name in ShipNamesSetup:
                    for time in range(ShipNamesSetup[Name]):
                        ShipNames.append(Name)
        if Distance < 30:
            if Stage == 2:
                Stage = 3
                ShipNamesSetup = {'Scout_Ship':5,'Platform':4,'Ambush':6,'Speed_Bomber':12,'Carrier':10,'Fighter_Ship':30,'Mother_Ship':3}
                ShipNames = []
                for Name in ShipNamesSetup:
                    for time in range(ShipNamesSetup[Name]):
                        ShipNames.append(Name)
        if Distance < 15:
            if Stage == 3:
                Stage = 4
                SHIPCHANCE = 10
                SHIPMAX = 6
                ShipNamesSetup = {'Scout_Ship':2,'Platform':1,'Ambush':12,'Speed_Bomber':6,'Carrier':12,'Fighter_Ship':18,'Mother_Ship':8}
                ShipNames = []
                for Name in ShipNamesSetup:
                    for time in range(ShipNamesSetup[Name]):
                        ShipNames.append(Name)
        if Distance < 5:
            if Stage == 4:
                Stage = 5
                SHIPCHANCE = 1000
                SHIPMAX = 0
                ShipNamesSetup = {'Scout_Ship':2,'Platform':1,'Ambush':12,'Speed_Bomber':6,'Carrier':12,'Fighter_Ship':18,'Mother_Ship':8}
                ShipNames = []
                for Name in ShipNamesSetup:
                    for time in range(ShipNamesSetup[Name]):
                        ShipNames.append(Name)
    Distance -= 0.01
    # Display Power Crystal ---------------------------------- #
    if Power > 10000:
        Power = 10000
    PowerAmount = int(Power/10000*26)
    WhitePanel = pygame.Surface((10,26-PowerAmount+1))
    WhitePanel.fill(WHITE)
    CrystalValue = CrystalValueMain.copy()
    CrystalValue.blit(WhitePanel,(0,0))
    CrystalValue.set_colorkey((255,255,255))
    Display.blit(CrystalBase,(10,165))
    Display.blit(CrystalValue,(10,165))
    Display.blit(CrystalTop,(10,165))
    Power -= 2
    if PowerAmount < 5:
        WarningTimer += 1
        if WarningTimer >= 40:
            WarningTimer = 0
        if WarningTimer > 10:
            Display.blit(WarningImage,(25,175))
            if WarningTimer == 11:
                WarningSound.play()
    if Power <= 0:
        Power = 0
        IslandLoc[1] += 0.25
        PhysicalTiles = GetTileCollision(Island)
    elif IslandLoc[1] > 105:
        IslandLoc[1] -= 0.5
        PhysicalTiles = GetTileCollision(Island)
    # FPS ---------------------------------------------------- #
    NewSec = False
    TrueFPSCount += 1
    now = datetime.now()
    now = now.second
    if PrevNow != now:
        PrevNow = now
        NewSec = True
        TrueFPS = TrueFPSCount
        TrueFPSCount = 0
        TrueFPS = str(TrueFPS)
    # Buttons ------------------------------------------------ #
    Smash = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_F11:
                if fullscreen == False:
                    fullscreen = True
                    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.FULLSCREEN)
                else:
                    fullscreen = False
                    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT:
                Right = True
            if event.key == K_LEFT:
                Left = True
            if event.key == K_DOWN:
                Smash = True
            if event.key == ord('x'):
                if Jumps > 0:
                    Jumps -= 1
                    Gravity = -4
                    ButtonProgress[0] = 40
                    MovementParticles.append(['jump',player.rect.x-3,player.rect.y,'r',0])
            if event.key == ord('c'):
                if Punching == 0:
                    PunchAttempt.play()
                    Punching = 25
                    if Direction == 'r':
                        PlayerXMomentum = 5
                    else:
                        PlayerXMomentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                Right = False
            if event.key == K_LEFT:
                Left = False
    # Update ------------------------------------------------- #
    if fpsOn == True:
        drawText('FPS:'+(TrueFPS)+'', basicFont, WHITE, screen, 500,12)
    if Distance <= 0:
        OldDisplay = Display.copy()
        BlackPanel = pygame.Surface((300,200))
        BlackPanel.fill((BLACK))
        num = 0
        num2 = 0
        num3 = 0
        Text = ''
        OutroText = 'you successfully delivered the crystal and you were paid for your tough journey.                                                    press x'
        EndIntro = False
        while True:
            Display.blit(OldDisplay,(0,0))
            num += 2.55
            if num > 255:
                num = 255
            BlackPanel.set_alpha(int(num))
            Display.blit(BlackPanel,(0,0))
            if num == 255:
                num2 += 1
                if num2 == 2:
                    num2 = 0
                    if num3 < len(OutroText):
                        Text += OutroText[num3]
                    num3 += 1
                TextTemp = Text + ' '
                ShowText(TextTemp,50,50,1,200,Font_0)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if num == 255:
                        if event.key == ord('x'):
                            pygame.quit()
                            sys.exit()
            screen.blit(pygame.transform.scale(Display,(300*SCALE,200*SCALE)),(0,0))
            pygame.display.update()
            mainClock.tick(40)
    if player.rect.y > 200:
        AlphaSurface = pygame.Surface((300,200)).convert()
        AlphaSurface.fill(BLACK)
        AlphaSurface.set_alpha(100)
        Display.blit(AlphaSurface,(0,0))
        ShowText('you have failed ',100,70,1,200,Font_0)
        ShowText('press r ',125,90,1,200,Font_0)
        screen.blit(pygame.transform.scale(Display,(300*SCALE,200*SCALE)),(0,0))
        pygame.display.update()
        Dead = True
        while Dead:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    if event.key == ord('r'):
                        Right = False
                        Left = False
                        Smash = False
                        SmashTimer = 0
                        SmashAnimationTimer = 0
                        SmashAnimationStage = 0
                        IslandLoc = [50,100]
                        ResetGravity = False
                        Gravity = 2
                        Direction = 'r'
                        PlayerAnimationTimer = 0
                        PlayerAnimationState = 0
                        Jumps = 1
                        BackgroundTimer = 0
                        Power = 5000
                        WarningTimer = 0
                        Distance = 76
                        Particles = []
                        PowerParticles = []
                        Ships = []
                        Pirates = []
                        frame = 0
                        PlayerXMomentum = 0
                        Punching = 0
                        PhysicalTiles = GetTileCollision(Island)
                        player = PhysicsObject()
                        player.rect = pygame.Rect(66,108,6,8)
                        Dead = False
                        Stage = 0
                        Bullets = []
                        ShipNamesSetup = {'Scout_Ship':10,'Platform':30,'Ambush':1}
                        ShipNames = []
                        MovementParticles = []
                        Stars = []
                        WindParticles = []
                        WindParticles2 = []
                        for Star in range(20):
                            Stars.append([random.randint(0,300),random.randint(0,90),random.choice(StarImages)])
                        SHIPCHANCE = 120
                        SHIPMAX = 4
                        for Name in ShipNamesSetup:
                            for time in range(ShipNamesSetup[Name]):
                                ShipNames.append(Name)
                        BIslands = NewIslands(BISLANDTOTAL,BIslandDistances)
                        
    screen.blit(pygame.transform.scale(Display,(300*SCALE,200*SCALE)),(0,0))
    pygame.display.update()
    mainClock.tick(40)
    
