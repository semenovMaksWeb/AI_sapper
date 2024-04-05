from mss import mss
from time import sleep
import pyautogui

import parsingImg

import env

schema = []
START_CELL_W = 1040
START_CELL_H = 300
SIZE = 32

def screenFull():
    with mss() as sct:
        sct.shot(mon=-1, output='img/monitor-1.png')

def start():
    clickCell(0, 0, 3)
    createSchema()
    print(schema)
    return

def createSchema():
    for y in range(env.sizeY()):
        for x in range(env.sizeX()):
            parsingImg.parsingCell(y, x)
            val = parsingImg.cellPixelCheck()
            schema.append({"x": x, "y": y, "val": val})
    return

def clickPosition(x,y):
    pyautogui.moveTo(x, y, duration = 0.25)
    pyautogui.click()
    sleep(1)
    
def clickCell(x,y, time = 1):
    sleep(time)  
    clickPosition(START_CELL_W + SIZE * x, START_CELL_H + SIZE * y)
    screenFull()
    parsingImg.checkStatus()
    createSchema()