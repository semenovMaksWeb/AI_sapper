def levelSize():
    return 1

def sizeX():
    if levelSize() == 3:
        return 30
    if levelSize() == 2:
        return 15
    if levelSize() == 1:
        return 8
    
def sizeY():
    if levelSize() == 3:
        return 15
    if levelSize() == 2:
        return 15
    if levelSize() == 1:
        return 8