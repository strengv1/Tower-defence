import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
import Game


class MainMenu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setCentralWidget(QWidget())
        self.v_box = QVBoxLayout()
        self.h_box = QHBoxLayout()

        self.centralWidget().setLayout(self.v_box)
        self.init_window()


    def init_window(self):
        self.title = "Tower defence"
        self.left = 300
        self.top = 150
        self.width = 640
        self.height = 480

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        play = QPushButton("Play")
        howto = QPushButton("How to play")
        exit = QPushButton("Exit")
        settings = QPushButton("Settings")

        play.clicked.connect(self.open_game)
        exit.clicked.connect(self.close_game)
        howto.clicked.connect(self.how_to_play)

        menulabel = QLabel(self)
        menulabel.setPixmap(QtGui.QPixmap("data/menu_label"))
        menulabel.setAlignment(QtCore.Qt.AlignHCenter)

        self.h_box.addStretch()
        self.h_box.addWidget(settings)
        self.v_box.addLayout(self.h_box)
        self.v_box.addWidget(menulabel)
        self.v_box.addStretch()
        self.v_box.addWidget(play)
        self.v_box.addStretch()
        self.v_box.addWidget(howto)
        self.v_box.addStretch()
        self.v_box.addWidget(exit)

        self.show()


    def close_game(self):
        self.close()

    def how_to_play(self):
        print("Opettele pelaa")

    def open_game(self):
        ex = Game.Game()


