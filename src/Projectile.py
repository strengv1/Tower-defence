from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush


class Projectile(QGraphicsEllipseItem):

    def __init__(self, dir, speed, pos, target, dmg, range):
        super().__init__(0, 0, 5, 5)
        self.setBrush(QBrush(Qt.red))

        self.dir = dir
        self.speed = speed
        self.setPos(pos)
        self.target = target
        self.damage = dmg
        self.range = range
        self.distDone = 0
    def move(self, projectiles, scene):

        if self.collidesWithItem(self.target) or self.distDone > self.range:
            projectiles.remove(self)
            scene.removeItem(self)
            self.target.hp -= self.damage
        else:
            self.distDone += self.speed
            self.moveBy(self.dir[0]*self.speed, self.dir[1]*self.speed)
