from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsEllipseItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QPointF
from math import degrees, acos, sin, cos, hypot, pi
from src import Projectile

class Tower(QGraphicsRectItem):

    def __init__(self, type = "basic"):
        super().__init__(0, 0, 30, 30)
        self.setFlag(self.ItemIsMovable, self.ItemIsSelectable)
        self.active = False
        self.timer = 1000
        if type == "basic":
            self.attackSpeed = 20
            self.range = 200
            self.damage = 2
            self.furthestTarget = (0, 0, None)  # (Enemy's distance, index in list)

            self.setBrush(QBrush(Qt.blue))
            self.setPos(self.range / 2 - 15, self.range / 2 - 15)

            self.pipe = QGraphicsRectItem(0, 0, 20, 10, self)
            self.pipe.setBrush(QBrush(Qt.darkBlue))
            self.pipe.setPos(15, 10)
            self.pipe.setTransformOriginPoint(QPointF(0, 5))

            self.projectiles = []

            self.rangeIndicator = QGraphicsEllipseItem(-self.range/2+15, -self.range/2+15, self.range, self.range, self)


    def mouseMoveEvent(self, event):
        self.setPos(event.scenePos())
        self.pipe.setBrush(Qt.darkGray)
        self.setBrush(Qt.gray)
        self.setPos(QPointF(self.x() - self.x() % 30, self.y() - self.y() % 30))

    def mouseReleaseEvent(self, event):
        self.setBrush(Qt.blue)
        self.pipe.setBrush(Qt.darkBlue)
        self.setFlag(self.ItemIsMovable, False)
        self.rangeIndicator.hide()
        self.active = True

    def shoot(self, enemy, scene, projectiles):
        if self.timer >= self.attackSpeed:

            x_dir = cos(self.pipe.rotation()*pi/180)
            y_dir = sin(self.pipe.rotation()*pi/180)


            proj = Projectile.Projectile((x_dir, y_dir), 20, QPointF(self.x()+15, self.y()+15), enemy, self.damage, self.range)   #(dir, speed, pos, target, dmg, range)
            projectiles.append(proj)
            scene.addItem(proj)

            #enemy.hp -= self.damage
            self.timer = 0

        elif self.timer <= self.attackSpeed:
            self.timer += 1
        else:
            pass

    """
    Turn the pipe at the first enemy in range
    parameters: (the tower we are turning, enemy's x position, enemy's y position).
    """
    def aim_at(self, x, y):
        x_dir = x - self.scenePos().x()-5
        y_dir = y - self.scenePos().y()-5

        # Calculate the angle from the tower to enemy.
        angle = degrees(acos(x_dir / hypot(x_dir, y_dir)))

        if y_dir > 0:
            self.pipe.setRotation(angle)
        else:
            self.pipe.setRotation(360-angle)
