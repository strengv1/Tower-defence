from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt
from math import floor

class Enemy(QGraphicsEllipseItem):
    def __init__(self, hp=10, speed=2, brush=QBrush(Qt.red), spawn=(0,0), radius=10, dir = 1):
        super().__init__(0, 0, radius*2, radius*2)


        self.direction = dir        #right=1, down=2, left=3, up=4
        self.setBrush(brush)
        self.moveBy(0, 5)
        self.moveBy(spawn[0]*30, spawn[1]*30)
        self.hp = hp
        self.speed = speed
        self.radius = radius
        self.in_a_checkpoint = False

    """
    Kuinka tehdä käännös, dir on string "left" tai "right"
    """
    def turn(self, dir):
        if dir == "left":
            if self.direction == 1:
                self.direction = 4
            else:
                self.direction = self.direction-1
        if dir == "right":
            if self.direction == 4:
                self.direction = 1
            else:
                self.direction = self.direction+1


    """
    Returns the block object that the enemy is on
    """
    def get_block(self, blocks, blockWidth, blockHeight):

        return blocks[floor(self.y() / blockHeight)][floor(self.x() / blockWidth)]

