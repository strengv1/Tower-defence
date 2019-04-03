from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsEllipseItem, QGraphicsItemGroup
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QPointF

"""
Tower's position (tower.pos()) is the middle of the body
"""
class Tower(QGraphicsItemGroup):

    def __init__(self, type="basic"):
        super().__init__()
        if type == "basic":
            self.attackSpeed = 1
            self.range = 160
            self.setFlag(QGraphicsRectItem.ItemIsMovable)



            self.body = QGraphicsRectItem(0, 0, 30, 30)
            self.body.setBrush(QBrush(Qt.blue))
            self.body.setPos(-15,-15)

            self.pipe = QGraphicsRectItem(0, 0, 30, 10)
            self.pipe.setBrush(QBrush(Qt.darkBlue))
            self.pipe.setPos(0, -5)

            self.rangeIndicator = QGraphicsEllipseItem(0, 0, self.range, self.range)

            self.addToGroup(self.rangeIndicator)
            self.addToGroup(self.body)
            self.addToGroup(self.pipe)
            self.rangeIndicator.setPos(-self.range/2, -self.range/2)


def aim_at(tower, x, y):

    x_dir = x - tower.pos().x()
    y_dir = y - tower.pos().y()
#    print(x_dir, y_dir)