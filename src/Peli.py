import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QBrush, QColor, QPen, QPainter
from PyQt5.QtCore import QTimer, Qt, QRectF
import random


class Peli(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = "Main Menu"
        self.left = 300
        self.top = 150
        self.width = 640
        self.height = 700

        self.init_mainmenu()


    def init_mainmenu(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.scene = QGraphicsScene()

        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(10,10,620,680)

        play = QPushButton("Play")
        howto = QPushButton("How to play")
        exit = QPushButton("Exit")
        settings = QPushButton("Settings")
        #menulabel = QLabel(self)
        #menulabel.setPixmap(QtGui.QPixmap("data/menu_label"))
        #menulabel.setAlignment(QtCore.Qt.AlignHCenter)


        self.scene.addWidget(play)
        play.setGeometry(0,0, 100, 50)
        self.scene.addWidget(howto)
        howto.setGeometry(0, 100, 100, 50)
        self.scene.addWidget(exit)
        exit.setGeometry(0, 200, 100, 50)
        self.scene.addWidget(settings)
        settings.setGeometry(0, 300, 100, 50)

        play.setIcon(QtGui.QIcon("icon.png"))
        play.setIconSize(QtCore.QSize(30,30))


        self.show()

        play.clicked.connect(self.game_setup)
        exit.clicked.connect(self.close_game)
        howto.clicked.connect(self.how_to_play)


    def close_game(self):
        self.close()

    def how_to_play(self):
        print("Opettele pelaa")

    def game_setup(self):

        self.init_gamewindow()
        self.setup_sidebar()


#################################################
#Create enemy
        #self.enemy1 = QGraphicsEllipseItem(0, 0, 10, 10)
        #self.enemy1.setBrush(QBrush(Qt.red))

        #self.scene.addItem(self.enemy1)
################################################

        #self.timer = QTimer()
        #self.timer.timeout.connect(self.update)
        #self.timer.start(50)  # Milliseconds

   # def update(self):
    #    self.enemy1.moveBy(random.randint(-2,2),random.randint(-2,4))

    def init_gamewindow(self):
        self.scene.clear()
        self.setGeometry(300, 150, 1250, 800)
        self.setWindowTitle("Peli")
        self.view.setGeometry(10, 10, 1000, 780)

        self.setCentralWidget(QWidget())
        self.h_box = QHBoxLayout()
        self.sidebox = QVBoxLayout()

        self.centralWidget().setLayout(self.h_box)
        self.h_box.addWidget(self.view)
        self.h_box.addLayout(self.sidebox)


        #######################
        #   MAP CREATION




        #######################






    def setup_sidebar(self):
        self.randomButton = QPushButton("random button")
        self.sidebox.addWidget(self.randomButton)

        self.randomButton2 = QPushButton("random button 2")
        self.sidebox.addWidget(self.randomButton2)





