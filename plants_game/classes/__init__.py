import random

# используем во всех классах в качестве определения позиции
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# используем tilemap, вытаскиваем картинку по позиции x,y (пиксели)
class Imageposition:
    def __init__(self, x, y):
        self.pos = Position(x, y)