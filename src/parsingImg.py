from PIL import Image
import numpy
import sys
import collections

import env

numpy.set_printoptions(threshold=sys.maxsize)

def _saveImgStatus():
    image_pole = Image.open("img/pole.png")
    image_status = image_pole.crop((246, 10, 288, 60))
    image_status.save('img/status.png', quality=95)
    

def _parsingScreen():
    image = Image.open("img/monitor-1.png")
    position = None
    if env.levelSize() == 1:
        # position = (1015, 200, 1550, 810)
        pass
        
    if env.levelSize() == 2:
        position = (1015, 200, 1550, 810)
        
    if env.levelSize() == 3:
        position = (765, 200, 1795, 810)
    
    image_pole = image.crop(position)
    image_pole.save('img/pole.png', quality=95)

def _checkStatusGames():
    image = Image.open('img/status.png').convert('RGB')
    width, height = image.size
    pixel_values = list(image.getdata())
    pixel_values = numpy.array(pixel_values).reshape((width, height, 3))
    if pixel_values[0][0][2] ==  222:
        return True
    if pixel_values[0][0][2] ==  218:
        return False

def parsingCell(y, x):
    image_pole = Image.open('img/pole.png').convert('RGB')
    if env.levelSize() == 2:
        W_START = 17 + 32 * x
        H_START = 80 + 32 * y
        W_END = W_START + 28
        H_END = H_START + 28
    if env.levelSize() == 3:
        W_START = 20 + 32 * x
        H_START = 80 + 32 * y
        W_END = W_START + 32
        H_END = H_START + 32
    image_cell = image_pole.crop((W_START, H_START, W_END, H_END))
    image_cell.save('img/cell.png', quality = 95)
    
def cellPixelCheck():
    image_cell = Image.open('img/cell.png').convert('RGB')
    pixel_values = list(image_cell.getdata())
    # Цвета значении полей
    returnList1 = list((0,0,225))
    returnList2 = list((47,139,47))
    returnList3 = list((0,0,123))
    returnList4 = list((47, 47, 139))

    for i in pixel_values:
        if collections.Counter(i) == collections.Counter(returnList1):
            return 1
        if collections.Counter(i) == collections.Counter(returnList2):
            return 2
        if collections.Counter(i) == collections.Counter(returnList3):
            return 3
        if collections.Counter(i) == collections.Counter(returnList4):
            return 4
    
def checkStatus():
    _parsingScreen()
    _saveImgStatus()
    return _checkStatusGames()