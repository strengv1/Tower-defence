from src import Block
from src import Peli
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt

class Map():

    def __init__(self, path = "map1.txt"):
        self.blocks = []
        try:
            file = open(path)
        except OSError:
            print("Could not open {}".format(path))
        else:
            idx = 0
            for line in file:
                self.blocks.append([])

                for c in line:
                    if c == ".":
                        self.blocks[idx].append(Block.Block())
                    elif c == "#":
                        self.blocks[idx].append(Block.Block(True, False, False))  # Block(is_path, is_checkPoint, is_spawn)
                    elif c == "-":
                        self.blocks[idx].append(Block.Block(False, True, False))
                    elif c == "s":
                        self.blocks[idx].append((Block.Block(False, False, True)))
                    else:
                        self.blocks[idx].append(None)
                idx += 1

        """for x in self.blocks:
            for y in x:
                if y == None:
                    pass
                else:
                    print(y.is_path)
            print("rivi")"""


def draw_map(scene, blocks):
    x = 0
    y = 0
    for horizontal in blocks:
        for b in horizontal:
            rect = QGraphicsRectItem(30*x, 30*y, 30, 30)

            if b == None:
                pass
            elif b.is_path:
                rect.setBrush(QBrush(Qt.lightGray))
            elif b.is_checkPoint:
                rect.setBrush(QBrush(Qt.darkGray))
            elif b.is_spawn:
                rect.setBrush(Qt.red)
            else:
                rect.setBrush(Qt.green)

            scene.addItem(rect)
            x += 1
        x = 0
        y += 1