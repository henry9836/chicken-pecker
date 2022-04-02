#!/bin/python3
import pyautogui
import random
import cv2
from time import sleep
from pynput.mouse import Listener

setupStep = 0 #0,1 - Broswer, 2 - URL, 3 - Timer, 5-8 Colors
setupDone = False

BroswerTopLeft = [0, 0]
BroswerBottomRight = [1, 1]
BroswerMidPoint = [1, 1]
BroswerURL = [1, 1]

#Random
RANDOMNESS = 20

#Colors
Red = (255, 69, 0)
Orange = (255, 168, 0)
Yellow = (255, 214, 53)
Green = (0, 163, 104)
LightGreen = (126, 237, 86)
DarkBlue = (36, 80, 164)
Blue = (54, 144, 234)
LightBlue = (81, 233, 244)
Purple = (129, 30, 159)
Magenta = (180, 74, 192)
Pink = (255, 153, 170)
Brown = (156, 105, 38)
Black = (0, 0, 0)
Grey = (137, 141, 144)
LightGrey = (212, 215, 217)
White = (255, 255, 255)

#UI Points
TimerSection = [0, 0]
RedBox = [0, 0]
OrangeBox = [0, 0]
YellowBox = [0, 0]
GreenBox = [0, 0]
LightGreenBox = [0, 0]
DarkBlueBox = [0, 0]
BlueBox = [0, 0]
LightBlueBox = [0, 0]
PurpleBox = [0, 0]
MagentaBox = [0, 0]
PinkBox = [0, 0]
BrownBox = [0, 0]
BlackBox = [0, 0]
GreyBox = [0, 0]
LightGreyBox = [0, 0]
WhiteBox = [0, 0]
ConfirmPoint = [0, 0]
DismissPoint = [0, 0]

URL = "www.reddit.com/r/place/?cx=847&cy=694&px=36"

BANNER = s = '''\

    __  __ __  ____   __  __  _    ___  ____       ____   ___    __  __  _    ___  ____  
   /  ]|  |  ||    | /  ]|  |/ ]  /  _]|    \     |    \ /  _]  /  ]|  |/ ]  /  _]|    \ 
  /  / |  |  | |  | /  / |  ' /  /  [_ |  _  |    |  o  )  [_  /  / |  ' /  /  [_ |  D  )
 /  /  |  _  | |  |/  /  |    \ |    _]|  |  |    |   _/    _]/  /  |    \ |    _]|    / 
/   \_ |  |  | |  /   \_ |     \|   [_ |  |  |    |  | |   [_/   \_ |     \|   [_ |    \ 
\     ||  |  | |  \     ||  .  ||     ||  |  |    |  | |     \     ||  .  ||     ||  .  \\
 \____||__|__||____\____||__|\_||_____||__|__|    |__| |_____|\____||__|\_||_____||__|\_|
                                                                                         

'''

def on_move(x, y):
    pass

def on_click(x, y, button, pressed):
    global setupStep, setupDone, TimerSection, ConfirmPoint, DismissPoint, RANDOMNESS
    global RedBox, OrangeBox, YellowBox, GreenBox, LightGreenBox, DarkBlueBox, BlueBox, LightBlueBox, PurpleBox, MagentaBox, PinkBox, BrownBox, BlackBox, GreyBox, LightGreyBox, WhiteBox
    global Red, Orange, Yellow, Green, LightGreen, DarkBlue, Blue, LightBlue, Purple, Magenta, Pink, Brown, Black, Grey, LightGrey, White
    if pressed == True:
        if setupDone == False:
            if setupStep == 0:
                BroswerTopLeft[0] = x
                BroswerTopLeft[1] = y
                print("🐔 Click On The Bottom Right Capture Location (Broswer Content)")
            elif setupStep == 1:
                BroswerBottomRight[0] = x
                BroswerBottomRight[1] = y
                BroswerMidPoint[0] = BroswerTopLeft[0] + ((BroswerBottomRight[0] - BroswerTopLeft[0]) * 0.5)
                BroswerMidPoint[1] = BroswerTopLeft[1] + ((BroswerBottomRight[1] - BroswerTopLeft[1]) * 0.5)
                print("🐔 Click On The Address Bar (URL Textbox In Broswer)")
            elif setupStep == 2:
                BroswerURL[0] = x
                BroswerURL[1] = y
                print("🐔 Click On Something Else")
            elif setupStep == 3:
                displaySetup()
                sleep(1)
                goToWebSection()
                sleep(1)
            elif setupStep == 6:
                #Zoom till you find a good zoom
                sleep(1)
                findZoom()
                print("🐔 Click on white")
            elif setupStep == 7:
                WhiteBox[0] = x
                WhiteBox[1] = y
                print("🐔 Click on red")
            elif setupStep == 8:
                RedBox[0] = x
                RedBox[1] = y
                sleep(0.5)
                
                #Look for confirm dialog
                confirmBoxLoc = pyautogui.locateCenterOnScreen('./chicken-vision/confirm.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=True, confidence=0.9)
                if confirmBoxLoc != None:
                    print("🐔 Found Confirm Button!")
                    ConfirmPoint[0] = confirmBoxLoc.x
                    ConfirmPoint[1] = confirmBoxLoc.y

                    dismissBoxLoc = pyautogui.locateCenterOnScreen('./chicken-vision/dismiss.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=True, confidence=0.9)
                    if dismissBoxLoc != None:
                        print("🐔 Found Dismiss Button!")
                        DismissPoint[0] = dismissBoxLoc.x
                        DismissPoint[1] = dismissBoxLoc.y
                    else:
                        print("🐔 CLUCK Could not find Dismiss button!")
                        exit(0)
                    
                    #Search on Y of Red and above Y of confirmLoc
                    print("🐔 Finding Other Color Locations...")
                    colorbar = pyautogui.screenshot(region=(RedBox[0],RedBox[1], (BroswerBottomRight[0] - RedBox[0]), 2))
                    colorbar.save("./colorbar.png")
                    y = 0
                    for x in range(colorbar.width):
                        if (colorbar.getpixel((x, y)) == Orange and OrangeBox[0] == 0):
                            OrangeBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            OrangeBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Yellow and YellowBox[0] == 0):
                            YellowBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            YellowBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Green and GreenBox[0] == 0):
                            GreenBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            GreenBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == LightGreen and LightGreenBox[0] == 0):
                            LightGreenBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            LightGreenBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == DarkBlue and DarkBlueBox[0] == 0):
                            DarkBlueBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            DarkBlueBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Blue and BlueBox[0] == 0):
                            BlueBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            BlueBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == LightBlue and LightBlueBox[0] == 0):
                            LightBlueBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            LightBlueBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Purple and PurpleBox[0] == 0):
                            PurpleBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            PurpleBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Magenta and MagentaBox[0] == 0):
                            MagentaBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            MagentaBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Pink and PinkBox[0] == 0):
                            PinkBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            PinkBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Brown and BrownBox[0] == 0):
                            BrownBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            BrownBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Black and BlackBox[0] == 0):
                            BlackBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            BlackBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == Grey and GreyBox[0] == 0):
                            GreyBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            GreyBox[1] = RedBox[1] + y
                        elif (colorbar.getpixel((x, y)) == LightGrey and LightGreyBox[0] == 0):
                            LightGreyBox[0] = RedBox[0] + x + random.randint(0, RANDOMNESS)
                            LightGreyBox[1] = RedBox[1] + y
                            break
                    
                    #Test cursor positions
                    print("🐔 Values Assigned, testing...")
                    pyautogui.moveTo(ConfirmPoint[0], ConfirmPoint[1], duration = 0.2)
                    sleep(0.3)

                    pyautogui.moveTo(RedBox[0], RedBox[1], duration = 0.1)
                    clickAt(RedBox[0], RedBox[1], 0.2)
                    pyautogui.moveTo(OrangeBox[0], OrangeBox[1], duration = 0.1)
                    clickAt(OrangeBox[0], OrangeBox[1], 0.2)
                    pyautogui.moveTo(YellowBox[0], YellowBox[1], duration = 0.1)
                    clickAt(YellowBox[0], YellowBox[1], 0.2)
                    pyautogui.moveTo(GreenBox[0], GreenBox[1], duration = 0.1)
                    clickAt(GreenBox[0], GreenBox[1], 0.2)
                    pyautogui.moveTo(LightGreenBox[0], LightGreenBox[1], duration = 0.1)
                    clickAt(LightGreenBox[0], LightGreenBox[1], 0.2)
                    pyautogui.moveTo(DarkBlueBox[0], DarkBlueBox[1], duration = 0.1)
                    clickAt(DarkBlueBox[0], DarkBlueBox[1], 0.2)
                    pyautogui.moveTo(BlueBox[0], BlueBox[1], duration = 0.1)
                    clickAt(BlueBox[0], BlueBox[1], 0.2)
                    pyautogui.moveTo(LightBlueBox[0], LightBlueBox[1], duration = 0.1)
                    clickAt(LightBlueBox[0], LightBlueBox[1], 0.2)
                    pyautogui.moveTo(PurpleBox[0], PurpleBox[1], duration = 0.1)
                    clickAt(PurpleBox[0], PurpleBox[1], 0.2)
                    pyautogui.moveTo(MagentaBox[0], MagentaBox[1], duration = 0.1)
                    clickAt(MagentaBox[0], MagentaBox[1], 0.2)
                    pyautogui.moveTo(PinkBox[0], PinkBox[1], duration = 0.1)
                    clickAt(PinkBox[0], PinkBox[1], 0.2)
                    pyautogui.moveTo(BrownBox[0], BrownBox[1], duration = 0.1)
                    clickAt(BrownBox[0], BrownBox[1], 0.2)
                    pyautogui.moveTo(BlackBox[0], BlackBox[1], duration = 0.1)
                    clickAt(BlackBox[0], BlackBox[1], 0.2)
                    pyautogui.moveTo(GreyBox[0], GreyBox[1], duration = 0.1)
                    clickAt(GreyBox[0], GreyBox[1], 0.2)
                    pyautogui.moveTo(LightGreyBox[0], LightGreyBox[1], duration = 0.1)
                    clickAt(LightGreyBox[0], LightGreyBox[1], 0.2)
                    pyautogui.moveTo(WhiteBox[0], WhiteBox[1], duration = 0.1)
                    clickAt(WhiteBox[0], WhiteBox[1], 0.2)
                    pyautogui.moveTo(BroswerMidPoint[0], BroswerMidPoint[1], duration = 0.1)
                    sleep(0.2)

                    closeColor()
                    
                    print("🐔 Values Tested!")
                    #loadVisionTemplate()
                    compare()
                else:
                    print("🐔 CLUCK Could not find Confirm button!")
                    exit(0)
                setupDone = True
            setupStep += 1

def on_scroll(x, y, dx, dy):
    pass

def findZoom():
    print("🐔 Wait to find a good zoom level...")
    while True:
        pyautogui.scroll(-30)
        for i in range(6):
            sleep(0.3)
            pyautogui.scroll(1)
            if isGoodZoom() == True:
                print("🐔 Found Good Zoom Level! <" + str(i) + ">")
                return
            print("🐔 Bad Zoom <" + str(i) + ">")
        print("🐔 Bad Zooms Maybe Help Me A little")
    

def isGoodZoom():
    TargetLoc = pyautogui.locateOnScreen('./chicken-vision/ideal_reddit.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=False, confidence=0.4)
    if TargetLoc != None:
        return True
    TargetLoc = pyautogui.locateOnScreen('./chicken-vision/ideal_reddit_2.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=False, confidence=0.4)
    if TargetLoc != None:
        return True
    return False

def loadVisionTemplate():
    pyautogui.moveTo(BroswerTopLeft[0], BroswerTopLeft[1], duration = 0)
    print("🐔 Loading Template for Chicken-Vision...")
    TargetLoc = pyautogui.locateCenterOnScreen('./chicken-vision/ideal_reddit.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=False, confidence=0.4)
    if TargetLoc == None:
        targetLoc = pyautogui.locateCenterOnScreen('./chicken-vision/ideal_reddit_2.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=False, confidence=0.4)
    
    if targetLoc != None:
        print("🐔 CLUCK FOUND Image Match!")
        matchedTemplate = pyautogui.screenshot(region=(targetLoc.x, targetLoc.y, 512, 512))
        matchedTemplate.save("./matchedTemplate.png")
    else:
        print("🐔 CLUCK Could not find Template Image Match!")
        exit(0)

def compare():
    TargetTemplate = pyautogui.locateCenterOnScreen('./chicken-vision/ideal_reddit.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=False, confidence=0.4)
    if TargetTemplate == None:
        TargetTemplate = pyautogui.locateCenterOnScreen('./chicken-vision/ideal_reddit_2.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=False, confidence=0.4)
        target = cv2.imread('./chicken-vision/ideal_reddit_2.png')
    else:
        target = cv2.imread('./chicken-vision/ideal_reddit.png')

    if TargetTemplate == None:
        print("🐔 CLUCK Could not find Template Image Match!")
        exit()

    #Screenshot What We Have
    originX = TargetTemplate.x - (target.shape[1] * 0.5)
    originY = TargetTemplate.y - (target.shape[0] * 0.5)
    endX = target.shape[1]
    endY = target.shape[0]
    print(str(originX)+","+str(originY))
    screenshot = pyautogui.screenshot(region=(originX, originY, endX, endY))
    screenshot.save("./screenshot.png")
    print("🐔 DONE!")

def clickAt(x, y, delay):
    pyautogui.click(x, y)
    sleep(delay)

def closeColor():
    global DismissPoint
    dismissBoxLoc = pyautogui.locateOnScreen('./chicken-vision/dismiss.png', region=(BroswerTopLeft[0], BroswerTopLeft[1], BroswerBottomRight[0], BroswerBottomRight[1]), grayscale=True, confidence=0.9)
    if dismissBoxLoc != None:
        clickAt(DismissPoint[0], DismissPoint[1], 0.2)

def displaySetup():
    print("Setup Done.")
    print("-------------------------")
    print("| [URL] <- (" + str(BroswerURL[0]) + ", " + str(BroswerURL[1]) + ")")
    print("-------------------------")
    print("|(" + str(BroswerTopLeft[0]) + ", " + str(BroswerTopLeft[1]) + ")")
    print("|    (" + str(BroswerMidPoint[0]) + ", " + str(BroswerMidPoint[1]) + ")")
    print("|          (" + str(BroswerBottomRight[0]) + ", " + str(BroswerBottomRight[1]) + ")")
    print("-------------------------")

def goToWebSection():
    print("🐔 Flying To r/place")
    #pyautogui.moveTo(BroswerURL[0], BroswerURL[1], duration = 0.5)
    clickAt(BroswerURL[0], BroswerURL[1], 0.3)
    pyautogui.hotkey('ctrl', 'a')
    sleep(0.3)
    pyautogui.press('delete')
    sleep(0.3)
    pyautogui.write(URL)
    sleep(0.5)
    pyautogui.press("enter")
    print("🐔 Crash Bang")
    pyautogui.moveTo(BroswerMidPoint[0], BroswerMidPoint[1], duration = 3)
    sleep(5)
    clickAt(BroswerMidPoint[0], BroswerMidPoint[1], 0.2)
    sleep(1)
    clickAt(BroswerMidPoint[0], BroswerMidPoint[1], 0.2)
    sleep(1)

def TimerExists():
    global RedBox, BroswerBottomRight
    if (RedBox[0] == 0):
        RedBox[0] = BroswerTopLeft[0]
        RedBox[1] = BroswerTopLeft[1]

    if pyautogui.locateOnScreen('./chicken-vision/timer.png', region=(RedBox[0],RedBox[1] - 200,BroswerBottomRight[0],BroswerBottomRight[1]), grayscale=True, confidence=0.9) != None:
        return True
    return False

#Setup
print(BANNER)
print("🐔 Running Setup...")
print("🐔 Click On The Top Left Capture Location (Broswer Content)")

#Start listener
with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()