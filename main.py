import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Main menu"
        self.left = 300
        self.top = 200
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

        play = QPushButton("Play")
        howto = QPushButton("How to play")
        exit = QPushButton("Exit")
        settings = QPushButton("Settings")
        menulabel = QLabel("Main menu")
        menulabel.setAlignment(QtCore.Qt.AlignHCenter)

        ylareuna = QHBoxLayout()
        ylareuna.addStretch()
        ylareuna.addWidget(settings)

        v_box = QVBoxLayout()

        v_box.addLayout(ylareuna)
        v_box.addWidget(menulabel)
        v_box.addStretch()
        v_box.addWidget(play)
        v_box.addStretch()
        v_box.addWidget(howto)
        v_box.addStretch()
        v_box.addWidget(exit)




        self.setLayout(v_box)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



