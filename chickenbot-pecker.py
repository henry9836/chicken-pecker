#!/bin/python3
import pyautogui
import random
import cv2
from time import sleep
from pynput.mouse import Listener

BANNER = s = '''\

    __  __ __  ____   __  __  _    ___  ____       ____   ___    __  __  _    ___  ____  
   /  ]|  |  ||    | /  ]|  |/ ]  /  _]|    \     |    \ /  _]  /  ]|  |/ ]  /  _]|    \ 
  /  / |  |  | |  | /  / |  ' /  /  [_ |  _  |    |  o  )  [_  /  / |  ' /  /  [_ |  D  )
 /  /  |  _  | |  |/  /  |    \ |    _]|  |  |    |   _/    _]/  /  |    \ |    _]|    / 
/   \_ |  |  | |  /   \_ |     \|   [_ |  |  |    |  | |   [_/   \_ |     \|   [_ |    \ 
\     ||  |  | |  \     ||  .  ||     ||  |  |    |  | |     \     ||  .  ||     ||  .  \\
 \____||__|__||____\____||__|\_||_____||__|__|    |__| |_____|\____||__|\_||_____||__|\_|
                                                                                         

'''

def clickAt(x, y, delay):
    pyautogui.click(x, y)
    sleep(delay)

def loop():
    while True:
        ErrorMessage = pyautogui.locateCenterOnScreen('./chicken-vision/opps.png', grayscale=True, confidence=0.9)
        if ErrorMessage != None:
            print("CLUCK I FOUND A BAD CHICKEN!")
            x = ErrorMessage.x
            y = ErrorMessage.y
            pyautogui.moveTo(x, y, duration = 3)
            clickAt(x, y, 0.2)
            pyautogui.hotkey('ctrl', 'r')
            while True:
                print("Waiting on Chicken...")
                PlaceImage = pyautogui.locateCenterOnScreen('./chicken-vision/place.png', region=(x-100, y-75, 200, 75), grayscale=True, confidence=0.9)
                if PlaceImage != None:
                    clickAt(PlaceImage.x, PlaceImage.y, 0.2)
                    print("Chicken Fixed Returning To Watch...")
                    break
                
                Timer = pyautogui.locateCenterOnScreen('./chicken-vision/timer.png', region=(x-100, y-75, 200, 75), grayscale=True, confidence=0.9)
                if Timer != None:
                    clickAt(Timer.x, Timer.y, 0.2)
                    print("Chicken Fixed Returning To Watch...")
                    break
                sleep(1)
        sleep(1)

print(BANNER)
print("Mother Hen Is Monitoring For Issues...")
while True:
    try:
        loop()
    except:
        print("CLUCK! Something went wrong, waking mother hen...")
        sleep(1)
