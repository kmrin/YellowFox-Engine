# Imports
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import sys
import copy
import json
import time as Time
import xml.etree.ElementTree as ET
from pygame import *
from random import *

# Load content index and settings
with open('data/parameters/index.json') as i:
    content = json.load(i)
    launchParameters = content['launchParameters']
    songList = content['songs']
    noteStyles = content['notes']
    mdata = content['mdata']
    currVersion = mdata['currVersion']
with open('data/parameters/options.json') as x:
    arguments = json.load(x)

# Init pygame
init()

# Clock goes tic tac
clock = time.Clock()

# Launch main game screen with current settings
width = launchParameters['width']
height = launchParameters['height']
antiAliasing = launchParameters['antiAliasing']
potatoMode = launchParameters['potatoMode']
skipIntro = launchParameters['skipIntro']
skipCountdown = launchParameters['skipCountdown']

renderResolution = (1600, 900)
displayResolution = (width, height)

renderSurface = Surface(renderResolution)
scaledWindow = display.set_mode(displayResolution)

# Window properties
display.set_caption(f'YellowFox Engine | {currVersion}')

# Disable mouse
mouse.set_visible(False)

# Load fonts
SysFont10 = font.Font('data/fonts/unispace-regular.otf', 10)
SysFont15 = font.Font('data/fonts/unispace-regular.otf', 15)
SysFont20 = font.Font('data/fonts/unispace-regular.otf', 20)
SysFont25 = font.Font('data/fonts/unispace-regular.otf', 25)
SysFont30 = font.Font('data/fonts/unispace-regular.otf', 30)
SysFont40 = font.Font('data/fonts/unispace-regular.otf', 40)
SysFont50 = font.Font('data/fonts/unispace-regular.otf', 50)
SysFont60 = font.Font('data/fonts/unispace-regular.otf', 60)
SysFont70 = font.Font('data/fonts/unispace-regular.otf', 70)
SysFont80 = font.Font('data/fonts/unispace-regular.otf', 80)
SysFont90 = font.Font('data/fonts/unispace-regular.otf', 90)
FNFFont70 = font.Font('data/fonts/phantommuff.ttf', 70)
FNFFont80 = font.Font('data/fonts/phantommuff.ttf', 80)
FNFFont90 = font.Font('data/fonts/phantommuff.ttf', 90)
FNFFont100 = font.Font('data/fonts/phantommuff.ttf', 100)
FNFFont110 = font.Font('data/fonts/phantommuff.ttf', 110)
FNFFont120 = font.Font('data/fonts/phantommuff.ttf', 120)

# Volume text animation variables
volFadeDuration = 1000
volFadeTimer = 0
volFadeAlpha = 0
volFadeIn = False
volFadeOut = False

# Game variables
running = True
middleScreen = 1600 // 2, 900 // 2
currentW = 1600
currentH = 900
volume = 0.2
currentMenu = 'Main'
selectedSong = 0
selectedOption = 0
selectedMain = 0
selectedKeybind = 0
preventDoubleEnter = False
Inst = None
Vocals = None
chart = None
misses = 0
health = 50
BG = None
opponentAnimation = ['Up', -10]
playerAnimation = ['Up', -10]
hasPlayedMicDrop = False
combo = 0
bpm = 60000 / 100
arrow1Alpha = 1
arrow2Aplha = 1
character1 = None
character2 = None
character1Alpha = 1
character2Alpha = 1
currentTime = 0
paused = False
startupRan = False
frameTimer = 0
singlePlayer = False
sceneLoaded = False

# Set menu background
if antiAliasing:
    menuBG = transform.smoothscale(image.load('data/ui/menu/bg.png'), (currentW, currentH))
else:
    menuBG = transform.scale(image.load('data/ui/menu/bg.png'), (currentW, currentH))
rectBG = menuBG.get_rect()
rectBG.center = (middleScreen[0], middleScreen[1])

# Set menu images
if antiAliasing:
    fnfLogo = transform.smoothscale(image.load('data/ui/menu/logo.png'), (525, 365))
else:
    fnfLogo = transform.scale(image.load('data/ui/menu/logo.png'), (525, 365))
fnfLogoRect = fnfLogo.get_rect()
fnfLogoRect.center = (middleScreen[0] - 465, middleScreen[1] - 180)
playBtn = image.load('data/ui/menu/playButton.png')
playBtnRect = playBtn.get_rect()
playBtnRect.center = (middleScreen[0] - 510, middleScreen[1] + 90)
optionsBtn = image.load('data/ui/menu/optionsButton.png')
optionsBtnRect = optionsBtn.get_rect()
optionsBtnRect.center = (middleScreen[0] - 410, middleScreen[1] + 260)
optionHighligher = image.load('data/ui/menu/optionHighlighter.png')
optionHighligherRect = optionHighligher.get_rect()
optionHighligherRect.center = (middleScreen[0] - 705, middleScreen[1] + 90)

# Set menu rects
topRect = Surface((1600, 65), SRCALPHA)
bottomRect = Surface((1600, 65), SRCALPHA)
topRect.fill((0, 0, 0, 128))
bottomRect.fill((0, 0, 0, 128))
rects_x = 0
topRectY = currentH - 900
bottomRectY = currentH - 65

# Set info text
infoText = SysFont30.render('YellowFox Engine', True, (255, 255, 255))
infoText2 = SysFont30.render(f'{currVersion} by rin', True, (255, 255, 255))

# Start-up time
startTime = time.get_ticks()

# Loading screen
def loadingScreen():
    loadingText = FNFFont70.render('Loading...', 1, (255, 255, 255))
    renderSurface.fill((20, 20, 20))
    renderSurface.blit(loadingText, (50, currentH - 120))
    if antiAliasing:
        scaledSurface = transform.smoothscale(renderSurface, displayResolution)
    else:
        scaledSurface = transform.scale(renderSurface, displayResolution)
    scaledWindow.blit(scaledSurface, (0, 0))
    display.flip()

# Draw startup sequence
def startup():
    global startupRan
    global skipIntro
    if not skipIntro and not startupRan:
        startUpScreen()
    startupRan = True

# Startup screen
def startUpScreen():
    finalText = FNFFont100.render('YellowFox Engine', 1, (255, 255, 255))
    finalTextShadow = FNFFont110.render('YellowFox Engine', 1, (20, 20, 20))
    finalTextRect = finalText.get_rect()
    finalTextShadowRect = finalTextShadow.get_rect()
    finalTextRect.center = (middleScreen[0], middleScreen[1])
    finalTextShadowRect.center = (middleScreen[0], middleScreen[1])

    # Startup texts
    texts = [
        ("rin presents...", SysFont60),
        ("friday night funkin'", SysFont60),
        ("but it runs on pygame!", SysFont60),
        ("why tho?", SysFont60),
        ("shoutout to EnderSteve!", SysFont60)
    ]

    # Draw bg
    renderSurface.blit(menuBG, rectBG)

    # Translucent rectangle
    rectangle = Surface((1600, 160), SRCALPHA)
    rectangle.fill((0, 0, 0, 128))
    rect_x = 0
    rect_y = middleScreen[1] - 80
    renderSurface.blit(rectangle, (rect_x, rect_y))

    # Draw shadows
    for text, font in texts:
        textRender = font.render(text, 1, (255, 255, 255))
        textRect = textRender.get_rect()
        textRect.center = (middleScreen[0], middleScreen[1])

        renderSurface.blit(textRender, textRect)
        if antiAliasing:
            scaledSurface = transform.smoothscale(renderSurface, displayResolution)
        else:
            scaledSurface = transform.scale(renderSurface, displayResolution)
        scaledWindow.blit(scaledSurface, (0, 0))
        display.flip()
        Time.sleep(1.5)
        renderSurface.blit(menuBG, rectBG)
        renderSurface.blit(rectangle, (rect_x, rect_y))
        if antiAliasing:
            scaledSurface = transform.smoothscale(renderSurface, displayResolution)
        else:
            scaledSurface = transform.scale(renderSurface, displayResolution)
        scaledWindow.blit(scaledSurface, (0, 0))
        display.flip()

    # Render final text
    renderSurface.blit(menuBG, rectBG)
    renderSurface.blit(rectangle, (rect_x, rect_y))
    renderSurface.blit(finalTextShadow, finalTextShadowRect)
    renderSurface.blit(finalText, finalTextRect)
    if antiAliasing:
        scaledSurface = transform.smoothscale(renderSurface, displayResolution)
    else:
        scaledSurface = transform.scale(renderSurface, displayResolution)
    scaledWindow.blit(scaledSurface, (0, 0))
    display.flip()
    Time.sleep(1.6)

# Draw main menu
def drawMain():
    # Draw logo and buttons
    renderSurface.blit(fnfLogo, fnfLogoRect)
    renderSurface.blit(playBtn, playBtnRect)
    renderSurface.blit(optionsBtn, optionsBtnRect)
    
    # Draw hightlighter
    if selectedMain == 0:
        renderSurface.blit(optionHighligher, (0, currentH - 450))
    if selectedMain == 1:
        renderSurface.blit(optionHighligher, (0, currentH - 280))

# Draw availiable songs on the screen
def drawSongs():
    rectangle = Surface((800, 770), SRCALPHA)
    rectangle.fill((0, 0, 0, 128))
    rect_x = 165
    rect_y = 65
    renderSurface.blit(rectangle, (rect_x, rect_y))
    
    for i in range(len(songList)):
        if i == selectedSong:
            songName = FNFFont70.render(songList[i], 1, (255, 255, 255))
        else:
            songName = FNFFont70.render(songList[i], 1, (200, 200, 200))

        songNameRect = songName.get_rect()
        songNameRect.center = (middleScreen[0] - 235, middleScreen[1] 
                               + 110 * (i - selectedSong))
        renderSurface.blit(songName, songNameRect)
    
    renderSurface.blit(optionHighligher, (0, middleScreen[1] - 100))

# Draw options menu
def drawOptions():
    rectangle = Surface((800, 770), SRCALPHA)
    rectangle.fill((0, 0, 0, 128))
    rect_x = 165
    rect_y = 65
    renderSurface.blit(rectangle, (rect_x, rect_y))
    
    optionsText = [f"Speed: {options.selectedSpeed}", f"Play as: {options.playAs}",
                   f"No dying: {options.noDying}", f"Note style: {noteStyles[options.selectedNoteStyle]}",
                   f"Downscroll: {options.downscroll}", f"Debug mode: {options.debugMode}",
                   "Health: {0}".format("Healthbar" if options.healthFormat == "Healthbar" else "Infobar"),
                   f"Colored info bar: {options.coloredInfo}", "Keybinds"]
    
    for i in range(len(optionsText)):
        if i == selectedOption:
            text = FNFFont70.render(optionsText[i], 1, (255, 255, 255))
        else:
            text = FNFFont70.render(optionsText[i], 1, (200, 200, 200))
        
        # Change current option position
        text1 = text.get_rect()
        text1.center = (middleScreen[0] - 235, middleScreen[1] 
                        + 110 * (i - selectedOption))
        renderSurface.blit(text, text1)
    
    renderSurface.blit(optionHighligher, (0, middleScreen[1] - 100))

# Draw keybinds set menu
def drawKeybinds():
    rectangle = Surface((800, 770), SRCALPHA)
    rectangle.fill((0, 0, 0, 128))
    rect_x = 165
    rect_y = 65
    renderSurface.blit(rectangle, (rect_x, rect_y))
    
    keyList = [key.name(K_a), key.name(K_s), key.name(K_w), key.name(K_d), 
                key.name(K_LEFT), key.name(K_DOWN), key.name(K_UP), key.name(K_RIGHT), "None"]
    
    for i in range(len(keyList)):
        keyList[i] = keyList[i].title()
    
    tempText = ["Left: {0}", "Down: {0}", "Up: {0}", "Right: {0}", "Left 2: {0}", 
                "Down 2: {0}", "Up 2: {0}", "Right 2: {0}", "Reset keybinds"]
    
    for i in range(len(tempText)):
        tempText[i] = tempText[i].format(keyList[i])
        
        if i == selectedKeybind:
            temp = FNFFont70.render(tempText[i], 1, (255, 255, 255))
        else:
            temp = FNFFont70.render(tempText[i], 1, (200, 200, 200))
        
        # Change current option position (no animation, snap movement)
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0] - 235, middleScreen[1] 
                        + 110 * (i - selectedKeybind))
        renderSurface.blit(temp, temp1)
    
    renderSurface.blit(optionHighligher, (0, middleScreen[1] - 100))

# Draw keybind edit prompt
def drawEditKeybinds():
    rectangle = Surface((1600, 190), SRCALPHA)
    rectangle.fill((0, 0, 0, 128))
    rect_x = 0
    rect_y = 360
    renderSurface.blit(rectangle, (rect_x, rect_y))
    
    text = SysFont70.render("Press a key to edit keybind", 1, (255, 255, 255))
    text1 = text.get_rect()
    text1.midbottom = middleScreen
    renderSurface.blit(text, text1)
    text = SysFont70.render("(ESC to cancel)", 1, (255, 255, 255))
    text1 = text.get_rect()
    text1.midtop = middleScreen
    renderSurface.blit(text, text1)

# 3, 2, 1, GO!
def countdown():
    if not skipCountdown:
        colors = [(51, 52, 105), (61, 62, 115), (71, 72, 125), (0, 0, 0)]
        texts = ['3', '2', '1']
        images = ['data/ui/game/go.png']
        for i in range(3):
            text = FNFFont110.render(texts[i], True, (255, 255, 255))
            text_rect = text.get_rect(center=middleScreen)
            sprite = image.load(images[0])
            sprite_rect = sprite.get_rect(center=middleScreen)
            sfx = [threeSFX, twoSFX, oneSFX][i]
            renderSurface.fill(colors[i])
            renderSurface.blit(menuBG, rectBG)
            renderSurface.blit(text, text_rect)
            if antiAliasing:
                scaledSurface = transform.smoothscale(renderSurface, displayResolution)
            else:
                scaledSurface = transform.scale(renderSurface, displayResolution)
            scaledWindow.blit(scaledSurface, (0, 0))
            display.flip()
            sfx.play()
            Time.sleep(0.6)
            if i == 2:
                renderSurface.fill(colors[i])
                renderSurface.blit(sprite, sprite_rect)
                if antiAliasing:
                    scaledSurface = transform.smoothscale(renderSurface, displayResolution)
                else:
                    scaledSurface = transform.scale(renderSurface, displayResolution)
                scaledWindow.blit(scaledSurface, (0, 0))
                display.flip()
        goSFX.play()
        Time.sleep(0.6)

# Load shit
def loadAnimation(item, type):
    # Check type
    if type == 'character':
        tree = ET.parse(f'data/characters/{item}/character.xml')
        spriteSheet = image.load(f'data/characters/{item}/character.png').convert_alpha()
    else:
        tree = ET.parse(f'data/{type}/{item}/animation.xml')
        spriteSheet = image.load(f'data/{type}/{item}/animation.png').convert_alpha()
    
    # XML stuff
    root = tree.getroot()
    animations = {}
    offsetX = {}
    offsetY = {}
    
    # Grab texture coordinates
    for subtexture in root.iter('SubTexture'):
        name = subtexture.attrib['name']
        x = int(subtexture.attrib['x'])
        y = int(subtexture.attrib['y'])
        width = int(subtexture.attrib['width'])
        height = int(subtexture.attrib['height'])
        frameX = int(subtexture.attrib['frameX'])  # These guys
        frameY = int(subtexture.attrib['frameY'])  # Suck balls
        frameWidth = int(subtexture.attrib['frameWidth'])
        frameHeight = int(subtexture.attrib['frameHeight'])
        
        # Hmm rectangles
        frameRect = Rect(x, y, width, height)
        frameSurface = Surface((frameWidth, frameHeight), SRCALPHA)
        frameSurface.blit(spriteSheet, (0, 0), frameRect)
        
        # Separate frame name from id
        animationName = name.split('0')[0].rstrip()
        
        # Append
        if animationName not in animations:
            animations[animationName] = []
            offsetX[animationName] = []
            offsetY[animationName] = []
        animations[animationName].append(frameSurface)
        offsetX[animationName].append(frameX)
        offsetY[animationName].append(frameY)
    return animations, offsetX, offsetY

# Draw animations
def drawAnimation(item, position, scale, animation, duration, flipped, offsetX, offsetY, pixel=False):
    animFrames = item
    osX = offsetX
    osY = offsetY
    frameDuration = 1000 // duration
    if animation in animFrames:
        frames = animFrames[animation]
        ofsX = osX[animation]
        ofsY = osY[animation]
        numFrames = len(frames)
        frameIndex = int(frameTimer / frameDuration) % numFrames
        
        currentFrame = frames[frameIndex]
        currentOfsX = ofsX[frameIndex]
        currentOfsY = ofsY[frameIndex]
        frameWidth, frameHeight = currentFrame.get_size()
        
        if antiAliasing and not pixel:
            scaledFrame = transform.smoothscale(currentFrame, (int(frameWidth * scale),
                                                            int(frameHeight * scale)))
        else:
            scaledFrame = transform.scale(currentFrame, (int(frameWidth * scale),
                                                            int(frameHeight * scale)))
        
        if flipped:
            scaledFrame = transform.flip(scaledFrame, True, False)
        
        x, y = (position[0] - scaledFrame.get_width() // 2,
                position[1] - scaledFrame.get_width() // 2)
        
        if flipped: 
            renderSurface.blit(scaledFrame, (x + currentOfsX, y - currentOfsY))
        else:
            renderSurface.blit(scaledFrame, (x - currentOfsX, y - currentOfsY))

# Options screen class
class Options:
    def __init__(self):
        self.update()
    
    def update(self):
        global K_a, K_s, K_w, K_d
        global K_LEFT, K_DOWN, K_UP, K_RIGHT
        
        self.noteStyles = noteStyles
        self.arguments = json.load(open('data/parameters/options.json'))
        self.selectedSpeed = self.arguments['selectedSpeed']
        self.playAs = self.arguments['playAs']
        
        if self.arguments['selectedNoteStyle'] < len(noteStyles):
            self.selectedNoteStyle = self.arguments['selectedNoteStyle']
        else:
            self.selectedNoteStyle = 0
        
        self.noDying = self.arguments['noDying'] == 'True'
        self.downscroll = self.arguments['downscroll'] == 'True'
        self.debugMode = self.arguments['debug_mode'] == 'True'
        
        K_a = self.arguments["keybinds"][0]
        K_s = self.arguments["keybinds"][1]
        K_w = self.arguments["keybinds"][2]
        K_d = self.arguments["keybinds"][3]
        
        K_LEFT = self.arguments["keybinds"][4]
        K_DOWN = self.arguments["keybinds"][5]
        K_UP = self.arguments["keybinds"][6]
        K_RIGHT = self.arguments["keybinds"][7]
        
        self.keybinds = [K_a, K_s, K_w, K_d, K_LEFT, K_DOWN, K_UP, K_RIGHT]
        self.healthFormat = self.arguments["health_format"]
        self.coloredInfo = self.arguments["colored_info"] == "True"
    
    def saveOptions(self):
        global K_a, K_s, K_w, K_d
        global K_LEFT, K_DOWN, K_UP, K_RIGHT
        
        self.arguments["selectedSpeed"] = self.selectedSpeed
        self.arguments["playAs"] = self.playAs
        self.arguments["noDying"] = str(self.noDying)
        self.arguments["debug_mode"] = str(self.debugMode)
        self.arguments["downscroll"] = str(self.downscroll)
        self.arguments["selectedNoteStyle"] = self.selectedNoteStyle
        self.arguments["keybinds"] = [K_a, K_s, K_w, K_d, K_LEFT, K_DOWN, K_UP, K_RIGHT]
        self.arguments["health_format"] = self.healthFormat
        self.arguments["colored_info"] = str(self.coloredInfo)
        
        json.dump(self.arguments, open('data/parameters/options.json', 'w'))

# Note classes
class Note:
    def __init__(self, pos, column, side, length, noteId, textureName, behaviour=None):
        self.pos = pos
        self.column = column
        self.side = side
        self.length = length
        self.id = noteId
        self.texture = textureName
        self.behaviour = behaviour
        self.columnid = -1
        self.columnid2 = -1
        self.columnid3 = -1
        self.bigHealthBoost = 2.3
        self.smallHealthBoost = 0.4
        self.healthPenalty = -4
        self.mustAvoid = False
        self.hitModchart = []
        self.missModchart = []

class LongNote:
    def __init__(self, pos, column, side, isEnd, textureName):
        self.pos = pos
        self.column = column
        self.side = side
        self.isEnd = isEnd
        self.texture = textureName

class LongNoteGroup:
    def __init__(self, groupId):
        self.id = groupId
        self.notes = []
        self.size = 0
        self.canDealDamage = True

    def setSize(self):
        self.notes.remove(self.notes[0])
        self.size = len(self.notes)

# Define options
options = Options()

# Main game
def mainGame(songName, options):
    # Call in
    global Inst
    global Vocals
    global chart
    global misses
    global health
    global BG
    global opponentAnimation
    global playerAnimation
    global hasPlayedMicDrop
    global combo
    global bpm
    global arrow1Alpha
    global arrow2Aplha
    global character1
    global character2
    global character1Alpha
    global character2Alpha
    global currentTime
    global frameTimer
    global singlePlayer
    global sceneLoaded
    global potatoMode
    
    # Scene not loaded by default
    sceneLoaded = False
    
    # Frametimer
    frameTimer = 0
    
    # Arrow alphas
    arrow1Alpha = 1
    arrow2Alpha = 1
    
    # Game logic
    misses = 0
    health = 50
    combo = 0
    fpsQuality = 60
    fpsList = []
    fpsTime = Time.time()
    accuracy = 0
    accuracyDisplayTime = 0
    showAccuracy = False
    accuracyIndicator = ''
    accuracyPercentList = []
    longNotesChart = []
    opponentHitTimes = [-10 for _ in range(4)]
    opponentAnimation = ["Up", -10]
    playerAnimation = ["Up", -10]
    modifications = []
    dynamicModifications = []
    transitionValuesList = []
    hasPlayedMicDrop = False
    loadedCharacters = {}
    singlePlayer = False
    sys.setrecursionlimit(1000000)
    
    # Not pixel by default
    pixelSong = False
    
    # Default keybinds
    K_a = options.keybinds[0]
    K_s = options.keybinds[1]
    K_w = options.keybinds[2]
    K_d = options.keybinds[3]
    K_LEFT = options.keybinds[4]
    K_DOWN = options.keybinds[5]
    K_UP = options.keybinds[6]
    K_RIGHT = options.keybinds[7]
    
    # Update window title
    display.set_caption(f'YellowFox Engine | Now playing: {songName}')
    
    # Grab song data
    with open(f'data/songs/{songName}/data.json') as i:
        songData = json.load(i)
        
    # Grab song data
    def open_file(song):
        global Inst
        global Vocals
        global chart
        global bpm
        
        # Get song path
        songPath = f'data/songs/{song}/'
        
        # Load audio
        Inst = mixer.Sound(
            songPath + "\Inst.ogg")
        Vocals = mixer.Sound(
            songPath + "\Voices.ogg")
        
        # Load chart
        try:
            chart = json.load(open(songPath + '/chart.json'))['song']['notes']
        except:
            print("Chart is in incorrect format, formatting it.")
            chart = {"song": json.load(open(songPath + '/chart.json', 'w'))}
            json.dump(chart, open(songPath + '/chart.json', 'w'))
            chart = chart['song']['notes']
        try:
            bpm = json.load(open(songPath + '/chart.json'))['song']['bpm']
            bpm = 60000 / bpm
        except error as e:
            print("No BPM detected, using 100 bpm")
            if options.debugMode:
                print("Debug mode stopped the program. Error:")
                print(e)
            bpm = 60000 / 100
    
    # Play song
    def play(song=False):
        if not song:
            open_file(songList[randint(0, len(songList) - 1)])
        else:
            open_file(song)
    play(songName)
    
    # Lenght
    temp1 = Inst.get_length()
    temp2 = Vocals.get_length()
    if temp1 > temp2:
        songLen = temp1
    else:
        songLen = temp2
    
    # Check if song uses mods
    try:
        modifications = songData['modifications']
    except:
        modifications = []
    try:
        dynamicModifications = json.load(open(f'data/songs/{songName}/modchart.json'))['modchart']
    except:
        dynamicModifications = []
    
    # Show loading
    loadingScreen()
    
    # Grab acc indicator textures
    if antiAliasing:
        accuracyIndicatorImages = [
            transform.smoothscale(image.load("data/ui/accuracy/sick.png").convert_alpha(), (225, 100)),
            transform.smoothscale(image.load("data/ui/accuracy/good.png").convert_alpha(), (225, 100)),
            transform.smoothscale(image.load("data/ui/accuracy/bad.png").convert_alpha(), (225, 100)),
            transform.smoothscale(image.load("data/ui/accuracy/shit.png").convert_alpha(), (225, 100))
        ]
    else:
        accuracyIndicatorImages = [
            transform.scale(image.load("data/ui/accuracy/sick.png").convert_alpha(), (225, 100)),
            transform.scale(image.load("data/ui/accuracy/good.png").convert_alpha(), (225, 100)),
            transform.scale(image.load("data/ui/accuracy/bad.png").convert_alpha(), (225, 100)),
            transform.scale(image.load("data/ui/accuracy/shit.png").convert_alpha(), (225, 100))
        ]
    
    # Check if charts use mustHitSection
    notesChart = []
    for section in chart:
        if not section['mustHitSection']:
            useMustHitSection = True
    
    if options.playAs == "Player":
        tempPlayAs = ["Player", "Opponent"]
    else:
        tempPlayAs = ["Opponent", "Player"]
    
    tempNoteId = 0
    for section in chart:
        if not useMustHitSection:
            tempMustHit = True
        else:
            tempMustHit = section["mustHitSection"]
        for note in section["sectionNotes"]:
            tempUser = ""
            tempDirection = ""
            if isinstance(note[2], int) or isinstance(note[2], float):
                if not useMustHitSection:
                    if 3 >= note[1] >= 0:
                        tempUser = tempPlayAs[0]
                    elif 7 >= note[1] >= 4:
                        tempUser = tempPlayAs[1]
                    if note[1] == 0 or note[1] == 5:
                        tempDirection = "Left"
                    if note[1] == 1 or note[1] == 4:
                        tempDirection = "Down"
                    if note[1] == 2 or note[1] == 6:
                        tempDirection = "Up"
                    if note[1] == 3 or note[1] == 7:
                        tempDirection = "Right"
                if useMustHitSection:
                    if tempMustHit:
                        if 3 >= note[1] >= 0:
                            tempUser = tempPlayAs[0]
                        if 7 >= note[1] >= 4:
                            tempUser = tempPlayAs[1]
                        if note[1] == 0 or note[1] == 4:
                            tempDirection = "Left"
                        if note[1] == 1 or note[1] == 5:
                            tempDirection = "Down"
                        if note[1] == 2 or note[1] == 6:
                            tempDirection = "Up"
                        if note[1] == 3 or note[1] == 7:
                            tempDirection = "Right"
                    if not tempMustHit:
                        if 3 >= note[1] >= 0:
                            tempUser = tempPlayAs[1]
                        if 7 >= note[1] >= 4:
                            tempUser = tempPlayAs[0]
                        if note[1] == 1 or note[1] == 5:
                            tempDirection = "Down"
                        if note[1] == 0 or note[1] == 4:
                            tempDirection = "Left"
                        if note[1] == 2 or note[1] == 6:
                            tempDirection = "Up"
                        if note[1] == 3 or note[1] == 7:
                            tempDirection = "Right"
                tempTextureName = tempUser
                tempNote = Note(note[0], tempDirection, tempUser, note[2], tempNoteId, tempTextureName)
                tempNote.columnid = note[1]
                if len(note) > 2:
                    if note[2] is None:
                        tempNote.columnid2 = -1
                    else:
                        tempNote.columnid2 = note[2]
                if len(note) > 3:
                    if note[3] is None:
                        tempNote.columnid3 = -1
                    else:
                        tempNote.columnid3 = note[3]
                notesChart.append(tempNote)
                tempNoteId += 1

    notesChart.sort(key=lambda s: s.pos)

    temp = 0
    for k in range(len(notesChart)):
        if notesChart[k] is None:
            temp += 1

    for k in range(temp):
        notesChart.remove(None)

    longNotesLen = 41 // options.selectedSpeed
    for note in notesChart:
        if note.length >= longNotesLen > 0 and int(round(note.length // longNotesLen)):
            tempGroup = LongNoteGroup(note.id)
            for k in range(1, int(round(note.length // longNotesLen))):
                tempGroup.notes.append(LongNote(note.pos + k * longNotesLen, note.column, note.side, False, note.side))
            tempGroup.notes.append(
                LongNote(note.pos + (note.length // longNotesLen) * longNotesLen, note.column, note.side, True,
                         note.side))
            tempGroup.setSize()
            longNotesChart.append(tempGroup)

    longNotesChart.sort(key=lambda s: s.id)
    for element in longNotesChart:
        element.notes.sort(key=lambda s: s.pos)  
    
    # Get attribute rectangle
    def getAttributeRect(data):
        return Rect(float(data.attrib['x']), float(data.attrib['y']), float(data.attrib['width']),
                    float(data.attrib['height']))

    # Get number of first chars
    def getNfirstCharacters(text, n):
        result = ""
        if n < len(text):
            for i in range(n):
                result = f"{result}{text[i]}"
            return result
        else:
            return text

    # Get number of last chars
    def getNlastCharacters(text, n):
        result = ""
        for i in range(n):
            result = f"{result}{text[-i - 1]}"
        return result

    # Get animation XML data
    def getXmlData(name, type):
        if type == 'character':
            XMLpath = f'data/characters/{name}/character.xml'
            characterImage = image.load(f'data/characters/{name}/character.png')
            XMLfile = ET.parse(XMLpath).getroot()
            result = [[] for _ in range(5)]
            for data in XMLfile:
                name = data.attrib['name']
                tempResult = ""
                for i in range(len(name)):
                    if name[i] == '_':
                        tempResult = f"{tempResult}{' NOTE '}"
                    else:
                        tempResult = f"{tempResult}{name[i].upper()}"
                data.attrib['name'] = tempResult
            
            for data in XMLfile:
                name = data.attrib['name']
                tempResult = ""
                temp = False
                for i in range(len(name)):
                    if temp:
                        tempResult = f"{tempResult}{name[i]}"
                    if name[i] == " ":
                        temp = True
                if tempResult != "":
                    data.attrib['name'] = tempResult
            
            for data in XMLfile:
                name = data.attrib['name']
                if getNfirstCharacters(name, 9) == 'NOTE IDLE' or getNfirstCharacters(name, 4) == 'IDLE':
                    name = f"idle dance{getNlastCharacters(name, 4)}"
                data.attrib['name'] = name
            
            for data in XMLfile:
                name = data.attrib['name']
                if getNfirstCharacters(name, 10) == 'IDLE DANCE':
                    data.attrib['name'] = name.lower()
            
            for data in XMLfile:
                name = data.attrib['name']
                if getNfirstCharacters(name, 2) == 'UP':
                    name = f'NOTE UP{getNlastCharacters(name, 4)}'
                if getNfirstCharacters(name, 4) == "DOWN":
                    name = f"NOTE DOWN{getNlastCharacters(name, 4)}"
                if getNfirstCharacters(name, 4) == "LEFT":
                    name = f"NOTE LEFT{getNlastCharacters(name, 4)}"
                if getNfirstCharacters(name, 5) == "RIGHT":
                    name = f"NOTE RIGHT{getNlastCharacters(name, 4)}"
                data.attrib["name"] = name
            
            for data in XMLfile:
                if getNfirstCharacters(data.attrib["name"], 9) == "NOTE LEFT" and len(data.attrib["name"]) == 13:
                    result[0].append(characterImage.subsurface(getAttributeRect(data)))
                if getNfirstCharacters(data.attrib["name"], 9) == "NOTE DOWN" and len(data.attrib["name"]) == 13:
                    result[1].append(characterImage.subsurface(getAttributeRect(data)))
                if getNfirstCharacters(data.attrib["name"], 7) == "NOTE UP" and len(data.attrib["name"]) == 11:
                    result[2].append(characterImage.subsurface(getAttributeRect(data)))
                if getNfirstCharacters(data.attrib["name"], 10) == "NOTE RIGHT" and len(data.attrib["name"]) == 14:
                    result[3].append(characterImage.subsurface(getAttributeRect(data)))
                if getNfirstCharacters(data.attrib["name"], 10) == "idle dance" and len(data.attrib["name"]) == 14:
                    result[4].append(characterImage.subsurface(getAttributeRect(data)))
            return result
    
    # Load arrow sprites
    def loadArrows(skinName):
        base_path = "data" + os.path.sep + "ui" + os.path.sep + "arrows" + os.path.sep + "{0}".format(skinName)
        json_path = os.path.join(base_path, "arrowData.json")
        XMLPath = os.path.join(base_path, "arrowSkin.xml")
        imagePath = os.path.join(base_path, "arrowSkin.png")
        
        skinData = json.load(open(json_path))
        XMLFile = ET.parse(XMLPath).getroot()
        skinImage = image.load(imagePath).convert_alpha()
        
        result = {
            "arrowsSkin": [None for _ in range(4)],
            "pressedArrowsSkins": [None for _ in range(4)],
            "greyArrow": [None for _ in range(4)],
            "longNotesImg": [None for _ in range(4)],
            "longNotesEnd": [None for _ in range(4)]
        }
        
        tempArrows = ["purple alone0000", "blue alone0000", "green alone0000", "red alone0000"]
        tempPressed = ["left press0000", "down press0000", "up press0000", "right press0000"]
        tempGrey = ["arrowLEFT0000", "arrowDOWN0000", "arrowUP0000", "arrowRIGHT0000"]
        tempLong = ["purple hold0000", "blue hold0000", "green hold0000", "red hold0000"]
        tempLongEnd = ["purple tail0000", "blue tail0000", "green tail0000", "red tail0000"]
        
        attribute_rect_cache = {data.attrib["name"]: getAttributeRect(data) for data in XMLFile}
        
        for data in XMLFile:
            name = data.attrib["name"]
            if name in tempArrows:
                try:
                    temp = skinData["Size"]["arrowsSkin"][tempArrows.index(name)]
                except KeyError:
                    temp = 1
                tempImage = skinImage.subsurface(attribute_rect_cache[name]).convert_alpha()
                if antiAliasing:
                    tempImage = transform.smoothscale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                else:
                    tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["arrowsSkin"][tempArrows.index(name)] = tempImage
            elif name in tempPressed:
                try:
                    temp = skinData["Size"]["pressedArrowsSkin"][tempPressed.index(name)]
                except KeyError:
                    temp = 1
                tempImage = skinImage.subsurface(attribute_rect_cache[name]).convert_alpha()
                if antiAliasing:
                    tempImage = transform.smoothscale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                else:
                    tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["pressedArrowsSkins"][tempPressed.index(name)] = tempImage
            elif name in tempGrey:
                try:
                    temp = skinData["Size"]["greyArrow"][tempGrey.index(name)]
                except KeyError:
                    temp = 1
                tempImage = skinImage.subsurface(attribute_rect_cache[name]).convert_alpha()
                if antiAliasing:
                    tempImage = transform.smoothscale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                else:
                    tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["greyArrow"][tempGrey.index(name)] = tempImage
            elif name in tempLong:
                try:
                    temp = skinData["Size"]["greyArrow"][tempLong.index(name)]
                except KeyError:
                    temp = 1
                tempImage = skinImage.subsurface(attribute_rect_cache[name]).convert_alpha()
                if antiAliasing:
                    tempImage = transform.smoothscale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                else:
                    tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["longNotesImg"][tempLong.index(name)] = tempImage
            elif name in tempLongEnd:
                try:
                    temp = skinData["Size"]["greyArrow"][tempLongEnd.index(name)]
                except KeyError:
                    temp = 1
                tempImage = skinImage.subsurface(attribute_rect_cache[name]).convert_alpha()
                if antiAliasing:
                    tempImage = transform.smoothscale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                else:
                    tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["longNotesEnd"][tempLongEnd.index(name)] = tempImage
        
        return result

    # Draw grey notes
    def drawGreyNotes():
        width = currentW
        height = currentH
        currentTime = Time.time() - startTime
        if "hideNotes2" not in modifications:
            if K_a in keyPressed or K_LEFT in keyPressed:
                temp = loadedArrowTextures["Player"].pressedArrowsSkins[0].get_rect()
            else:
                temp = loadedArrowTextures["Player"].greyArrow[0].get_rect()
            if not options.downscroll:
                temp.center = (width - 615, 125)
            else:
                temp.center = (width - 615, height - 125)
            if K_a in keyPressed or K_LEFT in keyPressed:
                temp1 = copy.copy(loadedArrowTextures["Player"].pressedArrowsSkins[0])
                temp1.set_alpha(arrow2Alpha * 255)
                renderSurface.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Player"].greyArrow[0]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                renderSurface.blit(temp1, temp)
            if K_s in keyPressed or K_DOWN in keyPressed:
                temp = loadedArrowTextures["Player"].pressedArrowsSkins[1].get_rect()
            else:
                temp = loadedArrowTextures["Player"].greyArrow[1].get_rect()
            if not options.downscroll:
                temp.center = (width - 455, 125)
            else:
                temp.center = (width - 455, height - 125)
            if K_s in keyPressed or K_DOWN in keyPressed:
                temp1 = copy.copy(loadedArrowTextures["Player"].pressedArrowsSkins[1]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                renderSurface.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Player"].greyArrow[1]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                renderSurface.blit(temp1, temp)
            if K_w in keyPressed or K_UP in keyPressed:
                temp = loadedArrowTextures["Player"].pressedArrowsSkins[2].get_rect()
            else:
                temp = loadedArrowTextures["Player"].greyArrow[2].get_rect()
            if not options.downscroll:
                temp.center = (width - 295, 125)
            else:
                temp.center = (width - 295, height - 125)
            if K_w in keyPressed or K_UP in keyPressed:
                temp1 = copy.copy(loadedArrowTextures["Player"].pressedArrowsSkins[2]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                renderSurface.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Player"].greyArrow[2]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                renderSurface.blit(temp1, temp)
            if K_d in keyPressed or K_RIGHT in keyPressed:
                temp = loadedArrowTextures["Player"].pressedArrowsSkins[3].get_rect()
            else:
                temp = loadedArrowTextures["Player"].greyArrow[3].get_rect()
            if not options.downscroll:
                temp.center = (width - 135, 125)
            else:
                temp.center = (width - 135, height - 125)
            if K_d in keyPressed or K_RIGHT in keyPressed:
                temp1 = copy.copy(loadedArrowTextures["Player"].pressedArrowsSkins[3]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                renderSurface.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Player"].greyArrow[3]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                renderSurface.blit(temp1, temp)
        if not singlePlayer and "hideNotes1" not in modifications:
            if currentTime - opponentHitTimes[0] > 0.15:
                temp = loadedArrowTextures["Opponent"].greyArrow[0].get_rect()
            else:
                temp = loadedArrowTextures["Opponent"].pressedArrowsSkins[0].get_rect()
            if not options.downscroll:
                temp.center = (135, 125)
            else:
                temp.center = (135, height - 125)
            if currentTime - opponentHitTimes[0] > 0.15:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].greyArrow[0]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                renderSurface.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].pressedArrowsSkins[0]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                renderSurface.blit(temp1, temp)
            if currentTime - opponentHitTimes[1] > 0.15:
                temp = loadedArrowTextures["Opponent"].greyArrow[1].get_rect()
            else:
                temp = loadedArrowTextures["Opponent"].pressedArrowsSkins[1].get_rect()
            if not options.downscroll:
                temp.center = (295, 125)
            else:
                temp.center = (295, height - 125)
            if currentTime - opponentHitTimes[1] > 0.15:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].greyArrow[1]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                renderSurface.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].pressedArrowsSkins[1]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                renderSurface.blit(temp1, temp)
            if currentTime - opponentHitTimes[2] > 0.15:
                temp = loadedArrowTextures["Opponent"].greyArrow[2].get_rect()
            else:
                temp = loadedArrowTextures["Opponent"].pressedArrowsSkins[2].get_rect()
            if not options.downscroll:
                temp.center = (455, 125)
            else:
                temp.center = (455, height - 125)
            if currentTime - opponentHitTimes[2] > 0.15:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].greyArrow[2]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                renderSurface.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].pressedArrowsSkins[2]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                renderSurface.blit(temp1, temp)
            if currentTime - opponentHitTimes[3] > 0.15:
                temp = loadedArrowTextures["Opponent"].greyArrow[3].get_rect()
            else:
                temp = loadedArrowTextures["Opponent"].pressedArrowsSkins[3].get_rect()
            if not options.downscroll:
                temp.center = (615, 125)
            else:
                temp.center = (615, height - 125)
            if currentTime - opponentHitTimes[3] > 0.15:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].greyArrow[3]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                renderSurface.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].pressedArrowsSkins[3]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                renderSurface.blit(temp1, temp)

    # Draw standard notes
    def drawNotes():
        global misses
        global health
        global opponentAnimation
        global combo
        
        currentTime = Time.time() - startTime
        width = currentW
        height = currentH
        renderNotes = True
        for note in notesChart:
            if renderNotes:
                if note.side == "Opponent" and currentTime * 1000 >= note.pos:
                    opponentAnimation = [note.column, currentTime]
                    opponentHitTimes[["Left", "Down", "Up", "Right"].index(note.column)] = currentTime
                    notesChart.remove(note)
                if currentTime * 1000 - 133 >= note.pos and note.side == "Player" and note.column in ["Left", "Down",
                                                                                                      "Up",
                                                                                                      "Right"]:
                    for noteGroup in longNotesChart:
                        if noteGroup.id == note.id:
                            noteGroup.canDealDamage = False
                            break
                    notesChart.remove(note)
                    if not note.mustAvoid:
                        misses += 1
                        update_modifications(note.missModchart, note.missModchart)
                    health += note.healthPenalty
                    if health < 0:
                        health = 0
                    if not note.mustAvoid:
                        accuracyPercentList.append(0)
                        combo = 0
                if 50 + (note.pos - currentTime * 1000) * options.selectedSpeed < currentH + 100:
                    if not singlePlayer and "hideNotes1" not in modifications:
                        if note.side == "Opponent" and note.column == "Down":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[1].get_rect()
                            if not options.downscroll:
                                temp.center = (295, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    295, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[1]).convert_alpha()
                            temp1.set_alpha(arrow1Alpha * 255)
                            renderSurface.blit(temp1, temp)
                        elif note.side == "Opponent" and note.column == "Left":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[0].get_rect()
                            if not options.downscroll:
                                temp.center = (135, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    135, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[0]).convert_alpha()
                            temp1.set_alpha(arrow1Alpha * 255)
                            renderSurface.blit(temp1, temp)
                        elif note.side == "Opponent" and note.column == "Up":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[2].get_rect()
                            if not options.downscroll:
                                temp.center = (455, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    455, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[2]).convert_alpha()
                            temp1.set_alpha(arrow1Alpha * 255)
                            renderSurface.blit(temp1, temp)
                        elif note.side == "Opponent" and note.column == "Right":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[3].get_rect()
                            if not options.downscroll:
                                temp.center = (615, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    615, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[3]).convert_alpha()
                            temp1.set_alpha(arrow1Alpha * 255)
                            renderSurface.blit(temp1, temp)
                    if "hideNotes2" not in modifications:
                        if note.side == "Player" and note.column == "Down":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[1].get_rect()
                            if not options.downscroll:
                                temp.center = (
                                    width - 455, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    width - 455, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[1]).convert_alpha()
                            temp1.set_alpha(arrow2Alpha * 255)
                            renderSurface.blit(temp1, temp)
                        elif note.side == "Player" and note.column == "Left":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[0].get_rect()
                            if not options.downscroll:
                                temp.center = (
                                    width - 615, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    width - 615, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[0]).convert_alpha()
                            temp1.set_alpha(arrow2Alpha * 255)
                            renderSurface.blit(temp1, temp)
                        elif note.side == "Player" and note.column == "Up":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[2].get_rect()
                            if not options.downscroll:
                                temp.center = (
                                    width - 295, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    width - 295, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[2]).convert_alpha()
                            temp1.set_alpha(arrow2Alpha * 255)
                            renderSurface.blit(temp1, temp)
                        elif note.side == "Player" and note.column == "Right":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[3].get_rect()
                            if not options.downscroll:
                                temp.center = (
                                    width - 135, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    width - 135, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[3]).convert_alpha()
                            temp1.set_alpha(arrow2Alpha * 255)
                            renderSurface.blit(temp1, temp)

                else:
                    renderNotes = False

    # Draw long notes (snakes)
    def drawLongNotes():
        global opponentAnimation
        global playerAnimation
        global misses
        global health
        global combo
        
        currentTime = Time.time() - startTime
        width = currentW
        height = currentH
        deleteList = []
        for noteGroup in longNotesChart:
            deleteGroup = False
            run = True
            if len(noteGroup.notes) == 0:
                run = False
                deleteGroup = True
            if run and 50 + (noteGroup.notes[0].pos - currentTime * 1000) * options.selectedSpeed < height + 100:
                for longNote in noteGroup.notes:
                    if currentTime * 1000 - 133 >= longNote.pos:
                        if longNote.side == "Player":
                            if (noteGroup.size - len(noteGroup.notes)) / noteGroup.size >= 0.75:
                                noteGroup.canDealDamage = False
                            if noteGroup.canDealDamage:
                                misses += 1
                                health -= 4
                                if health < 0:
                                    health = 0
                                accuracyPercentList.append(0)
                                combo = 0
                                noteGroup.canDealDamage = False
                            noteGroup.notes.remove(longNote)
                    else:
                        if noteGroup.canDealDamage:
                            transparent = False
                        else:
                            transparent = True
                        if longNote.side == "Opponent" and currentTime * 1000 >= longNote.pos:
                            if currentTime - opponentAnimation[1] > 0.7:
                                opponentAnimation = [longNote.column, currentTime]
                            opponentHitTimes[["Left", "Down", "Up", "Right"].index(longNote.column)] = currentTime
                            noteGroup.notes.remove(longNote)
                        if longNote.side == "Player" and currentTime * 1000 >= longNote.pos and longNote.column in [
                                                    "Left",
                                                    "Down",
                                                    "Up",
                                                    "Right"] and (((K_LEFT in keyPressed or K_a in keyPressed) and longNote.column == "Left") or (
                                                            (K_DOWN in keyPressed or K_s in keyPressed) and longNote.column == "Down") or (
                                                            (K_UP in keyPressed or K_w in keyPressed) and longNote.column == "Up") or (
                                                            (K_RIGHT in keyPressed or K_d in keyPressed) and longNote.column == "Right")):
                            if currentTime - playerAnimation[1] > 0.7:
                                playerAnimation = [longNote.column, currentTime]
                            noteGroup.notes.remove(longNote)
                        if 50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed < height + 100:
                            if not singlePlayer and longNote.side == "Opponent" and "hideNotes1" not in modifications:
                                if longNote.column == "Down":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            220 + 125,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            220 + 125,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        temp1 = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesEnd[1]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        renderSurface.blit(temp1, temp)
                                    else:
                                        temp1 = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesImg[1]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        renderSurface.blit(temp1, temp)
                                if longNote.column == "Left":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (60 + 125, 50 + (
                                                longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            60 + 125,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        temp1 = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesEnd[0]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        renderSurface.blit(temp1, temp)
                                    else:
                                        temp1 = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesImg[0]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        renderSurface.blit(temp1, temp)
                                if longNote.column == "Up":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            380 + 125,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            380 + 125,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        temp1 = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesEnd[2]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        renderSurface.blit(temp1, temp)
                                    else:
                                        temp1 = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesImg[2]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        renderSurface.blit(temp1, temp)
                                if longNote.column == "Right":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            540 + 125,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            540 + 125,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        temp1 = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesEnd[3]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        renderSurface.blit(temp1, temp)
                                    else:
                                        temp1 = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesImg[3]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        renderSurface.blit(temp1, temp)
                            if longNote.side == "Player" and "hideNotes2" not in modifications:
                                if longNote.column == "Up":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            width - 220 - 25,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            width - 220 - 25,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        img = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesEnd[2]).convert_alpha()
                                    else:
                                        img = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesImg[2]).convert_alpha()
                                    if arrow2Alpha:
                                        if transparent:
                                            img.set_alpha(100)
                                    else:
                                        img.set_alpha(arrow2Alpha * 255)
                                    renderSurface.blit(img, temp)
                                if longNote.column == "Down":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            width - 380 - 25,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            width - 380 - 25,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        img = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesEnd[1]).convert_alpha()
                                    else:
                                        img = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesImg[1]).convert_alpha()
                                    if arrow2Alpha == 1:
                                        if transparent:
                                            img.set_alpha(100)
                                    else:
                                        img.set_alpha(arrow2Alpha * 255)
                                    renderSurface.blit(img, temp)
                                if longNote.column == "Left":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            width - 540 - 25,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            width - 540 - 25,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        img = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesEnd[0]).convert_alpha()
                                    else:
                                        img = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesImg[0]).convert_alpha()
                                    if arrow2Alpha == 1:
                                        if transparent:
                                            img.set_alpha(100)
                                    else:
                                        img.set_alpha(arrow2Alpha * 255)
                                    renderSurface.blit(img, temp)
                                if longNote.column == "Right":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            width - 60 - 25,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            width - 60 - 25,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        img = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesEnd[3]).convert_alpha()
                                    else:
                                        img = copy.copy(
                                            loadedArrowTextures[longNote.texture].longNotesImg[3]).convert_alpha()
                                    if arrow2Alpha == 1:
                                        if transparent:
                                            img.set_alpha(100)
                                    else:
                                        img.set_alpha(arrow2Alpha * 255)
                                    renderSurface.blit(img, temp)
            if deleteGroup:
                deleteList.append(noteGroup.id)
        for element in longNotesChart:
            if element.id in deleteList:
                deleteList.remove(element.id)
                longNotesChart.remove(element)
            if len(deleteList) == 0:
                break

    # HUD - health bar
    def drawHealthBar():
        global health
        if health > 100:
            health = 100
        if health < 0:
            health = 0
        width = currentW
        height = currentH
        reduction_factor = 0.7

        if not options.downscroll:
            temp = SysFont15.render('Health^', 1, (217, 217, 217))
            temp1 = temp.get_rect()
            temp1.center = (middleScreen[0], currentH - 20)
            draw.rect(renderSurface, (20, 20, 20), Rect(250, currentH - 60, 1075, int(70 * reduction_factor)))
            draw.rect(renderSurface, (224, 224, 224), Rect(260, height - 50, int((width - 90) * reduction_factor), int(30 * reduction_factor)))
            renderSurface.blit(temp, temp1)
        else:
            temp = SysFont15.render('Health:', 1, (217, 217, 217))
            temp1 = temp.get_rect()
            temp1.center = (middleScreen[0], 30)
            draw.rect(renderSurface, (20, 20, 20), Rect(250, 20, 1075, int(70 * reduction_factor)))
            draw.rect(renderSurface, (224, 224, 224), Rect(260, 40, int((width - 90) * reduction_factor), int(30 * reduction_factor)))
            renderSurface.blit(temp, temp1)

        if health < 100:
            if not options.downscroll:
                draw.rect(renderSurface, (239, 83, 80), Rect(265, height - 45, int((width - 100) / 100 * (100 - health) * reduction_factor), int(20 * reduction_factor)))
            else:
                draw.rect(renderSurface, (239, 83, 80), Rect(265, 45, int((width - 100) / 100 * (100 - health) * reduction_factor), int(20 * reduction_factor)))

        if health > 0:
            if not options.downscroll:
                draw.rect(renderSurface, (124, 179, 66), Rect(265 + int((width - 100) / 100 * (100 - health) * reduction_factor), height - 45, int((width - 100) / 100 * health * reduction_factor), int(20 * reduction_factor)))
            else:
                draw.rect(renderSurface, (124, 179, 66), Rect(265 + int((width - 100) / 100 * (100 - health) * reduction_factor), 45, int((width - 100) / 100 * health * reduction_factor), int(20 * reduction_factor)))

    # HUD - progress bar
    def drawProgressBar():
        currentTime = Time.time() - startTime
        width = currentW
        height = currentH
        if not options.downscroll:
            draw.rect(renderSurface, (224, 224, 224), Rect(400, 5, width - 800, 30))
            draw.rect(renderSurface, (20, 20, 20), Rect(402, 7, width - 804, 25))
        else:
            draw.rect(renderSurface, (224, 224, 224), Rect(400, height - 5 - 40, width - 800, 30))
            draw.rect(renderSurface, (20, 20, 20), Rect(402, height - 7 - 36, width - 804, 25))
        temp = int(round(songLen - (Time.time() - startTime), 0))
        if not options.downscroll:
            draw.rect(renderSurface, (170, 170, 170), Rect(405, 10, (width - 810) / songLen * currentTime, 20))
        else:
            draw.rect(renderSurface, (170, 170, 170), Rect(405, height - 10 - 30, (width - 810) / songLen * currentTime, 20))
        tempMinutes = temp // 60
        tempSeconds = temp - (60 * tempMinutes)
        if tempSeconds < 10:
            temp1 = "0"
        else:
            temp1 = ""
        temp = SysFont20.render(f"{songName} {tempMinutes}:{temp1}{tempSeconds}", 1, (255, 255, 255))
        temp1 = temp.get_rect()
        if not options.downscroll:
            temp1.midtop = (middleScreen[0], 5)
        else:
            temp1.midbottom = (middleScreen[0], height - 20)
        renderSurface.blit(temp, temp1)

    # Draw characters
    def drawCharacters():
        currentTime = Time.time() - startTime
        animationFrame1 = int((((Time.time() - startTime) * 1000 / 2) % bpm) / bpm * len(character1.texture[4]))
        animationFrame2 = int((((Time.time() - startTime) * 1000 / 2) % bpm) / bpm * len(character2.texture[4]))

        # Character 1 - Idle animation
        if currentTime - opponentAnimation[1] >= 0.75:
            temp = character1.texture[4][animationFrame1].get_rect()
            temp.midbottom = [character1.pos[4][animationFrame1][0], currentH - character1.pos[4][animationFrame1][1]]
            temp1 = character1.texture[4][animationFrame1]
            temp1.set_alpha(character1Alpha * 255)
            renderSurface.blit(temp1, temp)
        # Character 1 - Directional animation
        else:
            animationDirection1 = ["Left", "Down", "Up", "Right"].index(opponentAnimation[0])
            if currentTime - opponentAnimation[1] < 0.45:
                tempTime = 0.45 / len(character1.texture[animationDirection1])
                numFrame = int((currentTime - opponentAnimation[1]) // tempTime)
            else:
                numFrame = len(character1.texture[animationDirection1]) - 1
            temp = character1.texture[animationDirection1][numFrame].get_rect()
            temp.midbottom = [character1.pos[animationDirection1][numFrame][0], currentH - character1.pos[animationDirection1][numFrame][1]]
            temp1 = character1.texture[animationDirection1][numFrame]
            temp1.set_alpha(character1Alpha * 255)
            renderSurface.blit(temp1, temp)
        
        # Character 2 - Idle animation
        if currentTime - playerAnimation[1] >= 0.75:
            temp = character2.texture[4][animationFrame2].get_rect()
            temp.midbottom = [currentW - character2.pos[4][animationFrame2][0], currentH - character2.pos[4][animationFrame2][1]]
            temp1 = character2.texture[4][animationFrame2]
            temp1.set_alpha(character2Alpha * 255)
            renderSurface.blit(temp1, temp)
        # Character 2 - Directional animation
        else:
            animationDirection2 = ["Left", "Down", "Up", "Right"].index(playerAnimation[0])
            if currentTime - playerAnimation[1] < 0.45:
                tempTime = 0.45 / len(character2.texture[animationDirection2])
                numFrame = int((currentTime - playerAnimation[1]) // tempTime)
            else:
                numFrame = len(character2.texture[animationDirection2]) - 1
            if numFrame > 14:
                numFrame = 1
            temp = character2.texture[animationDirection2][numFrame].get_rect()
            temp.midbottom = [currentW - character2.pos[animationDirection2][numFrame][0], currentH - character2.pos[animationDirection2][numFrame][1]]
            temp1 = character2.texture[animationDirection2][numFrame]
            temp1.set_alpha(character2Alpha * 255)
            renderSurface.blit(temp1, temp)
    
    # Death screen
    def death():
        global hasPlayedMicDrop
        startDeathTime = Time.time()
        deathScreenMusicStart.play()
        while True:
            for events in event.get():
                if events.type == QUIT:
                    deathScreenMusic.stop()
                    deathScreenMusicEnd.stop()
                    quit()
                    exit()
                if events.type == KEYDOWN:
                    if events.key == K_ESCAPE or events.key == K_BACKSPACE:
                        deathScreenMusic.stop()
                        return False
                    if events.key == K_SPACE or events.key == K_RETURN:
                        deathScreenMusic.stop()
                        deathScreenMusicEnd.play()
                        Time.sleep(deathScreenMusicEnd.get_length() - 2.5)
                        deathScreenMusicEnd.stop()
                        return True
            renderSurface.fill((0, 0, 0))
            if Time.time() - startDeathTime > deathScreenMusicStart.get_length() - 1.5 and not hasPlayedMicDrop:
                deathScreenMusic.play(-1)
                hasPlayedMicDrop = True
            renderSurface.blit(BFdead, deathScreenRect)
            if antiAliasing:
                scaled_surface = transform.smoothscale(renderSurface, displayResolution)
            else:
                scaled_surface = transform.scale(renderSurface, displayResolution)
            scaledWindow.blit(scaled_surface, (0, 0))
            display.flip()

    # Arrow class
    class arrowTexture:
        def __init__(self, skinName):
            temp = loadArrows(skinName)
            self.arrowsSkins = temp['arrowsSkin']
            for i in range(4):
                if self.arrowsSkins[i] is None:
                    self.arrowsSkins[i] = Surface((0, 0))
            self.pressedArrowsSkins = temp["pressedArrowsSkins"]
            for i in range(4):
                if self.pressedArrowsSkins[i] is None:
                    self.pressedArrowsSkins[i] = Surface((0, 0))
            self.greyArrow = temp["greyArrow"]
            for i in range(4):
                if self.greyArrow[i] is None:
                    self.greyArrow[i] = Surface((0, 0))
            self.longNotesImg = temp["longNotesImg"]
            for i in range(4):
                if self.longNotesImg[i] is None:
                    self.longNotesImg[i] = Surface((0, 0))
            if options.downscroll:
                for i in range(len(self.longNotesImg)):
                    self.longNotesImg[i] = transform.flip(self.longNotesImg[i], False, True)
            self.longNotesEnd = temp["longNotesEnd"]
            for i in range(4):
                if self.longNotesEnd[i] is None:
                    self.longNotesEnd[i] = Surface((0, 0))
            if options.downscroll:
                for i in range(len(self.longNotesEnd)):
                    self.longNotesEnd[i] = transform.flip(self.longNotesEnd[i], False, True)

    # Update modifications
    def update_modifications(modifications, dynamic_modifications):
        global character1
        global character2
        currentTime = Time.time() - startTime
        currentTime *= 1000
        for mod in dynamic_modifications:
            if mod["type"] == "add/remove" and mod["pos"] >= currentTime:
                if mod["action"] == "add":
                    modifications.append(mod["name"])
                elif mod["action"] == "remove":
                    if mod["name"] in modifications:
                        modifications.remove(mod["name"])
                dynamic_modifications.remove(mod)
            if mod["type"] == "arrowAlphaChange":
                try:
                    print("________")
                    print("Real time:")
                    print(currentTime)
                    print("Mod time:")
                    print(modchartGetValue("currentTime"))
                    temp = modchartGetValue(mod["pos"])
                    print("temp time:")
                    print(temp)
                    print("________")
                except:
                    temp = 0
                if currentTime >= temp:
                    if mod["player"] == 1:
                        transitionValuesList.append(
                            transitionValue("arrow1Alpha", modchartGetValue(mod["startValue"]),
                                            modchartGetValue(mod["endValue"]), modchartGetValue(mod["startTime"]),
                                            modchartGetValue(mod["endTime"])))
                    if mod["player"] == 2:
                        transitionValuesList.append(
                            transitionValue("arrow2Alpha", modchartGetValue(mod["startValue"]),
                                            modchartGetValue(mod["endValue"]), modchartGetValue(mod["startTime"]),
                                            modchartGetValue(mod["endTime"])))
                    dynamic_modifications.remove(mod)
            if mod["type"] == "characterAlphaChange":
                try:
                    temp = modchartGetValue(mod["pos"])
                except:
                    temp = 0
                if currentTime >= temp:
                    if mod["player"] == 1:
                        transitionValuesList.append(
                            transitionValue("character1Alpha", modchartGetValue(mod["startValue"]),
                                            modchartGetValue(mod["endValue"]), modchartGetValue(mod["startTime"]),
                                            modchartGetValue(mod["endTime"])))
                    if mod["player"] == 2:
                        transitionValuesList.append(
                            transitionValue("character2Alpha", modchartGetValue(mod["startValue"]),
                                            modchartGetValue(mod["endValue"]), modchartGetValue(mod["startTime"]),
                                            modchartGetValue(mod["endTime"])))
                    dynamic_modifications.remove(mod)
            if mod["type"] == "changeCharacter":
                try:
                    temp = modchartGetValue(mod["pos"])
                except:
                    temp = 0
                if currentTime >= temp:
                    if mod["player"] == 1:
                        if options.playAs == 'Player':
                            character1 = loadedCharacters[mod["name"]]
                        elif options.playAs == 'Opponent':
                            character2 = loadedCharacters[mod['name']]
                    elif mod["player"] == 2:
                        if options.playAs == 'Player':
                            character2 = loadedCharacters[mod["name"]]
                        elif options.playAs == 'Opponent':
                            character1 = loadedCharacters[mod['name']]
                    dynamic_modifications.remove(mod)
            if mod["type"] == "changeArrowTexture":
                try:
                    temp = modchartGetValue(mod["pos"])
                except:
                    temp = 0
                if currentTime >= temp:
                    if mod["player"] == 1:
                        loadedArrowTextures["Opponent"] = loadedArrowTextures[mod["name"]]
                    elif mod["player"] == 2:
                        loadedArrowTextures["Player"] = loadedArrowTextures[mod["name"]]
                    dynamic_modifications.remove(mod)
            if mod["type"] == "Organiser":
                update_modifications(modifications, mod["modchart"])
    
    # Update trans value
    def update_transitionValue():
        for element in transitionValuesList:
            element.update()
            if not element.isActive:
                transitionValuesList.remove(element)
    
    # Mod chart loading
    def modchartLoading():
        for mod in dynamicModifications:
            if mod["type"] == "characterLoading":
                try:
                    alias = mod["alias"]
                except:
                    alias = None
                if alias is None:
                    loadedCharacters[mod["name"]] = Character(mod["name"], mod["player"], True)
                else:
                    loadedCharacters[mod["alias"]] = Character(mod["name"], mod["player"], True)
            if mod["type"] == "arrowTextureLoading":
                loadedArrowTextures[mod["loadedName"]] = arrowTexture(mod["textureName"])
    
    # Mod chart get string args
    def modchartGetStringArguments(string):
        temp = ""
        arguments = []
        for letter in string:
            if letter != " ":
                temp += letter
            else:
                arguments.append(temp)
                temp = ""
        arguments.append(temp)
        return arguments

    # Mod chart string eval
    def modchartEvaluateString(string):
        arguments = modchartGetStringArguments(string)
        for k in range(len(arguments)):
            try:
                temp = int(arguments[k])
            except:
                temp = arguments[k]
            arguments[k] = temp
        for k in range(len(arguments)):
            if arguments[k] not in ["+", "-", "*", "/", "%", "^"] and getVariableValue(arguments[k]) is not None:
                arguments[k] = getVariableValue(arguments[k])
        total = 0
        print("Debug")
        print(total)
        # TODO: Problem here:
        if not isinstance(arguments[0], str):
            total = arguments[0]
        print(total)
        for k in range(len(arguments)):
            if isinstance(arguments[k], str):
                if arguments[k] == "+":
                    total += arguments[k + 1]
                elif arguments[k] == "-":
                    total -= arguments[k + 1]
                elif arguments[k] == "*":
                    total *= arguments[k + 1]
                elif arguments[k] == "/":
                    total /= arguments[k + 1]
                elif arguments[k] == "%":
                    total %= arguments[k + 1]
                elif arguments[k] == "^":
                    total **= arguments[k + 1]
        print("test: " + str(total))
        return total
    
    # Get var val
    def getVariableValue(variableName):
        try:
            temp = globals()[variableName]
            return temp
        except:
            try:
                temp = locals()[variableName]
                return temp
            except:
                return None
    
    # Get mc val
    def modchartGetValue(value):
        if isinstance(value, str):
            return modchartEvaluateString(value)
        else:
            return value

    # Transitions
    class transitionValue:
        def __init__(self, variable, startValue, endValue, startTime1, endTime):
            self.variable = variable
            self.startValue = startValue
            self.endValue = endValue
            self.startTime = startTime1
            self.endTime = endTime
            self.isActive = True

        def update(self):
            global arrow1Alpha
            global arrow2Alpha
            global character1Alpha
            global character2Alpha
            currentTime = Time.time() - startTime
            if self.endTime >= currentTime >= self.startTime:
                vector = self.endValue - self.startValue
                progress = (currentTime - self.startTime) / (self.endTime - self.startTime)
                value = self.startValue + (vector * progress)
                if self.variable == "arrow1Alpha":
                    arrow1Alpha = value
                elif self.variable == "arrow2Alpha":
                    arrow2Alpha = value
                elif self.variable == "character1Alpha":
                    character1Alpha = value
                elif self.variable == "character2Alpha":
                    character2Alpha = value
            elif currentTime > self.endTime:
                if self.variable == "arrow1Alpha":
                    arrow1Alpha = self.endValue
                elif self.variable == "arrow2Alpha":
                    arrow2Alpha = self.endValue
                elif self.variable == "character1Alpha":
                    character1Alpha = self.endValue
                elif self.variable == "character2Alpha":
                    character2Alpha = self.endValue
                self.isActive = False

    # Load GF
    gfEnabled = songData['gf']['Enabled']
    gfStyle = songData['gf']['style']
    gfAnim = songData['gf']['anim']
    gfOnCenter = songData['gf']['OnCenter']
    gfScale = songData['gf']['scale']
    gfFlipped = songData['gf']['flipped']
    gfPos = songData['gf']['pos']
    gfPixel = False
    pixelSong = False
    
    if 'pixel' in gfStyle:
        gfPixel = True
        pixelSong = True
    
    if gfEnabled:
        gfAnimation, gfOfsX, gfOfsY = loadAnimation(gfStyle, 'girlfriends')
        if gfOnCenter:
            gfPosX = middleScreen[0]
            gfPosY = middleScreen[1]
        else:
            gfPosX = gfPos[0]
            gfPosY = gfPos[1]

    # Character class
    class Character:
        def __init__(self, name, characterNum, loadedFromModchart=False, isPixel=pixelSong):
            
            if name != "None":
                if options.playAs == "Opponent":
                    if characterNum == 1:
                        temp = 2
                    else:
                        temp = 1
                else:
                    temp = characterNum
                
                # Load size and texture
                if not loadedFromModchart:
                    self.size = \
                        songData[f'character{temp}']['size']
                else:
                    self.size = \
                        songData['modchartCharacters'][name]['size']
                
                # Parse XML file and get texture based on XML indications
                self.texture = getXmlData(name, 'character')
                
                # Get offset
                try:
                    self.offset = json.load(open(f'data/characters/{name}/offset.json'))['offset']
                except:
                    self.offset = [[] for _ in range(5)]
                    for i in range(5):
                        for x in range(len(self.texture[i])):
                            self.offset[i].append([0, 0])
                if not loadedFromModchart:
                    try:
                        textureDirection = json.load(open(f'data/characters/{name}/characterData.json'))['texture_direction']
                    except:
                        textureDirection = "Right"
                else:
                    try:
                        textureDirection = json.load(open(f'data/characters/{name}/characterData.json'))['texture_direction']
                        if textureDirection == 'Right' and options.playAs == 'Opponent':
                            textureDirection = 'Left'
                    except:
                        textureDirection = 'Left'
                
                # Multiply offset by size
                for i in range(len(self.offset)):
                    for x in range(len(self.offset[i])):
                        self.offset[i][x][0] *= self.size[i][0]
                        self.offset[i][x][1] *= self.size[i][1]
                
                # Get pos
                if not loadedFromModchart:
                    self.pos = \
                        songData[f'character{temp}']['pos']
                else:
                    self.pos = \
                        songData['modchartCharacters'][name]['pos']
                
                self.isCentered = False
                               
                # Invert texture and offset when necessary
                if (textureDirection == "Left" and characterNum == 1) or (
                        textureDirection == "Right" and characterNum == 2):
                    for k in range(5):
                        for x in range(len(self.offset[k])):
                            self.offset[k][x][0] *= -1
                    for k in range(5):
                        for x in range(len(self.texture[k])):
                            self.texture[k][x] = transform.flip(self.texture[k][x], True, False)
                    temp1 = self.texture[0]
                    self.texture[0] = self.texture[3]
                    self.texture[3] = temp1
                    temp1 = self.offset[0]
                    self.offset[0] = self.offset[3]
                    self.offset[3] = temp1
                # Add offset to pos
                for k in range(5):
                    for x in range(len(self.offset[k])):
                        if characterNum == 1:
                            self.offset[k][x][0] = self.pos[0] + self.offset[k][x][0]
                            self.offset[k][x][1] = self.pos[1] + self.offset[k][x][1]
                        else:
                            self.offset[k][x][0] = self.pos[0] - self.offset[k][x][0]
                            self.offset[k][x][1] = self.pos[1] + self.offset[k][x][1]
                self.pos = self.offset
                # Scale texture to size
                for k in range(5):
                    for x in range(len(self.texture[k])):
                        if antiAliasing and not isPixel:
                            self.texture[k][x] = transform.smoothscale(self.texture[k][x], (
                                int(self.texture[k][x].get_width() * self.size[k][0]),
                                int(self.texture[k][x].get_height() * self.size[k][1])))
                        else:
                            self.texture[k][x] = transform.scale(self.texture[k][x], (
                                int(self.texture[k][x].get_width() * self.size[k][0]),
                                int(self.texture[k][x].get_height() * self.size[k][1])))
            # Handle no character
            else:
                self.texture = [[SysFont40.render("", 1, (255, 255, 255))] for _ in range(5)]
                self.pos = [[[0, 0]] for _ in range(5)]
    
    # Load chars
    if options.playAs == 'Player':
        # Load normal characters
        try:
            # Load opponent character
            characterName = songData["character1"]["Name"]
            alias = None
            if alias is None:
                loadedCharacters[characterName] = Character(characterName, 1)
                character1 = loadedCharacters[characterName]
            else:
                loadedCharacters[alias] = Character(characterName, 1)
                character1 = loadedCharacters[alias]
        except error as e:
            print("Opponent character loading failed, skipping loading")
            if options.debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character1 = Character("None", 1)
        try:
            # Load player character
            characterName = songData['character2']['Name']
            alias = None
            if alias is None:
                loadedCharacters[characterName] = Character(characterName, 2)
                character2 = loadedCharacters[characterName]
            else:
                loadedCharacters[alias] = Character(characterName, 2)
                character2 = loadedCharacters[alias]
        except:
            print("Player character loading failed, skipping loading")
            if options.debugMode:
                print("Debug mode stopped the program, printing error:")
                print(error)
            character2 = Character("None", 2)
    else:
        # Invert characters
        try:
            characterName = songData['character1']['Name']
            try:
                alias = songData['character1']['alias']
            except:
                alias = None
            if alias is None:
                loadedCharacters[characterName] = Character(characterName, 2)
                character2 = loadedCharacters[characterName]
            else:
                loadedCharacters[characterName] = Character(characterName, 2)
                character2 = loadedCharacters[alias]
        except error as e:
            print("Opponent character loading failed, skipping loading")
            if options.debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character2 = Character("None", 2)
        try:
            # Load player character
            characterName = songData['character2']['Name']
            try:
                alias = songData['character2']['alias']
            except:
                alias = None
            if alias is None:
                loadedCharacters[characterName] = Character(characterName, 1)
                character1 = loadedCharacters[characterName]
            else:
                loadedCharacters[alias] = Character(characterName, 1)
                character1 = loadedCharacters[alias]
        except error as e:
            print("Player character loading failed, skipping loading")
            if options.debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character1 = Character("None", 1)
    
    # Arrow texture class
    class arrowTexture:
        def __init__(self, skinName):
            temp = loadArrows(skinName)
            self.arrowsSkins = temp['arrowsSkin']
            for i in range(4):
                if self.arrowsSkins[i] is None:
                    self.arrowsSkins[i] = Surface((0, 0))
            self.pressedArrowsSkins = temp["pressedArrowsSkins"]
            for i in range(4):
                if self.pressedArrowsSkins[i] is None:
                    self.pressedArrowsSkins[i] = Surface((0, 0))
            self.greyArrow = temp["greyArrow"]
            for i in range(4):
                if self.greyArrow[i] is None:
                    self.greyArrow[i] = Surface((0, 0))
            self.longNotesImg = temp["longNotesImg"]
            for i in range(4):
                if self.longNotesImg[i] is None:
                    self.longNotesImg[i] = Surface((0, 0))
            if options.downscroll:
                for i in range(len(self.longNotesImg)):
                    self.longNotesImg[i] = transform.flip(self.longNotesImg[i], False, True)
            self.longNotesEnd = temp["longNotesEnd"]
            for i in range(4):
                if self.longNotesEnd[i] is None:
                    self.longNotesEnd[i] = Surface((0, 0))
            if options.downscroll:
                for i in range(len(self.longNotesEnd)):
                    self.longNotesEnd[i] = transform.flip(self.longNotesEnd[i], False, True)
    
    # Store arrow textures
    loadedArrowTextures = {"Main": arrowTexture(options.noteStyles[options.selectedNoteStyle])}
    loadedArrowTextures["Player"] = copy.copy(loadedArrowTextures["Main"])
    loadedArrowTextures["Opponent"] = copy.copy(loadedArrowTextures["Main"])

    """ # Get background rectangle
    BGrect = Background[0].get_rect()
    BGrect.bottomright = (currentW, currentH) """
    
    # Load BF death
    BFdead = image.load('data/characters/boyfriend/dead.png').convert_alpha()
    
    # Rectangles
    arrowRect = loadedArrowTextures["Main"].arrowsSkins[0].get_rect()
    deathScreenRect = BFdead.get_rect()
    deathScreenRect.midbottom = (middleScreen[0], currentH - 50)
    
    # Death screen music
    deathScreenMusic = mixer.Sound('data/sounds/deathBGM.ogg')
    deathScreenMusicEnd = mixer.Sound('data/sounds/deathEnd.ogg')
    deathScreenMusicStart = mixer.Sound('data/sounds/deathMicDrop.ogg')
    
    # Bopping speed
    boppingSpeed = songData['boppingSpeed']

    # Define song environment
    environmentType = songData['envType']
    songEnvironment = songData['stage']
    
    if songEnvironment == 'christmas-stage':
        if antiAliasing:
            songBG = transform.smoothscale(image.load('data/environments/christmas-stage/Background0.png'), (1600, 900)).convert_alpha()
        else:
            songBG = transform.scale(image.load('data/environments/christmas-stage/Background0.png'), (1600, 900)).convert_alpha()

        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])

        image1 = image.load('data/environments/christmas-stage/Stairs.png').convert_alpha()
        image2 = image.load('data/environments/christmas-stage/tree.png').convert_alpha()
        image3 = image.load('data/environments/christmas-stage/snow.png').convert_alpha()

        image1rect = image1.get_rect()
        image1rect.center = (middleScreen[0], middleScreen[1] - 50)
        image2rect = image2.get_rect()
        image2rect.center = (middleScreen[0], middleScreen[1])
        image3rect = image3.get_rect()
        image3rect.center = (middleScreen[0], middleScreen[1] + 330)

        christmasUpperBop, christmasUpperBopX, christmasUpperBopY = loadAnimation('christmasUpperBop', 'generic')
        christmasBottomBop, christmasBottomBopX, christmasBottomBopY = loadAnimation('christmasBottomBop', 'generic')
        christmasSanta, christmasSantaX, christmasSantaY = loadAnimation('christmasSanta', 'generic')
    elif songEnvironment == 'christmasblood-stage':
        if antiAliasing:
            songBG = transform.smoothscale(image.load('data/environments/christmasblood-stage/Background0.png'), (1600, 900)).convert_alpha()
        else:
            songBG = transform.scale(image.load('data/environments/christmasblood-stage/Background0.png'), (1600, 900)).convert_alpha()
        
        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])
        
        image1 = image.load('data/environments/christmasblood-stage/tree.png').convert_alpha()
        image2 = image.load('data/environments/christmasblood-stage/snow.png').convert_alpha()
        
        image1rect = image1.get_rect()
        image1rect.center = (middleScreen[0], middleScreen[1])
        image2rect = image2.get_rect()
        image2rect.center = (middleScreen[0], middleScreen[1] + 330)
    elif songEnvironment == 'daddy-stage':
        if antiAliasing:
            songBG = transform.smoothscale(image.load('data/environments/daddy-stage/Background0.png'), (1600, 900)).convert_alpha()
        else:
            songBG = transform.scale(image.load('data/environments/daddy-stage/Background0.png'), (1600, 900)).convert_alpha()

        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])
    elif songEnvironment == 'spooky-stage':
        if antiAliasing:
            songBG = transform.smoothscale(image.load('data/environments/spooky-stage/Background0.png'), (1600, 900)).convert_alpha()
        else:
            songBG = transform.scale(image.load('data/environments/spooky-stage/Background0.png'), (1600, 900)).convert_alpha()

        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])
    elif songEnvironment == 'pico-stage':
        if antiAliasing:
            songBG = transform.smoothscale(image.load('data/environments/pico-stage/Background0.png'), (1600, 900)).convert_alpha()
        else:
            songBG = transform.scale(image.load('data/environments/pico-stage/Background0.png'), (1600, 900)).convert_alpha()

        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])
    elif songEnvironment == 'tankman-stage':
        if antiAliasing:
            songBG = transform.smoothscale(image.load('data/environments/tankman-stage/Background0.png'), (1600, 900)).convert_alpha()
        else:
            songBG = transform.scale(image.load('data/environments/tankman-stage/Background0.png'), (1600, 900)).convert_alpha()

        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])

        image1 = image.load('data/environments/tankman-stage/foreground.png').convert_alpha()
        image1rect = image1.get_rect()
        image1rect.center = (middleScreen[0], middleScreen[1] - 20)

        smokeLeft, smokeLeftX, smokeLeftY = loadAnimation('smokeLeft', 'generic')
        smokeRight, smokeRightX, smokeRightY = loadAnimation('smokeRight', 'generic')
        watchTower, watchTowerOffsetX, watchTowerOffsetY = loadAnimation('tankWatchTower', 'generic')
        tank0, tank0X, tank0Y = loadAnimation('tank0', 'generic')
        tank1, tank1X, tank1Y = loadAnimation('tank1', 'generic')
        tank2, tank2X, tank2Y = loadAnimation('tank2', 'generic')
        tank3, tank3X, tank3Y = loadAnimation('tank3', 'generic')
        tank4, tank4X, tank4Y = loadAnimation('tank4', 'generic')
        tank5, tank5X, tank5Y = loadAnimation('tank5', 'generic')
    elif songEnvironment == 'mommy-stage':
        if antiAliasing:
            songBG = transform.smoothscale(image.load('data/environments/mommy-stage/Background0.png'), (1600, 900)).convert_alpha()
        else:
            songBG = transform.scale(image.load('data/environments/mommy-stage/Background0.png'), (1600, 900)).convert_alpha()

        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])

        bgLimo, bgLimoX, bgLimoY = loadAnimation('bgLimo', 'generic')
        limoDancer, limoDancerX, limoDancerY = loadAnimation('limoDancer', 'generic')
        limoDrive, limoDriveX, limoDriveY = loadAnimation('limoDrive', 'generic')
        girlfriend, girlfriendX, girlfriendY = loadAnimation('girlfriend-speaker', 'girlfriends')
    elif songEnvironment == 'weeb-stage':
        songBG = transform.scale(image.load(f'data/environments/{songEnvironment}/Background0.png'), (currentW, currentH)).convert_alpha()
        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])
        bgFreaks, bgFreaksX, bgFreaksY = loadAnimation('freaks-group', 'generic')
    elif songEnvironment == 'weeb-dark-stage':
        songBG = transform.scale(image.load(f'data/environments/{songEnvironment}/Background0.png'), (currentW, currentH)).convert_alpha()
        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])
        bgFreaks, bgFreaksX, bgFreaksY = loadAnimation('freaks-dissuaded', 'generic')
    elif songEnvironment == 'weeb-blood-stage':
        songBG = transform.scale(image.load(f'data/environments/{songEnvironment}/Background0.png'), (currentW, currentH)).convert_alpha()
        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])
        evilSchool, evilSchoolX, evilSchoolY = loadAnimation('evilSchool', 'generic')
        bgFreaks, bgFreaksX, bgFreaksY = loadAnimation('freaks-ghoul', 'generic')
    elif environmentType == 'custom':
        if antiAliasing:
            songBG = transform.smoothscale(image.load(f'data/environments/{songEnvironment}/Background0.png'), (currentW, currentH)).convert_alpha()
        else:
            songBG = transform.smoothscale(image.load(f'data/environments/{songEnvironment}/Background0.png'), (currentW, currentH)).convert_alpha()
        songBGrect = songBG.get_rect()
        songBGrect.center = (middleScreen[0], middleScreen[1])
    
    def drawChristmasScene():
        renderSurface.blit(songBG, songBGrect)
        if not potatoMode:
            drawAnimation(christmasUpperBop, (middleScreen[0], middleScreen[1] + 550), 
                    0.75, 'metaanim', boppingSpeed, False, christmasUpperBopX, christmasUpperBopY)
        renderSurface.blit(image1, image1rect)
        renderSurface.blit(image2, image2rect)
        if not potatoMode:
            drawAnimation(christmasBottomBop, (middleScreen[0], middleScreen[1] + 550), 
                        0.75, 'metaanim', boppingSpeed, False, christmasBottomBopX, christmasBottomBopY)
        renderSurface.blit(image3, image3rect)
        if not potatoMode:
            drawAnimation(christmasSanta, (middleScreen[0] - 750, middleScreen[1] + 200), 
                        0.55, 'metaanim', boppingSpeed, False, christmasSantaX, christmasSantaY)
    def drawChristmasBloodScene():
        renderSurface.blit(songBG, songBGrect)
        renderSurface.blit(image1, image1rect)
        renderSurface.blit(image2, image2rect)
    def drawDaddyScene():
        renderSurface.blit(songBG, songBGrect)
    def drawSpookyScene():
        renderSurface.blit(songBG, songBGrect)
    def drawPicoScene():
        renderSurface.blit(songBG, songBGrect)
    def drawMommyScene():
        renderSurface.blit(songBG, songBGrect)
        if not potatoMode:
            drawAnimation(bgLimo, (middleScreen[0] + 300, middleScreen[1] + 1250), 1, 'metaanim', 24, False, bgLimoX, bgLimoY)
            drawAnimation(limoDancer, (middleScreen[0] - 210, middleScreen[1]), 1, 'metaanim', 24, False, limoDancerX, limoDancerY)
            drawAnimation(limoDancer, (middleScreen[0] + 140, middleScreen[1]), 1, 'metaanim', 24, False, limoDancerX, limoDancerY)
            drawAnimation(limoDancer, (middleScreen[0] + 500, middleScreen[1]), 1, 'metaanim', 24, False, limoDancerX, limoDancerY)
        drawAnimation(girlfriend, (middleScreen[0], middleScreen[1] + 150), 1, 'hairblowing', 24, True, girlfriendX, girlfriendY)
        drawAnimation(limoDrive, (middleScreen[0] + 150, middleScreen[1] + 1200), 1, 'metaanim', 24, False, limoDriveX, limoDriveY)
    def drawTankmanScene():
        renderSurface.blit(songBG, songBGrect)
        if not potatoMode:
            drawAnimation(watchTower, (middleScreen[0] - 450, middleScreen[1] - 200),
                        0.8, 'towerbop', boppingSpeed, False, watchTowerOffsetX, watchTowerOffsetY)
            drawAnimation(smokeLeft, (middleScreen[0] - 600, middleScreen[1] - 200), 
                        0.6, 'metaanim', boppingSpeed, False, smokeLeftX, smokeLeftY)
            drawAnimation(smokeRight, (middleScreen[0] + 680, middleScreen[1] - 200),
                        0.6, 'metaanim', boppingSpeed, False, smokeRightX, smokeRightY)
        renderSurface.blit(image1, image1rect)
        if not potatoMode:
            drawAnimation(tank0, (middleScreen[0] - 690, middleScreen[1] + 280),
                        0.8, 'metaanim', boppingSpeed, False, tank0X, tank0Y)
            drawAnimation(tank1, (middleScreen[0] - 420, middleScreen[1] + 550),
                        0.8, 'metaanim', boppingSpeed, False, tank1X, tank1Y)
            drawAnimation(tank2, (middleScreen[0] - 100, middleScreen[1] + 460),
                        0.8, 'metaanim', boppingSpeed, False, tank2X, tank2Y)
            drawAnimation(tank3, (middleScreen[0] + 150, middleScreen[1] + 565),
                        0.7, 'metaanim', boppingSpeed, False, tank3X, tank3Y)
            drawAnimation(tank4, (middleScreen[0] + 500, middleScreen[1] + 460),
                        0.7, 'metaanim', boppingSpeed, False, tank4X, tank4Y)
            drawAnimation(tank5, (middleScreen[0] + 680, middleScreen[1] + 280),
                        0.8, 'metaanim', boppingSpeed, False, tank5X, tank5Y)
    def drawWeebScene():
        renderSurface.blit(songBG, songBGrect)
        if not potatoMode:
            drawAnimation(bgFreaks, (middleScreen[0], middleScreen[1] + 900),
                          5, 'metaanim', boppingSpeed, False, bgFreaksX, bgFreaksY, True)
    def drawWeebDarkScene():
        renderSurface.blit(songBG, songBGrect)
        drawAnimation(bgFreaks, (middleScreen[0], middleScreen[1] + 900),
                          5, 'metaanim', boppingSpeed, False, bgFreaksX, bgFreaksY, True)
    def drawWeebBloodScene():
        renderSurface.blit(songBG, songBGrect)
        drawAnimation(evilSchool, (middleScreen[0], middleScreen[1]),
                      6.5, 'metaanim', boppingSpeed, False, evilSchoolX, evilSchoolY, True)
        drawAnimation(bgFreaks, (middleScreen[0], middleScreen[1] + 900),
                          5, 'metaanim', boppingSpeed, False, bgFreaksX, bgFreaksY, True)
    def drawCustomScene():
        renderSurface.blit(songBG, songBGrect)

    # Gameplay startup sequence
    modchartLoading()
    countdown()
    keyPressed = []
    startTime = Time.time()
    Inst.play()
    Vocals.play()
    Inst.set_volume(volume)
    Vocals.set_volume(volume)
    
    # Gameplay loop
    while True:
        frameTimer += clock.tick()
        currentTime = (Time.time() - startTime) * 1000
        notesToClear = [[], [], [], []]
        for events in event.get():
            if events.type == QUIT:
                exit()
            if events.type == KEYDOWN and events.key == K_ESCAPE:
                Inst.stop()
                Vocals.stop()
                return False
            if events.type == KEYDOWN:
                keyPressed.append(events.key)
            if events.type == KEYDOWN and events.key == K_SPACE:
                print(f'Debug: Current song position: {((Time.time() - startTime) * 1000)}')
            if events.type == KEYUP and events.key in keyPressed:
                keyPressed.remove(events.key)
            if events.type == KEYDOWN:
                currentTime = Time.time() - startTime
                testNotes = True
                for note in notesChart:
                    if testNotes:
                        if note.pos <= currentTime * 1000 + 133:
                            if note.side == "Player" and currentTime * 1000 - 133 <= note.pos <= currentTime * 1000 + 133 and note.column in [
                                "Left", "Down", "Up", "Right"]:
                                if (events.key == K_a or events.key == K_LEFT) and note.column == "Left":
                                    notesToClear[0].append(note)
                                if (events.key == K_s or events.key == K_DOWN) and note.column == "Down":
                                    notesToClear[1].append(note)
                                if (events.key == K_w or events.key == K_UP) and note.column == "Up":
                                    notesToClear[2].append(note)
                                if (events.key == K_d or events.key == K_RIGHT) and note.column == "Right":
                                    notesToClear[3].append(note)
                        else:
                            testNotes = False
        currentTime = Time.time() - startTime
        for k in range(4):
            if len(notesToClear[k]) > 0:
                gamemin = notesToClear[k][0].pos
                gameminX = 0
                x = 0
                for element in notesToClear[k]:
                    if element.pos < gamemin:
                        gamemin = element.pos
                        gameminX = x
                    x += 1
                accuracy = str(round(notesToClear[k][gameminX].pos - currentTime * 1000, 2))
                if not notesToClear[k][gameminX].mustAvoid:
                    showAccuracy = True
                    accuracyDisplayTime = Time.time()
                executeNoteModchart = True
                if currentTime * 1000 + 47 >= notesToClear[k][gameminX].pos >= currentTime * 1000 - 47:
                    if not notesToClear[k][gameminX].mustAvoid:
                        accuracyIndicator = accuracyIndicatorImages[0].convert_alpha()
                        accuracyPercentList.append(1)
                        combo += 1
                    else:
                        misses += 1
                        combo = 0
                    health += notesToClear[k][gameminX].bigHealthBoost
                elif currentTime * 1000 + 79 >= notesToClear[k][gameminX].pos >= currentTime * 1000 - 79:
                    if not notesToClear[k][gameminX].mustAvoid:
                        accuracyIndicator = accuracyIndicatorImages[1].convert_alpha()
                        accuracyPercentList.append(0.75)
                        combo += 1
                    else:
                        misses += 1
                        combo = 0
                    health += notesToClear[k][gameminX].smallHealthBoost
                elif currentTime * 1000 + 109 >= notesToClear[k][gameminX].pos >= currentTime * 1000 - 109:
                    if not notesToClear[k][gameminX].mustAvoid:
                        accuracyIndicator = accuracyIndicatorImages[2].convert_alpha()
                        accuracyPercentList.append(0.5)
                        combo += 1
                    else:
                        misses += 1
                        combo = 0
                    health += notesToClear[k][gameminX].smallHealthBoost
                else:
                    if not notesToClear[k][gameminX].mustAvoid:
                        accuracyIndicator = accuracyIndicatorImages[3].convert_alpha()
                        accuracyPercentList.append(-1)
                    misses += 1
                    combo = 0
                    health -= notesToClear[k][gameminX].healthPenalty
                    executeNoteModchart = False
                if not notesToClear[k][gameminX].mustAvoid:
                    playerAnimation = [notesToClear[k][gameminX].column, currentTime]
                if executeNoteModchart:
                    update_modifications(notesToClear[k][gameminX].hitModchart, notesToClear[k][gameminX].hitModchart)
                notesChart.remove(notesToClear[k][gameminX])
        if health > 100:
            health = 100
        renderSurface.fill((0, 0, 0))
        
        # Graphics
        update_modifications(modifications, dynamicModifications)
        update_transitionValue()
        if environmentType == 'custom':
            drawCustomScene()
        elif environmentType == 'blank':
            renderSurface.fill((20, 20, 20))
        elif environmentType == 'preset':
            if songEnvironment == 'christmas-stage':
                drawChristmasScene()
            elif songEnvironment == 'christmasblood-stage':
                drawChristmasBloodScene()
            elif songEnvironment == 'daddy-stage':
                drawDaddyScene()
            elif songEnvironment == 'spooky-stage':
                drawSpookyScene()
            elif songEnvironment == 'pico-stage':
                drawPicoScene()
            elif songEnvironment == 'mommy-stage':
                drawMommyScene()
            elif songEnvironment == 'tankman-stage':
                drawTankmanScene()
            elif songEnvironment == 'weeb-stage':
                drawWeebScene()
            elif songEnvironment == 'weeb-dark-stage':
                drawWeebDarkScene()
            elif songEnvironment == 'weeb-blood-stage':
                drawWeebBloodScene()
        if gfEnabled and not potatoMode:
            if not gfPixel:
                drawAnimation(gfAnimation, (gfPosX, gfPosY), gfScale, gfAnim, boppingSpeed, gfFlipped, gfOfsX, gfOfsY)
            else:
                drawAnimation(gfAnimation, (gfPosX, gfPosY), gfScale, gfAnim, boppingSpeed, gfFlipped, gfOfsX, gfOfsY, True)
        drawCharacters()
        drawLongNotes()
        drawGreyNotes()
        drawNotes()
        drawProgressBar()
        
        # draw bottom info bar
        if len(accuracyPercentList) == 0:
            tempAccuracy = "NA"
        else:
            temp = 0
            for element in accuracyPercentList:
                temp += element
            temp /= len(accuracyPercentList)
            tempAccuracy = "{0}%".format(round(temp * 100, 2))
        if options.coloredInfo:
            text1 = "Combo: {0} | Misses: {1} | ".format(combo, misses)
            text2 = "Accuracy: {0}".format(tempAccuracy)
            if options.healthFormat == "Healthbar":
                text3 = ""
            else:
                text3 = " | Health: {0}%".format(round(health, 2))
            biggest_height = 0
            tmp_width = 0
            tempText1 = text1 + text2 + text3
            for k in range(len(tempText1)):
                tmp = SysFont30.render(tempText1[k], 1, (255, 255, 255)).get_rect()
                if tmp.height > biggest_height:
                    biggest_height = tmp.height
                tmp_width += tmp.width
            tempText = Surface((tmp_width, biggest_height), flags=SRCALPHA)
            tempText = tempText.convert_alpha()
            tempText.fill((0, 0, 0, 0))
            current_x = 0
            for k in range(len(text1)):
                tempLetter = SysFont30.render(text1[k], 1, (255, 255, 255))
                tempText.blit(tempLetter, (current_x, 0))
                current_x += tempLetter.get_rect().width
            if len(accuracyPercentList) == 0:
                tempColor = (255, 255, 255)
            elif round(temp * 100, 2) >= 85:
                tempColor = (0, 255, 0)
            elif 85 >= round(temp * 100, 2) > 70:
                tempColor = (210, 139, 0)
            else:
                tempColor = (255, 0, 0)
            for k in range(len(text2)):
                tempLetter = SysFont30.render(text2[k], 1, tempColor)
                tempText.blit(tempLetter, (current_x, 0))
                current_x += tempLetter.get_rect().width
            if health >= 75:
                tempColor = (0, 255, 0)
            elif 75 > health >= 50:
                tempColor = (210, 139, 0)
            elif health < 50:
                tempColor = (255, 0, 0)
            else:
                tempColor = (255, 255, 255)
            for k in range(len(text3)):
                if k > 1:
                    tempLetter = SysFont30.render(text3[k], 1, tempColor)
                else:
                    tempLetter = SysFont30.render(text3[k], 1, (255, 255, 255))
                tempText.blit(tempLetter, (current_x, 0))
                current_x += tempLetter.get_rect().width
            temp1 = tempText.get_rect()
            if not options.downscroll:
                temp1.midbottom = (middleScreen[0], currentH - 70)
            else:
                temp1.midtop = (middleScreen[0], 75)
            renderSurface.blit(tempText, temp1)
        else:
            if options.healthFormat == "Healthbar":
                temp = SysFont30.render("Combo: {0} | Misses: {1} | Accuracy: {2}".format(combo, misses, tempAccuracy), 1,
                                     (255, 255, 255))
            else:
                temp = SysFont30.render(
                    "Combo: {0} | Misses: {1} | Accuracy: {2} | Health: {3}%".format(combo, misses, tempAccuracy,
                                                                                     round(health, 2)), 1,
                    (255, 255, 255))
            temp1 = temp.get_rect()
            if not options.downscroll:
                temp1.midbottom = (middleScreen[0], currentH - 10)
            else:
                temp1.midtop = (middleScreen[0], 75)
            renderSurface.blit(temp, temp1)
        
        # Accuracy display
        if Time.time() - accuracyDisplayTime > 0.5:
            showAccuracy = False
        if showAccuracy:
            temp = SysFont30.render(accuracy, 1, (255, 255, 255))
            temp1 = temp.get_rect()
            temp1.center = (middleScreen[0], middleScreen[1] + 270)
            renderSurface.blit(temp, temp1)
            renderSurface.blit(accuracyIndicator, (middleScreen[0] - 100, middleScreen[1] + 160))

        # FPS
        fps = 1 / (Time.time() - fpsTime)
        fpsTime = Time.time()
        fpsList.append(fps)
        temp = 0
        for element in fpsList:
            temp += element
        temp /= len(fpsList)
        while len(fpsList) > fpsQuality:
            fpsList.remove(fpsList[0])
        renderSurface.blit(SysFont40.render(str(round(temp, 2)), 1, (255, 255, 255)), Rect(5, 0, 0, 0))
        
        # Health bar
        if options.healthFormat == "Healthbar":
            drawHealthBar()
        
        # Final draw
        scaled_surface = transform.smoothscale(renderSurface, displayResolution)
        scaledWindow.blit(scaled_surface, (0, 0))
        display.flip()
        if Time.time() - startTime > songLen:
            Inst.stop()
            Vocals.stop()
            sceneLoaded = False
            return False
        if health <= 0 and not options.noDying:
            Inst.stop()
            Vocals.stop()
            return death()

# Initial loading screen
loadingScreen()

# Load menu characters
boyfriend, boyfriendX, boyfriendY = loadAnimation('boyfriend', 'character')
girlfriend, girlfriendX, girlfriendY = loadAnimation('girlfriend-speaker', 'girlfriends')
daddy, daddyX, daddyY = loadAnimation('daddy', 'character')
spookykids, spookyX, spookyY = loadAnimation('spookykids', 'character')
monster, monsterX, monsterY = loadAnimation('monster', 'character')
pico, picoX, picoY = loadAnimation('pico', 'character')
mommy, mommyX, mommyY = loadAnimation('mommy', 'character')
momdad, momdadX, momdadY = loadAnimation('momanddadxmas-dad', 'character')
monsterChristmas, monsterChX, monsterChY = loadAnimation('monsterChristmas', 'character')
senpai, senpaiX, senpaiY = loadAnimation('senpai', 'character')
senpaiPissed, senpaiPissedX, senpaiPissedY = loadAnimation('senpai-pissed', 'character')
senpaiBlood, senpaiBloodX, senpaiBloodY = loadAnimation('senpai-blood', 'character')
tankman, tankmanX, tankmanY = loadAnimation('tankman', 'character')

# Audio stuff
# Play menu music & set SFX
threeSFX = mixer.Sound('data/sounds/3.ogg')
twoSFX = mixer.Sound('data/sounds/2.ogg')
oneSFX = mixer.Sound('data/sounds/1.ogg')
goSFX = mixer.Sound('data/sounds/go.ogg')
dahSFX = mixer.Sound('data/sounds/dah.ogg')
staticSFX = mixer.Sound('data/sounds/staticSound.ogg')
menuSFX = mixer.Sound('data/sounds/menuNavigation.ogg')
menuCancel = mixer.Sound('data/sounds/cancelMenu.ogg')
menuConfirm = mixer.Sound('data/sounds/confirmMenu.ogg')
menuMusic = mixer.Sound('data/sounds/menuBGM.ogg')
menuMusic.play(-1)
for channel in range(mixer.get_num_channels()):
    mixer.Channel(channel).set_volume(volume)

# Menu loop
while running:
    # Update frame timer
    frameTimer += clock.tick()
    
    # Volume fade animation
    volAnimCurrentTime = time.get_ticks()
    if volFadeIn:
        volFadeAlpha = min((volAnimCurrentTime - volFadeTimer) / volFadeDuration * 255, 255)
        if volFadeAlpha >= 255:
            volFadeIn = False
            volFadeTimer = volAnimCurrentTime + 1000
            volFadeOut = True
    elif volFadeOut:
        volFadeAlpha = max(255 - (volAnimCurrentTime - volFadeTimer) / volFadeDuration * 255, 0)
        if volFadeAlpha <= 0:
            volFadeOut = False
    
    # Window title
    display.set_caption(f'YellowFox Engine | {currVersion}')
    
    # Draw startup sequence
    if not startupRan:
        startup()
    
    # Default white bg
    renderSurface.fill((255, 255, 255))
        
    # Draw menu background
    renderSurface.blit(menuBG, rectBG)
    
    # Draw top and bottom rects
    renderSurface.blit(topRect, (rects_x, topRectY))
    renderSurface.blit(bottomRect, (rects_x, bottomRectY))
    
    # Draw info text
    renderSurface.blit(infoText, (15, 15))
    renderSurface.blit(infoText2, (currentW - 320, 15))
    
    # Draw volume text
    volumeText = SysFont30.render(f'Volume: {volume:.1f}', True, (255, 255, 255))
    volumeText.set_alpha(volFadeAlpha)
    volumeTextRect = volumeText.get_rect()
    volumeTextRect.center = (middleScreen[0], middleScreen[1] - 417)
    renderSurface.blit(volumeText, volumeTextRect)
    
    # Events handling
    for events in event.get():
        # Handle go back with ESC
        if events.type == QUIT or (events.type == KEYDOWN and events.key == K_ESCAPE):
            if currentMenu == 'Main':
                options.saveOptions()
                running = False
            else:
                if currentMenu == 'Keybinds':
                    menuCancel.play()
                    currentMenu = 'Options'
                elif currentMenu == 'Edit keybinds':
                    menuCancel.play()
                    currentMenu = 'Keybinds'
                else:
                    menuCancel.play()
                    currentMenu = 'Main'
        
         # Handle volume change
        if events.type == KEYDOWN:
            if events.key == K_EQUALS or events.key == K_PLUS or events.key == K_KP_PLUS:
                volume += 0.1
                volume = min(volume, 1.0)
                for channel in range(mixer.get_num_channels()):
                    mixer.Channel(channel).set_volume(volume)
                print('Current volume: ', f'{volume:.1f}')
                dahSFX.play()
                volFadeTimer = time.get_ticks()
                volFadeIn = True
                volFadeOut = False
            elif events.key == K_MINUS or events.key == K_KP_MINUS:
                volume -= 0.1
                volume = max(volume, 0.0)
                for channel in range(mixer.get_num_channels()):
                    mixer.Channel(channel).set_volume(volume)
                dahSFX.play()
                print('Current volume: ', f'{volume:.1f}')
                volFadeTimer = time.get_ticks()
                volFadeIn = True
                volFadeOut = False
        
        # Do X in select song menu
        if events.type == KEYDOWN and events.key == K_RETURN:
            if currentMenu == 'Select song':
                menuMusic.stop()
                """ menuConfirm.play() """
                restart = True
                while restart:
                    options.saveOptions()
                    options.update()
                    Inst = None
                    Vocals = None
                    chart = None
                    misses = 0
                    health = 50
                    BG = None
                    opponentAnimation = ['Up', -10]
                    playerAnimation = ['Up', -10]
                    hasPlayedMicDrop = False
                    combo = 0
                    bpm = 60000 / 100
                    arrow1Alpha = 1
                    arrow2Aplha = 1
                    character1 = None
                    character2 = None
                    character1Alpha = 1
                    character2Alpha = 1
                    if not options.debugMode:
                        try:
                            restart = mainGame(songList[selectedSong], options)
                        except:
                            restart = False
                    else:
                        restart = mainGame(songList[selectedSong], options)
                menuMusic.play(-1)
                menuMusic.set_volume(volume)
                
            # Do X in main menu
            if currentMenu == 'Main':
                if selectedMain == 0:
                    menuConfirm.play()
                    currentMenu = 'Select song'
                if selectedMain == 1:
                    menuConfirm.play()
                    currentMenu = 'Options'
                    preventDoubleEnter = True
        
        # Grab keydown event
        if events.type == KEYDOWN:
            # Do X in select menu (again)
            if currentMenu == "Select song":
                if (events.key == K_w or ((events.key == K_UP and K_UP != 1073741906 and K_DOWN != 1073741906) or (
                        events.key == 1073741906))) and selectedSong > 0:
                    menuSFX.play()
                    selectedSong -= 1
                if (events.key == K_s or ((events.key == K_DOWN and K_DOWN != 1073741905 and K_UP != 1073741905) or (
                        events.key == 1073741905))) and selectedSong < len(songList) - 1:
                    menuSFX.play()
                    selectedSong += 1
        
        # Do X in options menu
            if currentMenu == "Options":
                if (events.key == K_w or ((events.key == K_UP and K_UP != 1073741906 and K_DOWN != 1073741906) or (
                        events.key == 1073741906))) and selectedOption > 0:
                    menuSFX.play()
                    selectedOption -= 1
                if (events.key == K_s or ((events.key == K_DOWN and K_DOWN != 1073741905 and K_UP != 1073741905) or (
                        events.key == 1073741905))) and selectedOption < 8:
                    menuSFX.play()
                    selectedOption += 1
                if selectedOption == 0:
                    if (events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904))) and options.selectedSpeed > 0.1:
                        options.selectedSpeed -= 0.1
                        options.selectedSpeed = round(options.selectedSpeed, 1)
                    if events.key == K_d or (
                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                            events.key == 1073741903)):
                        options.selectedSpeed += 0.1
                        options.selectedSpeed = round(options.selectedSpeed, 1)
                if selectedOption == 1 and (events.key == K_a or (
                                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                                            events.key == 1073741904)) or events.key == K_d or events.key == K_RIGHT):
                    if options.playAs == "Player":
                        options.playAs = "Opponent"
                    else:
                        options.playAs = "Player"
                if selectedOption == 2 and (events.key == K_a or (
                                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                                            events.key == 1073741904)) or events.key == K_d or events.key == K_RIGHT):
                    if options.noDying:
                        options.noDying = False
                    else:
                        options.noDying = True
                if selectedOption == 3:
                    if (events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904))) and options.selectedNoteStyle > 0:
                        options.selectedNoteStyle -= 1
                    if (events.key == K_d or (
                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                            events.key == 1073741903))) and options.selectedNoteStyle < len(
                        noteStyles) - 1:
                        options.selectedNoteStyle += 1
                if selectedOption == 4 and ((events.key == K_a or (
                                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                                            events.key == 1073741904))) or (events.key == K_d or (
                                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                                            events.key == 1073741903)))):
                    options.downscroll = not options.downscroll
                if selectedOption == 5 and ((events.key == K_a or (
                                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                                            events.key == 1073741904))) or (events.key == K_d or (
                                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                                            events.key == 1073741903)))):
                    options.debugMode = not options.debugMode
                if selectedOption == 6 and ((events.key == K_a or (
                                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                                            events.key == 1073741904))) or (events.key == K_d or (
                                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                                            events.key == 1073741903)))):
                    if options.healthFormat == "Healthbar":
                        options.healthFormat = "Infobar"
                    else:
                        options.healthFormat = "Healthbar"
                if selectedOption == 7 and ((events.key == K_a or (
                                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                                            events.key == 1073741904))) or (events.key == K_d or (
                                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                                            events.key == 1073741903)))):
                    options.coloredInfo = not options.coloredInfo
                if selectedOption == 8 and (events.key == K_RETURN and not preventDoubleEnter):
                    menuConfirm.play()
                    currentMenu = "Keybinds"
                    preventDoubleEnter = True
            
            # Do X in main menu (again)
            if currentMenu == "Main":
                if (events.key == K_w or ((events.key == K_UP and K_UP != 1073741906 and K_DOWN != 1073741906) or (
                        events.key == 1073741906))) and selectedMain > 0:
                    menuSFX.play()
                    selectedMain -= 1
                if (events.key == K_s or ((events.key == K_DOWN and K_DOWN != 1073741905 and K_UP != 1073741905) or (
                        events.key == 1073741905))) and selectedMain < 1:
                    menuSFX.play()
                    selectedMain += 1
            
            # Do X in keybinds menu
            if currentMenu == "Keybinds":
                if (events.key == K_w or ((events.key == K_UP and K_UP != 1073741906 and K_DOWN != 1073741906) or (
                        events.key == 1073741906))) and selectedKeybind > 0:
                    menuSFX.play()
                    selectedKeybind -= 1
                if (events.key == K_s or ((events.key == K_DOWN and K_DOWN != 1073741905 and K_UP != 1073741905) or (
                        events.key == 1073741905))) and selectedKeybind < 8:
                    menuSFX.play()
                    selectedKeybind += 1
                if events.key == K_RETURN and not preventDoubleEnter and selectedKeybind < 8:
                    currentMenu = "Edit keybinds"
                if events.key == K_RETURN and not preventDoubleEnter and selectedKeybind == 8:
                    K_a = 97
                    K_s = 115
                    K_w = 119
                    K_d = 100
                    K_LEFT = 1073741904
                    K_DOWN = 1073741905
                    K_UP = 1073741906
                    K_RIGHT = 1073741903
            
            # Do X in edit keybinds menu
            if currentMenu == "Edit keybinds":
                if events.key == K_ESCAPE:
                    currentMenu = "Keybinds"
                elif events.key not in [K_RETURN, K_BACKSPACE, K_ESCAPE, K_SPACE, KMOD_SHIFT, KMOD_CTRL, KMOD_ALT,
                                        KMOD_CAPS] and events.key not in [K_a, K_s, K_w, K_d, K_LEFT, K_DOWN, K_UP,
                                                                          K_RIGHT]:
                    temp = False
                    if selectedKeybind == 0:
                        K_a = events.key
                        temp = True
                    if selectedKeybind == 1:
                        K_s = events.key
                        temp = True
                    if selectedKeybind == 2:
                        K_w = events.key
                        temp = True
                    if selectedKeybind == 3:
                        K_d = events.key
                        temp = True
                    if selectedKeybind == 4:
                        K_LEFT = events.key
                        temp = True
                    if selectedKeybind == 5:
                        K_DOWN = events.key
                        temp = True
                    if selectedKeybind == 6:
                        K_UP = events.key
                        temp = True
                    if selectedKeybind == 7:
                        K_RIGHT = events.key
                        temp = True
                    if temp:
                        currentMenu = "Keybinds"
                        
        # Reset double enter prevention
        preventDoubleEnter = False
    
    # Volume fade animation
    volAnimCurrentTime = time.get_ticks()
    if volFadeIn:
        volFadeAlpha = min((volAnimCurrentTime - volFadeTimer) / volFadeDuration * 255, 255)
        if volFadeAlpha >= 255:
            volFadeIn = False
            volFadeTimer = volAnimCurrentTime + 1000
            volFadeOut = True
    elif volFadeOut:
        volFadeAlpha = max(255 - (volAnimCurrentTime - volFadeTimer) / volFadeDuration * 255, 0)
        if volFadeAlpha <= 0:
            volFadeOut = False
    
    # Draw menus
    if currentMenu == 'Main':
        if startupRan:
            drawMain()
            drawAnimation(girlfriend, (currentW - 380, currentH - 380), 1, 'dancingbeat', 24, False, girlfriendX, girlfriendY)
    elif currentMenu == 'Options':
        drawOptions()
        drawAnimation(boyfriend, (currentW - 320, currentH - 270), 1, 'BF idle dance', 20, False, boyfriendX, boyfriendY)
    elif currentMenu == 'Select song':
        drawSongs()
        if selectedSong == 0 or selectedSong == 1 or selectedSong == 2:
            drawAnimation(daddy, (currentW - 320, currentH - 610), 1, 'idle', 20, True, daddyX, daddyY)
        elif selectedSong == 3 or selectedSong == 4:
            drawAnimation(spookykids, (currentW - 320, currentH - 370), 1, 'idle', 20, True, spookyX, spookyY)
        elif selectedSong == 5:
            drawAnimation(monster, (currentW - 320, currentH - 480), 1, 'monster idle', 24, True, monsterX, monsterY)
        elif selectedSong == 6 or selectedSong == 7 or selectedSong == 8:
            drawAnimation(pico, (currentW - 320, currentH - 320), 1, 'Pico Idle Dance', 24, False, picoX, picoY)
        elif selectedSong == 9 or selectedSong == 10 or selectedSong == 11:
            drawAnimation(mommy, (currentW - 320, currentH - 680), 1, 'idle', 24, True, mommyX, mommyY)
        elif selectedSong == 12 or selectedSong == 13:
            drawAnimation(momdad, (currentW - 320, currentH - 380), 1, 'idle', 24, True, momdadX, momdadY)
        elif selectedSong == 14:
            drawAnimation(monsterChristmas, (currentW - 320, currentH - 510), 1, 'monster idle', 24, True, monsterChX, monsterChY)
        elif selectedSong == 15:
            drawAnimation(senpai, (currentW - 335, currentH - 580), 6, 'idle', 24, True, senpaiX, senpaiY, True)
        elif selectedSong == 16:
            drawAnimation(senpaiPissed, (currentW - 340, currentH - 580), 6, 'idle', 24, True, senpaiPissedX, senpaiPissedY, True)
        elif selectedSong == 17:
            drawAnimation(senpaiBlood, (currentW - 400, currentH - 400), 6, 'idle', 24, True, senpaiBloodX, senpaiBloodY, True)
        elif selectedSong == 18 or selectedSong == 19 or selectedSong == 20:
            drawAnimation(tankman, (currentW - 320, currentH - 420), 1, 'idle1', 24, False, tankmanX, tankmanY)
    elif currentMenu == 'Keybinds':
        drawKeybinds()
        drawAnimation(boyfriend, (currentW - 320, currentH - 270), 1, 'BF idle dance', 20, False, boyfriendX, boyfriendY)
    elif currentMenu == 'Edit keybinds':
        drawEditKeybinds()
    
    if antiAliasing:
        scaled_surface = transform.smoothscale(renderSurface, displayResolution)
    else:
        scaled_surface = transform.scale(renderSurface, displayResolution)
    scaledWindow.blit(scaled_surface, (0, 0))
    
    # Update screen
    display.update()

# shoutout to endersteve!