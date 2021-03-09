import pyautogui as pya
import solver
import time
import glob
import os
import numpy as np
import cv2
import shutil


path = os.getcwd()
path1 = path + r'/temp'
path2  = path +r'/level'
try:
    shutil.rmtree(path1)
except:
    pass
try:
    os.mkdir('temp')
except:
    pass
try:
    os.mkdir('level')
except:
    pass

bluestacks = pya.locateCenterOnScreen('static/bluestacks.jpg', confidence=.9)
print(bluestacks)
pya.click(bluestacks)
time.sleep(3)
full = pya.locateCenterOnScreen('static/full.jpg', confidence=.8)
pya.click(full)
time.sleep(15)
mojeGry = pya.locateCenterOnScreen('static/mojegry.jpg', confidence=.8)
print(mojeGry)
if mojeGry:
    pya.click(mojeGry)
    time.sleep(2)
game = pya.locateCenterOnScreen('static/watersort.jpg', confidence=.5)
print(game)
if game:
    pya.click(game)
    time.sleep(6)

record = pya.locateCenterOnScreen('static/record.jpg', confidence=.8)

for m in range(4):
    pya.click(record)
    time.sleep(4.5)
    for k in range(10):

        screenshoot = pya.screenshot()
        screenshoot = cv2.cvtColor(np.array(screenshoot), cv2.COLOR_RGB2BGR)
        cv2.imwrite("level/screen.jpg", screenshoot)

        moves, boxes_position = solver.game_loop("level/screen.jpg")
        print(f'Steps to solve level: {len(moves)}')
        print(moves)
        for i,j in moves:
            pya.click(boxes_position[i])
            time.sleep(0.3)
            pya.click(boxes_position[j])
            pya.sleep(2.5)
        
        next_level = pya.locateCenterOnScreen('static/next.jpg', confidence=.7)
        pya.click(next_level)
        time.sleep(3)
        x_location = pya.locateCenterOnScreen('static/x.jpg', confidence=.7)
        if x_location:
            pya.click(x_location)
            time.sleep(2)
        x_location = pya.locateCenterOnScreen('static/x.jpg', confidence=.7)
        if x_location:
            pya.click(x_location)
            time.sleep(2)
    pya.click(record)
    time.sleep(2)
            