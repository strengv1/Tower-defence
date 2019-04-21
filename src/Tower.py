from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsEllipseItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QPointF
from math import degrees, acos, sin, cos, hypot, pi
from src import Projectile

class Tower(QGraphicsRectItem):

    def __init__(self, blockHeight, blockWidth, blocks, type = "basic"):
        super().__init__(0, 0, blockHeight, blockWidth)
        self.setFlag(self.ItemIsMovable, self.ItemIsSelectable)
        self.active = False
        self.timer = 1000
        self.blockWidth = blockWidth
        self.blockHeight = blockHeight
        self.type = type
        self.blocks = blocks

        if type == "basic":
            self.attackSpeed = 20
            self.range = 6*blockHeight - blockHeight/3
            self.damage = 2
            self.furthestTarget = (0, 0, None)  # (Enemy's distance, index in list)

            self.setBrush(QBrush(Qt.blue))
            self.setPos(self.range / 2 - blockWidth/2, self.range / 2 - blockHeight/2)

            self.pipe = QGraphicsRectItem(0, 0, blockHeight-blockHeight/3, blockHeight/3, self)
            self.pipe.setBrush(QBrush(Qt.darkBlue))
            self.pipe.setPos(blockHeight/2, blockHeight/3)
            self.pipe.setTransformOriginPoint(QPointF(0, blockHeight/6))

        if type == "fast":
            self.attackSpeed = 10
            self.range = 5 * blockHeight - blockHeight / 3
            self.damage = 1.2
            self.furthestTarget = (0, 0, None)  # (Enemy's distance, index in list)

            self.setBrush(QBrush(Qt.cyan))
            self.setPos(self.range / 2 - blockWidth / 2, self.range / 2 - blockHeight / 2)

            self.pipe = QGraphicsRectItem(0, 0, blockHeight - blockHeight / 3.5, blockHeight / 3, self)
            self.pipe.setBrush(QBrush(Qt.darkCyan))
            self.pipe.setPos(blockHeight / 2, blockHeight / 3)
            self.pipe.setTransformOriginPoint(QPointF(0, blockHeight / 6))

        if type == "sniper":
            self.attackSpeed = 60
            self.range = 40 * blockHeight
            self.damage = 5
            self.furthestTarget = (0, 0, None)  # (Enemy's distance, index in list)

            self.setBrush(QBrush(Qt.darkGreen))
            self.setPos(self.range / 2 - blockWidth / 2, self.range / 2 - blockHeight / 2)

            self.pipe = QGraphicsRectItem(0, 0, blockHeight, blockHeight / 5, self)
            self.pipe.setBrush(QBrush(Qt.darkGreen))
            self.pipe.setPos(blockWidth / 2, blockHeight / 2.5)
            self.pipe.setTransformOriginPoint(QPointF(0, blockHeight / 10))

        self.rangeIndicator = QGraphicsEllipseItem(-self.range/2+blockWidth/2, -self.range/2+blockHeight/2, self.range, self.range, self)


    def mouseMoveEvent(self, event):
        self.setPos(event.scenePos())


        self.pipe.setBrush(Qt.darkGray)
        self.setBrush(Qt.gray)
        self.setPos(QPointF(self.x() - self.x() % self.blockWidth, self.y() - self.y() % self.blockHeight))

    def mouseReleaseEvent(self, event):
        block = self.blocks[int(self.scenePos().y()/self.blockHeight)][int(self.scenePos().x()/self.blockWidth)]
        if not block.is_grass:
            print("Can't place turret here!")

        else:
            if self.type == "basic":
                self.setBrush(Qt.blue)
                self.pipe.setBrush(Qt.darkBlue)
            elif self.type == "sniper":
                self.setBrush(QBrush(Qt.darkGreen))
                self.pipe.setBrush(QBrush(Qt.darkGreen))
            elif self.type == "fast":
                self.setBrush(QBrush(Qt.cyan))
                self.pipe.setBrush(QBrush(Qt.darkCyan))

            self.setFlag(self.ItemIsMovable, False)
            self.rangeIndicator.hide()
            self.active = True

    def shoot(self, enemy, scene, projectiles):
        if self.timer >= self.attackSpeed:

            x_dir = cos(self.pipe.rotation()*pi/180)
            y_dir = sin(self.pipe.rotation()*pi/180)

            if self.type == "basic":
                proj = Projectile.Projectile((x_dir, y_dir), self.blockHeight/1.5, QPointF(self.x()+15, self.y()+15), enemy, self.damage, self.range)   #(dir, speed, pos, target, dmg, range)
                projectiles.append(proj)
                scene.addItem(proj)

            elif self.type == "sniper":
                self.furthestTarget[2].hp -= self.damage


            elif self.type == "fast":

                proj = Projectile.Projectile((x_dir, y_dir), self.blockHeight / 1.5,
                                             QPointF(self.x() + 15, self.y() + 15), enemy, self.damage,
                                             self.range)  # (dir, speed, pos, target, dmg, range)
                projectiles.append(proj)
                scene.addItem(proj)
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
