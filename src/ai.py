from mss import mss
from time import sleep
import pyautogui

import parsingImg
import env

schema = []
schemaFlag = []

if env.levelSize() == 2:
    START_CELL_W = 1040
    START_CELL_H = 300
if env.levelSize() == 1:
    START_CELL_W = 1160
    START_CELL_H = 290
SIZE = 32

def screenFull():
    with mss() as sct:
        sct.shot(mon=-1, output='img/monitor-1.png')

def start():
    clickCell(0, 0, 3)
    screenFull()
    parsingImg.checkStatus()
    while(True):
        schema.clear()
        createSchema()
        checkSchema()

def clickRandom():
        for elem in schema:
            if elem.get("val") == 0 and not checkFlagElem(elem.get("x"), elem.get("y")):
                clickCell(elem.get("x"), elem.get("y"))


def checkStatusAI():
    screenFull()
    parsingImg.checkStatus()
    sleep(1)

def checkSchema ():
    for elem in schema:
        if elem.get("val") != 0 and elem.get("val") != None:
            checkClick = []
            checkElemClickAll(elem, checkClick)
            if  len(checkClick) == 1:
                schemaFlag.append(checkClick[0])
                clickCell(checkClick[0].get("x"), checkClick[0].get("y"), 1, "right")
                fakeAllClickCheck(checkClick[0])
                checkStatusAI()
                return
                
    clickRandom()
    checkStatusAI()

def fakeAllClickCheck(elem):
    fakeClick(elem.get("x") + 1, elem.get("y"))
    fakeClick(elem.get("x") - 1, elem.get("y")) 
    
    fakeClick(elem.get("x"), elem.get("y") - 1)
    fakeClick(elem.get("x") + 1, elem.get("y") - 1)  
    fakeClick(elem.get("x") - 1, elem.get("y") - 1)
    
    fakeClick(elem.get("x"), elem.get("y") + 1)
    fakeClick(elem.get("x") + 1, elem.get("y") + 1)
    fakeClick(elem.get("x") - 1, elem.get("y") + 1)

def fakeClick(x, y):
        elemCheck = getSchemaElement(schema, x, y)
        if(
            elemCheck and 
            (elemCheck.get("val") != 0 and elemCheck.get("val") != None ) and 
            not checkFlagElem(x,y)
        ):
            clickCell(x, y)
            
def checkElemClickAll(elem, checkClick):
    blockCheckElemClick(elem.get("x") + 1, elem.get("y"), checkClick)
    blockCheckElemClick(elem.get("x") - 1, elem.get("y"), checkClick)
    
    blockCheckElemClick(elem.get("x"), elem.get("y") - 1, checkClick)
    blockCheckElemClick(elem.get("x") + 1, elem.get("y") - 1, checkClick)  
    blockCheckElemClick(elem.get("x") - 1, elem.get("y") - 1, checkClick)
    
    blockCheckElemClick(elem.get("x"), elem.get("y") + 1, checkClick)
    blockCheckElemClick(elem.get("x") + 1, elem.get("y") + 1, checkClick)  
    blockCheckElemClick(elem.get("x") - 1, elem.get("y") + 1, checkClick)

def checkFlagElem(x,y):
    if getSchemaElement(schemaFlag, x,y):
        return True
    return False

def blockCheckElemClick(x,y, checkClick):
    elemCheck = getSchemaElement(schema, x, y)
    if elemCheck and checkElementClick(elemCheck) and not checkFlagElem(x,y):
        checkClick.append(elemCheck)

def checkElementClick(elem):
    if elem.get("val") == 0:
        return True
    return False

def getSchemaElement(schema, x ,y):
    for elem in schema:
        if elem.get("x") == x and elem.get("y") ==  y:
            return elem

def createSchema():
    for y in range(env.sizeY()):
        for x in range(env.sizeX()):
            if checkFlagElem(x,y):
                schema.append({"x": x, "y": y, "val": None})
            else:
                parsingImg.parsingCell(y, x)
                val = parsingImg.cellPixelCheck()
                schema.append({"x": x, "y": y, "val": val})

def clickPosition(x,y, type="left"):
    pyautogui.moveTo(x, y, duration = 0.25)
    if type == "left":
        pyautogui.leftClick()
    else:
        pyautogui.rightClick()
    sleep(1)
    
def clickCell(x,y, time = 1, type = "left"):
    sleep(time)  
    clickPosition(START_CELL_W + SIZE * x, START_CELL_H + SIZE * y, type)