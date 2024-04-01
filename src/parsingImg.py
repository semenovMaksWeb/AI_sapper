from PIL import Image

import numpy
import sys
numpy.set_printoptions(threshold=sys.maxsize)

def _saveImgStatus():
    image_pole = Image.open("img/pole.png")
    image_status = image_pole.crop((246, 10, 288, 60))
    image_status.save('img/status.png', quality=95)
    

def _parsingScreen():
    image = Image.open("img/monitor-1.png")
    image_pole = image.crop((1015, 200, 1550, 810))
    image_pole.save('img/pole.png', quality=95)
 
#  0,0,255 это 1



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
    W_START = 7 + 32 * x
    H_START = 79 + 32 * y
    W_END = W_START + 32
    H_END = H_START + 32
    image_cell = image_pole.crop((W_START, H_START, W_END, H_END))
    image_cell.save('img/cell.png', quality = 95)
    
def cellPixelCheck():
    image_cell = Image.open('img/cell.png').convert('RGB')
    width, height = image_cell.size
    pixel_values = list(image_cell.getdata())
    pixel_values = numpy.array(pixel_values).reshape((width, height, 3))
    if pixel_values[10][17][0] == 0 and pixel_values[10][17][1] == 0 and pixel_values[10][17][2] == 255:
        return 1
    if pixel_values[10][17][0] == 47 and pixel_values[10][17][1] == 139 and pixel_values[10][17][2] == 47:
        return 2
    if pixel_values[10][17][0] == 238 and pixel_values[10][17][1] == 47 and pixel_values[10][17][2] == 47:
        return 3
    
def checkStatus():
    _parsingScreen()
    _saveImgStatus()
    return _checkStatusGames()