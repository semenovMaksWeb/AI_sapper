from mss import mss
from time import sleep
import parsingImg

def screenFull():
    sleep(3)
    with mss() as sct:
        sct.shot(mon=-1, output='img/monitor-1.png')

def start():
    # screenFull()
    parsingImg.parsingScreen()
    parsingImg.parsingCell(1,1)
    return