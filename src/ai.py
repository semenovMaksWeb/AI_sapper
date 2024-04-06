from mss import mss
from time import sleep
import pyautogui

import parsingImg
import env

# todo попробовать сделать объектом с ключом `${x}-${y}` для более быстрого поиска по x, y
schema = []
schemaFlag = []

checkScreen = 1

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

def saveOldScreen():
    global checkScreen
    checkScreen = checkScreen + 1
    parsingImg.fileAddOldScreen(checkScreen)

def start():
    clickCell(0, 0, 3)
    screenFull()
    parsingImg.checkStatus()
    while(True):
        checkStatusAI()
        createSchema()
        checkSchema()

def clickRandom():
        for elem in schema:
            if elem.get("val") == 0 and not checkFlagElem(elem.get("x"), elem.get("y")):
                print("click random", elem.get("x"), elem.get("y"))
                clickCell(elem.get("x"), elem.get("y"))
                return


def checkStatusAI():
    sleep(0.4)
    print("сделал скрин checkStatusAI")
    saveOldScreen()
    screenFull()
    sleep(0.4)
    parsingImg.checkStatus()
    sleep(0.4)

def checkSchema ():
    print("checkSchema", schema)
    for elem in schema:
        if elem.get("val") != 0 and elem.get("val") != None:
            checkClick = []
            checkElemClickAll(elem, checkClick)
            # todo изучать что цифра равна len(checkClick) и что флагов не больше чем цифра ибо нельзя ставить 2 флага когда цифра 1
            if  len(checkClick) == 1:
                schemaFlag.append(checkClick[0])
                clickCell(checkClick[0].get("x"), checkClick[0].get("y"), 1, "right")
                fakeAllClickCheck(checkClick[0])
                checkStatusAI()
                return
    clickRandom()
    checkStatusAI()

def fakeAllClickCheck(elem):
    # todo возможно стоит изучать куда имеет смысл нажимать
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
            not checkFlagElem(x, y)
        ):
            clickCell(x, y)
            checkStatusAI()
            createSchema()
            
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
    schema.clear()
    for y in range(env.sizeY()):
        for x in range(env.sizeX()):
            if checkFlagElem(x,y):
                schema.append({"x": x, "y": y, "val": None})
            else:
                parsingImg.parsingCell(y, x)
                val = parsingImg.cellPixelCheck()
                schema.append({"x": x, "y": y, "val": val})

def clickPosition(x,y, type="left"):
    print("click", x, " ", y,  " ", type)
    pyautogui.moveTo(x, y, duration = 0.25)
    if type == "left":
        pyautogui.leftClick()
    else:
        pyautogui.rightClick()
    sleep(0.4)
    
def clickCell(x,y, time = 0.4, type = "left"):
    sleep(time)  
    clickPosition(START_CELL_W + SIZE * x, START_CELL_H + SIZE * y, type)