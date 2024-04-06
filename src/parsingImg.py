from PIL import Image
import numpy
import sys

import env

numpy.set_printoptions(threshold=sys.maxsize)

def _saveImgStatus():
    image_pole = Image.open("img/pole.png")
    if env.levelSize() == 1:
        image_status = image_pole.crop((125, 10, 176, 60))
    if env.levelSize() == 2:
        image_status = image_pole.crop((246, 10, 288, 60))
    
    image_status.save('img/status.png', quality=95)
    

def _parsingScreen():
    image = Image.open("img/monitor-1.png")
    position = None
    if env.levelSize() == 1:
        position = (1130, 200, 1425, 551)
        pass
        
    if env.levelSize() == 2:
        position = (1015, 200, 1550, 810)
        
    if env.levelSize() == 3:
        position = (765, 200, 1795, 810)
    
    image_pole = image.crop(position)
    image_pole.save('img/pole.png', quality=95)

def _checkStatusGames():
    image_status_ok = Image.open('img/status_ok.png').convert('RGB')
    image_status = Image.open('img/status.png').convert('RGB')
    pixel_values_image_status = list(image_status.getdata())
    pixel_values_image_status_ok = list(image_status_ok.getdata())
    if not numpy.array_equal(pixel_values_image_status,pixel_values_image_status_ok):
        print("выход!")
        sys.exit(1)

def parsingCell(y, x):
    image_pole = Image.open('img/pole.png').convert('RGB')
    if env.levelSize() == 1:
        W_START = 20 + 32 * x
        H_START = 80 + 32 * y
        W_END = W_START + 32
        H_END = H_START + 32
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
    image_cell = Image.open("img/cell.png").convert('RGB')
    pixel_values = list(image_cell.getdata())
    # Цвета значении полей
    returnList1 = list((0,0,255))
    returnList2 = list((47,139,47))
    returnList3 = list((255,0,0))
    returnList4 = list((47, 47, 139))
    returnList0 = list((255,255,255))
    
    for i in pixel_values:
        if i[0] == returnList0[0] and i[1] == returnList0[1] and i[2] == returnList0[2]:
            return 0
        if i[0] == returnList1[0] and i[1] == returnList1[1] and i[2] == returnList1[2]:
            return 1
        if i[0] == returnList2[0] and i[1] == returnList2[1] and i[2] == returnList2[2]:
            return 2
        if i[0] == returnList3[0] and i[1] == returnList3[1] and i[2] == returnList3[2]:
            return 3
        if i[0] == returnList4[0] and i[1] == returnList4[1] and i[2] == returnList4[2]:
            return 4
    
def checkStatus():
    _parsingScreen()
    _saveImgStatus()
    return _checkStatusGames()