from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


class Enemy(QGraphicsEllipseItem):
    def __init__(self, hp=10, speed=2, brush=QBrush(Qt.red)):
        super().__init__(0, 0, 20, 20)
        self.setBrush(brush)

        self.hp = hp
        self.speed = speed
