from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from math import floor


"""
Enemy's position (enemy.pos()) is top left corner. To get the correct pos, call (enemy.pos().x() + radius, enemy.pos().y() + radius)
"""

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


"""
Find out if the enemy is on a checkpoint or not, and act accordingly. Ugly way to do it but I couldn't find an easier way just yet.
"""
def check_for_checkpoint(enemy, block, map, blockWidth, blockHeight):
        if enemy.direction == 1 and block.is_checkPoint and block.center[0] - 1 < enemy.x() + enemy.radius and not enemy.in_a_checkpoint:
            enemy.in_a_checkpoint = True
            # Found a checkPoint, left or right?
            dir = map.left_or_right(floor(enemy.x() / blockWidth), floor(enemy.y() / blockHeight), enemy.direction)
            enemy.turn(dir)
        elif enemy.direction == 2 and block.is_checkPoint and block.center[1] - 1 < enemy.y() + enemy.radius and not enemy.in_a_checkpoint:
            enemy.in_a_checkpoint = True
            dir = map.left_or_right(floor(enemy.x() / blockWidth), floor(enemy.y() / blockHeight), enemy.direction)
            enemy.turn(dir)
        elif enemy.direction == 3 and block.is_checkPoint and block.center[0] + 1 > enemy.x() + enemy.radius and not enemy.in_a_checkpoint:
            enemy.in_a_checkpoint = True
            dir = map.left_or_right(floor(enemy.x() / blockWidth), floor(enemy.y() / blockHeight), enemy.direction)
            enemy.turn(dir)
        elif enemy.direction == 4 and block.is_checkPoint and block.center[1] + 1 > enemy.y() + enemy.radius and not enemy.in_a_checkpoint:
            enemy.in_a_checkpoint = True
            dir = map.left_or_right(floor(enemy.x() / blockWidth), floor(enemy.y() / blockHeight), enemy.direction)
            enemy.turn(dir)

        if not map.blocks[floor(enemy.y() / blockHeight)][floor(enemy.x() / blockWidth)].is_checkPoint:
            enemy.in_a_checkpoint = False