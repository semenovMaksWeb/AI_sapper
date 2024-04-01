from PIL import Image
import numpy


def saveImgStatus():
    image_pole = Image.open("img/pole.jpg")
    image_status = image_pole.crop((246, 10, 288, 60))
    image_status.save('img/status.jpg', quality=95)
    

def parsingScreen():
    image = Image.open("img/monitor-1.png")
    image_pole = image.crop((1015, 200, 1550, 810))
    image_pole.save('img/pole.jpg', quality=95)
 
    
def checkStatusGames():
    image = Image.open('img/status.jpg').convert('RGB')
    width, height = image.size
    pixel_values = list(image.getdata())
    pixel_values = numpy.array(pixel_values).reshape((width, height, 3))
    if pixel_values[0][0][2] ==  222:
        return True
    if pixel_values[0][0][2] ==  218:
        return False

def parsingCell(x, y):
    image_pole = Image.open('img/pole.jpg').convert('RGB')
    W_START = 7 * x
    H_START = 79 * y
    image_cell = image_pole.crop((W_START, H_START, 40, 111))
    image_cell.save('img/cell.jpg', quality=95)