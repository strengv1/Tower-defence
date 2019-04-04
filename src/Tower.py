from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsEllipseItem, QGraphicsItemGroup
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QPointF
from math import degrees, acos, hypot



class Tower(QGraphicsItemGroup):

    def __init__(self, type="basic"):
        super().__init__()
        if type == "basic":
            self.attackSpeed = 1
            self.range = 160
            self.setFlag(QGraphicsRectItem.ItemIsMovable)


            self.body = QGraphicsRectItem(0, 0, 30, 30)
            self.body.setBrush(QBrush(Qt.blue))
            self.body.setPos(self.range/2-15, self.range/2-15)

            self.target = None


            self.pipe = QGraphicsRectItem(0, 0, 30, 10)
            self.pipe.setBrush(QBrush(Qt.darkBlue))
            self.pipe.setPos(self.range/2, self.range/2-5)
            self.pipe.setTransformOriginPoint(QPointF(0, 5))

            self.rangeIndicator = QGraphicsEllipseItem(0, 0, self.range, self.range)

            self.addToGroup(self.rangeIndicator)
            self.addToGroup(self.body)
            self.addToGroup(self.pipe)

"""
Turn the pipe at the first enemy in range
parameters: (the tower we are turning, enemy's x position, enemy's y position).
"""
def aim_at(tower, x, y):
    print(x, y)
    x_dir = x - tower.body.scenePos().x()-5
    y_dir = y - tower.body.scenePos().y()-5

    # Calculate the angle from the tower to enemy.
    angle = degrees(acos(x_dir / hypot(x_dir, y_dir)))

    if y_dir > 0:
        tower.pipe.setRotation(angle)
    else:
        tower.pipe.setRotation(360-angle)


