import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QBrush

import mainmenu

class Game():

    def __init__(self):

        asd = mainmenu.MainMenu()




        self.map = QMainWindow()
        self.map.setCentralWidget(QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.h_box = QHBoxLayout()  # Horizontal main layout
        self.sidebox = QVBoxLayout()


        self.map.centralWidget().setLayout(self.h_box)

        self.map.setGeometry(300, 150, 1200, 800)
        self.map.setWindowTitle('EZ4ENCE')
        self.map.show()

        # Add a scene for drawing 2d objects
        self.map.scene = QGraphicsScene()
        self.map.scene.setSceneRect(0, 0, 700, 700)

        # Add a view for showing the scene
        self.map.view = QGraphicsView(self.map.scene, self.map)
        self.map.view.adjustSize()
        self.map.view.show()
        self.h_box.addWidget(self.map.view)
        self.h_box.addLayout(self.sidebox)


# Random nappi sivuun
        self.map.randomButton = QPushButton("random button")
        self.sidebox.addWidget(self.map.randomButton)
# Random nappi2 sivuun
        self.map.randomButton2 = QPushButton("random button 2")
        self.sidebox.addWidget(self.map.randomButton2)

################################################
        #Create enemy
        self.enemy1 = QGraphicsEllipseItem(0, 0, 5, 5)
        self.enemy1.setBrush(QBrush(QColor(200,20,20)))
        self.map.scene.addItem(self.enemy1)
################################################

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Milliseconds

    def update(self):
        self.enemy1.moveBy(2.4, 0)



