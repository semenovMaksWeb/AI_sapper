from mss import mss
from time import sleep
import pyautogui

import parsingImg
import env

schema = {}
schemaFlag = {}

# checkScreen = 1

if env.levelSize() == 2:
    START_CELL_W = 1040
    START_CELL_H = 300
if env.levelSize() == 1:
    START_CELL_W = 1160
    START_CELL_H = 290
SIZE = 32

# получение ключа объекта schema по [y,x]
def getKeySchemaElement(y, x):
    return str(y) + "-" + str(x)

# сохранение объекта schema по [y,x]
def saveElementSchema(y, x, elem, name):
    key = getKeySchemaElement(y, x)
    if name == "schemaFlag":
        schemaFlag[key] = elem
    if name == "schema":
        schema[key] = elem
    
# скрин всего экрана
def screenFull():
    with mss() as sct:
        sct.shot(mon=-1, output='img/monitor-1.png')

# # функция отладки сохранение файлов скринов отдельно
# def saveOldScreen():
#     global checkScreen
#     checkScreen = checkScreen + 1
#     parsingImg.fileAddOldScreen(checkScreen)

# Старт программы
def start():
    clickCell(0, 0, 3)
    screenFull()
    parsingImg.checkStatus()
    while(True):
        checkStatusAI()
        createSchema()
        checkSchema()

# Рандомный клик когда программа не знает что делать
def clickRandom():
        for key, elem in schema.items():
            if elem.get("val") == 0 and not checkFlagElem(elem.get("x"), elem.get("y")):
                print("click random", elem.get("x"), elem.get("y"))
                clickCell(elem.get("x"), elem.get("y"))
                return

# Проверка ситуации все ли ок
def checkStatusAI():
    sleep(0.4)
    print("сделал скрин checkStatusAI")
    screenFull()
    # saveOldScreen()
    sleep(0.4)
    parsingImg.checkStatus()
    sleep(0.4)

# анализ schema для понимания что можно сделать
def checkSchema ():
    for key, elem in schema.items():
        if elem.get("val") != 0 and elem.get("val") != None:
            checkClick = []
            checkElemClickAll(elem, checkClick)
            if len(checkClick) == 1 and checkFlagAllCells(checkClick[0]):
                flagAddCells(elem)
                return
            if len(checkClick) == elem.get("val") - getCounterFlagAllCells(checkClick):
                for elemClick in checkClick:
                    flagAddCells(elemClick)
                return                   
    clickRandom()
    checkStatusAI()

# Поставка флага для 1 ячейки
def flagAddCells(elem):
    saveElementSchema(elem.get("x"), elem.get("y"), elem, "schemaFlag")
    saveElementSchema(elem.get("x"), elem.get("y"), {"x": elem.get("x"), "y": elem.get("y"), "val": None}, "schema")
    clickCell(elem.get("x"), elem.get("y"), 1, "right")
    fakeAllClickCheck(elem)
    checkStatusAI()

# клики во все безопастные места для открытие соседних клеток
def fakeAllClickCheck(elem):
    indexsCells = generatorIndexsCells(elem)
    for indexCells in indexsCells:
        if fakeClick(indexCells.get("x"), indexCells.get("y"), elem):
            return



def getCounterFlagAllCells(elem):
    counter = 0
    indexsCells = generatorIndexsCells(elem)
    for indexCells in indexsCells:
        if getSchemaElement(schemaFlag, indexCells.get("x"), indexCells.get("y")):
            counter = counter + 1
    return counter


def checkFlagAllCells(elem):
        val = elem.get("val")
        counter = getCounterFlagAllCells(elem)
        if counter != val:
            return True
        fakeClick(elem.get("x"), elem.get("y"), None)
        return False 
        
# проверка что есть хотя бы 1 соседний элемент который раскроет при клике
def checkAllCells0(elem):
    indexsCells = generatorIndexsCells(elem)
    for indexCell in indexsCells:
        elemCheck = getSchemaElement(schema, indexCell.get("x"), indexCell.get("y"))
        
        if(checkElementClick(elemCheck)):
            return True
        
    return False

# создание объект x,y с соседними ячейками
def generatorIndexsCells(elem):
    return [
        {"x":elem.get("x") + 1, "y":elem.get("y") },
        {"x":elem.get("x") - 1, "y":elem.get("y") },
        {"x": elem.get("x"), "y": elem.get("y") - 1 },
        {"x": elem.get("x") + 1, "y": elem.get("y") - 1 },
        {"x": elem.get("x") - 1, "y": elem.get("y") - 1 },
        {"x": elem.get("x"), "y": elem.get("y") + 1 },
        {"x": elem.get("x") + 1, "y": elem.get("y") + 1 },
        {"x": elem.get("x") - 1, "y": elem.get("y") + 1 },
        
    ]

# клик в конкретную безопастную ячейку места для открытие соседних клеток
def fakeClick(x, y, elemRecurs):
        elemCheck = getSchemaElement(schema, x, y)
        if(
            elemCheck and 
            (elemCheck.get("val") != 0 and elemCheck.get("val") != None ) and 
            not checkFlagElem(x, y) and
            checkAllCells0(elemCheck)
        ):
            # TODO нажимает все подряд надо как то разобраться
            clickCell(x, y)
            checkStatusAI()
            createSchema()
            if elemRecurs:
                fakeAllClickCheck(elemRecurs)
            return True

# изучение соседних клеток для понимание определение флажков
def checkElemClickAll(elem, checkClick):
    indexsCells = generatorIndexsCells(elem)
    for indexCells in indexsCells:
        blockCheckElemClick(indexCells.get("x"), indexCells.get("y"), checkClick)
 

# возвращает наличия флага по x,y
def checkFlagElem(x,y):
    return getSchemaElement(schemaFlag, x,y)

# проверка что на эту ячейку можно поставить флаг
def blockCheckElemClick(x,y, checkClick):
    elemCheck = getSchemaElement(schema, x, y)
    if elemCheck and checkElementClick(elemCheck) and not checkFlagElem(x,y):
        checkClick.append(elemCheck)

# проверка что это неизвестная ячейка
def checkElementClick(elem):
    if elem.get("val") == 0:
        return True
    return False

# получение объекта schema по x,y
def getSchemaElement(schema, x ,y):
    return schema.get(getKeySchemaElement(y,x))

# создание схемы по скрину
def createSchema():
    for y in range(env.sizeY()):
        for x in range(env.sizeX()):
            if checkFlagElem(x,y):
                saveElementSchema(x, y, {"x": x, "y": y, "val": None}, "schema")
            else:
                parsingImg.parsingCell(y, x)
                val = parsingImg.cellPixelCheck()
                saveElementSchema(x,y,{"x": x, "y": y, "val": val}, "schema")

# клик по ячейки
def clickPosition(x,y, type="left"):
    print("click", x, " ", y,  " ", type)
    pyautogui.moveTo(x, y, duration = 0.25)
    if type == "left":
        pyautogui.leftClick()
    else:
        pyautogui.rightClick()
    sleep(0.4)

# клик по ячейки учитывая сдвиг до игрового поля
def clickCell(x,y, time = 0.4, type = "left"):
    sleep(time)  
    clickPosition(START_CELL_W + SIZE * x, START_CELL_H + SIZE * y, type)