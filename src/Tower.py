from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsEllipseItem
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt


class Tower():

    def __init__(self, type="basic"):

        if type == "basic":
            self.attackSpeed = 1
            self.range = 80

            self.body = QGraphicsRectItem(0,0,30,30)
            self.body.setBrush(QBrush(Qt.blue))
            self.body.setFlag(QGraphicsRectItem.ItemIsMovable)


            self.rangeIndicator = QGraphicsEllipseItem(0, 0, self.range, self.range)
            self.rangeIndicator.setPen(QPen(1))