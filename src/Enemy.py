from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from math import floor


class Enemy(QGraphicsEllipseItem):
    def __init__(self, spawn, width, height, type = "basic"):
        if type == "basic":
            self.radius = width/2 - width/7
            super().__init__(0, 0, self.radius*2, self.radius*2)

            self.hp = 10
            self.speed = width/20
            self.setBrush(Qt.blue)
            self.damage = 4
            self.prize = 12

        if type == "fast":
            self.radius = width/3 - 2
            super().__init__(0, 0, self.radius*2, self.radius*2)

            self.hp = 6
            self.speed = width/15
            self.setBrush(Qt.blue)
            self.damage = 2
            self.prize = 8

        self.direction = 1
        self.moveBy(0, width/2-self.radius)
        self.moveBy(spawn[0]*width, spawn[1]*height)
        self.in_a_checkpoint = False

        self.distance = 0
        self.hpBar = QGraphicsRectItem(0,-5,self.hp*2,3, self)
        self.hpBar.setBrush(Qt.red)



    def delete(self, scene, enemies):
        scene.removeItem(self)
        enemies.remove(self)

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
    Move in wanted direction
    """
    def move(self):
        self.distance += self.speed
        if self.direction == 1:  # Dir: right=1, down=2, left=3, up=4
            self.moveBy(self.speed, 0)
        elif self.direction == 2:
            self.moveBy(0, self.speed)
        elif self.direction == 3:
            self.moveBy(-self.speed, 0)
        elif self.direction == 4:
            self.moveBy(0, -self.speed)



    """
    Returns the block object that the enemy is on
    """
    def get_block(self, blocks, blockWidth, blockHeight):

        return blocks[floor(self.y() / blockHeight)][floor(self.x() / blockWidth)]


"""
Find out if the enemy is on a checkpoint or not, and act accordingly. Ugly way to do it but I couldn't find an easier way just yet.
"""
def check_for_checkpoint(enemy, block, map, blockWidth, blockHeight):
        if  not enemy.in_a_checkpoint and enemy.direction == 1 and block.is_checkPoint and block.center[0] - 1 < enemy.x() + enemy.radius:
            enemy.in_a_checkpoint = True
            # Found a checkPoint, left or right?
            dir = map.left_or_right(floor(enemy.x() / blockWidth), floor(enemy.y() / blockHeight), enemy.direction)
            enemy.turn(dir)
        elif not enemy.in_a_checkpoint and enemy.direction == 2 and block.is_checkPoint and block.center[1] - 1 < enemy.y() + enemy.radius:
            enemy.in_a_checkpoint = True
            dir = map.left_or_right(floor(enemy.x() / blockWidth), floor(enemy.y() / blockHeight), enemy.direction)
            enemy.turn(dir)
        elif not enemy.in_a_checkpoint and enemy.direction == 3 and block.is_checkPoint and block.center[0] + 2 > enemy.x() + enemy.radius:
            enemy.in_a_checkpoint = True
            dir = map.left_or_right(floor(enemy.x() / blockWidth), floor(enemy.y() / blockHeight), enemy.direction)
            enemy.turn(dir)
        elif not enemy.in_a_checkpoint and enemy.direction == 4 and block.is_checkPoint and block.center[1] + 1 > enemy.y() + enemy.radius:
            enemy.in_a_checkpoint = True
            dir = map.left_or_right(floor(enemy.x() / blockWidth), floor(enemy.y() / blockHeight), enemy.direction)
            enemy.turn(dir)

        if not map.blocks[floor(enemy.y() / blockHeight)][floor(enemy.x() / blockWidth)].is_checkPoint:
            enemy.in_a_checkpoint = False