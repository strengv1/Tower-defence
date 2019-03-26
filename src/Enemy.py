from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


class Enemy(QGraphicsEllipseItem):
    def __init__(self, new_param, *args, **kwargs):
        QGraphicsEllipseItem.__init__(self, *args, **kwargs)

