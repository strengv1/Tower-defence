from src import Block
from src import Peli
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt

class Map():

    def __init__(self, path = "map1.txt"):
        self.blocks = []            #Alustetaan Blockien lista
        try:
            file = open(path)
        except OSError:
            print("Could not open {}".format(path))
        else:
            idx = 0
            for line in file:
                self.blocks.append([])          #Lisätään Block-listaan "sub_lista", jotka vastaavat vaakarivejä kartalla.

                for c in line:                  #Parsitaan tiedosto siten, että "." on tavallinen ruohonpala, "#" on polku, "-" on checkpoint ja "s" on spawn.
                                                #Rivinvaihtojen tilalle listaan menee "None", joka myöhemmissä vaiheissa täytyy muistaa skipata.
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

    """
    Function used for determining whether the enemy should turn left or right at a checkpoint.
    """
    def left_or_right(self, x, y, dir):
        if dir == 1:
            if self.blocks[y-1][x].is_path:
                return "left"
            else:
                return "right"

        elif dir == 2:
            if self.blocks[y][x+1].is_path:
                return "left"
            else:
                return "right"

        elif dir == 3:
            if self.blocks[y+1][x].is_path:
                return "left"
            else:
                return "right"

        elif dir == 4:
            if self.blocks[y][x-1].is_path:
                return "left"
            else:
                return "right"

"""
Kartan piirto, ottaa sisäänsä scenen johon halutaan palikat piirrettäväksi, sekä listan joka sisältää palikat.
Palauttaa spawnin sijainnin
"""
def draw_map(scene, blocks, height, width):
    x = 0
    y = 0
    blockheight = height
    blockwidth = width
    for horizontal in blocks:
        for b in horizontal:
            rect = QGraphicsRectItem(blockwidth*x, blockheight*y, blockwidth, blockheight)
            if b != None:
                b.x = x
                b.y = y
                b.center = (blockwidth*x + blockwidth/2, blockheight*y + blockheight/2)
                if b.is_path:
                    rect.setBrush(QBrush(Qt.lightGray))
                elif b.is_checkPoint:
                    rect.setBrush(QBrush(Qt.darkGray))

                elif b.is_spawn:
                    rect.setBrush(Qt.red)
                    spawn = (x, y)
                else:
                    rect.setBrush(Qt.green)

            if b != None:
                scene.addItem(rect)
            x += 1
        x = 0

        y += 1
    return spawn





