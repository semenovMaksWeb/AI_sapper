def levelSize():
    return 3

def sizeX():
    if levelSize() == 3:
        return 30
        pass
    if levelSize() == 2:
        return 15
    
def sizeY():
    if levelSize() == 3:
        return 15
        pass
    if levelSize() == 2:
        return 15