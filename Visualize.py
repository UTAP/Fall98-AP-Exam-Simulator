from graphics import *
import numpy as np
import time

MAP_PATH  = './map.dat'
BLOCK_SYMBOL = 'b'
GRID_SIZE = 15
OUTPUT_FILE = './output.txt'

def tokenize(string):
    string = string.replace(' ', '')
    return string.split(',')

class Map:
    BLOCK_SIZE = GRID_SIZE

    def __init__(self, filePath):
        self.filePath = filePath
        self.map =[[]]
        self.win = ''
        self.read_map()
        self.map_objects = []
        self.size = 0

    def read_map(self):
        content = ''
        with open(self.filePath, 'r') as content_file:
            content = content_file.read()
        self.map = np.array([list(c) for c in content.split('\n')[1:]])

    def draw_map(self):
        mapShape = self.map.shape
        x = mapShape[0] * self.BLOCK_SIZE
        y = mapShape[1] * self.BLOCK_SIZE
        self.size = mapShape[1]
        self.win = GraphWin(self.filePath, x, y)

    def draw_blocks(self):
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j] == BLOCK_SYMBOL:
                    corner1 = Point(j*self.BLOCK_SIZE, i*self.BLOCK_SIZE)
                    corner2 = Point((j+1)*self.BLOCK_SIZE, (i+1)*self.BLOCK_SIZE)
                    blockRectangle = Rectangle(corner1, corner2)
                    blockRectangle.setFill('black')
                    blockRectangle.draw(self.win)

    def draw_child(self, child_str='2, Peaceful, 5, 5, 1, 21, 51, 31'):
        if child_str.find('#') != -1:
            return False
        tokens = tokenize(child_str)
        self.draw_circle(tokens)
        self.draw_id(tokens)
        return True

    def draw_circle(self, tokens):
        x, y = float(tokens[2]), float(self.size) - float(tokens[3])
        center = Point(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE)
        circle = Circle(center, float(tokens[4])* self.BLOCK_SIZE)
        if tokens[1] == 'Peaceful':
            circle.setFill('blue')
        elif tokens[1] == 'Coward':
            circle.setFill('green')
        elif tokens[1] == 'Angry':
            circle.setFill('red')
        circle.draw(self.win)
        self.map_objects.append(circle)

    def draw_id(self, tokens):
        x, y = float(tokens[2]), float(self.size) - float(tokens[3])
        center = Point(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE)
        id_text = Text(center, tokens[0])
        id_text.draw(self.win)
        self.map_objects.append(id_text)

    def clean(self):
        for o in self.map_objects:
            o.undraw()
        self.map_objects = []


map = Map(MAP_PATH)
map.draw_map()
map.draw_blocks()
input_txt = ''
with open(OUTPUT_FILE, 'r') as content_file:
    input_txt = content_file.read()
for i in input_txt.split('\n'):
    if not map.draw_child(i):
        time.sleep(0.1)
        map.clean()


input()

