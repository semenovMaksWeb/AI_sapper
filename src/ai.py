from mss import mss
from time import sleep
import pyautogui

import parsingImg
import env

schema = {}
schemaFlag = {}

checkScreen = 1

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
def saveElementFlag(y, x, elem, name):
    key = getKeySchemaElement(y, x)
    if name == "schemaFlag":
        schemaFlag[key] = elem
    if name == "schema":
        schema[key] = elem
    
# скрин всего экрана
def screenFull():
    with mss() as sct:
        sct.shot(mon=-1, output='img/monitor-1.png')

# функция отладки сохранение файлов скринов отдельно
def saveOldScreen():
    global checkScreen
    checkScreen = checkScreen + 1
    parsingImg.fileAddOldScreen(checkScreen)

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
    saveOldScreen()
    screenFull()
    sleep(0.4)
    parsingImg.checkStatus()
    sleep(0.4)

# анализ schema для понимания что можно сделать
def checkSchema ():
    print("checkSchema", schema)
    for key, elem in schema.items():
        if elem.get("val") != 0 and elem.get("val") != None:
            checkClick = []
            checkElemClickAll(elem, checkClick)
            # TODO изучать что цифра равна len(checkClick) и что флагов не больше чем цифра ибо нельзя ставить 2 флага когда цифра 1
            if  len(checkClick) == 1:
                saveElementFlag(checkClick[0].get("x"), checkClick[0].get("x"), checkClick[0], "schemaFlag")
                clickCell(checkClick[0].get("x"), checkClick[0].get("y"), 1, "right")
                fakeAllClickCheck(checkClick[0])
                checkStatusAI()
                return
    clickRandom()
    checkStatusAI()

# клики во все безопастные места для открытие соседних клеток
def fakeAllClickCheck(elem):
    # TODO возможно стоит изучать куда имеет смысл нажимать
    fakeClick(elem.get("x") + 1, elem.get("y"))
    fakeClick(elem.get("x") - 1, elem.get("y")) 
    
    fakeClick(elem.get("x"), elem.get("y") - 1)
    fakeClick(elem.get("x") + 1, elem.get("y") - 1)  
    fakeClick(elem.get("x") - 1, elem.get("y") - 1)
    
    fakeClick(elem.get("x"), elem.get("y") + 1)
    fakeClick(elem.get("x") + 1, elem.get("y") + 1)
    fakeClick(elem.get("x") - 1, elem.get("y") + 1)

# клик в конкретную  безопастную ячейку места  для открытие соседних клеток
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
            # вызывать наверх функцию return fakeAllClickCheck и делать рекурсию 
            # может быть ситуация что вверх нельзя нажать а после открытие соседней клетки в вверху появится число которое является кликабельным сделать тут или в checkSchema нужно смотреть

 # изучение соседних клеток для понимание определение флажков
def checkElemClickAll(elem, checkClick):
    blockCheckElemClick(elem.get("x") + 1, elem.get("y"), checkClick)
    blockCheckElemClick(elem.get("x") - 1, elem.get("y"), checkClick)
    
    blockCheckElemClick(elem.get("x"), elem.get("y") - 1, checkClick)
    blockCheckElemClick(elem.get("x") + 1, elem.get("y") - 1, checkClick)  
    blockCheckElemClick(elem.get("x") - 1, elem.get("y") - 1, checkClick)
    
    blockCheckElemClick(elem.get("x"), elem.get("y") + 1, checkClick)
    blockCheckElemClick(elem.get("x") + 1, elem.get("y") + 1, checkClick)  
    blockCheckElemClick(elem.get("x") - 1, elem.get("y") + 1, checkClick)
 # изучение соседних клеток для понимание определение флажков

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
                saveElementFlag(x, y, {"x": x, "y": y, "val": None}, "schema")
            else:
                parsingImg.parsingCell(y, x)
                val = parsingImg.cellPixelCheck()
                saveElementFlag(x,y,{"x": x, "y": y, "val": val}, "schema")

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