import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import QTimer, Qt
from math import floor

from src import Mapper, Enemy

class Peli(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = "Main Menu"
        self.left = 300
        self.top = 150
        self.width = 640
        self.height = 700

        self.init_mainmenu()

    """
    Initialize main menu
    """
    def init_mainmenu(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("data/icon.png"))
        self.scene = QGraphicsScene()

        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(10,10,620,680)

        play = QPushButton("Play")
        howto = QPushButton("How to play")
        exit = QPushButton("Exit")
        settings = QPushButton("Settings")

        self.scene.addWidget(play)
        play.setGeometry(0,100, 100, 50)
        self.scene.addWidget(howto)
        howto.setGeometry(0, 200, 100, 50)
        self.scene.addWidget(exit)
        exit.setGeometry(0, 300, 100, 50)
        self.scene.addWidget(settings)
        settings.setGeometry(0, 400, 100, 50)

        play.setIcon(QtGui.QIcon("data/icon.png"))
        play.setIconSize(QtCore.QSize(30, 30))


        self.show()

        play.clicked.connect(self.game_setup)
        exit.clicked.connect(self.close_game)
        howto.clicked.connect(self.how_to_play)

    """
    Define what the exit button does
    """
    def close_game(self):
        self.close()


    """
    Define what the "How to play" button does
    """
    def how_to_play(self):
        print("Opettele pelaa")


    """
    Define what the "Play" button does
    """
    def game_setup(self):

        self.blockHeight = 30
        self.blockWidth = 30
        self.map = Mapper.Map()

        self.init_gamewindow()
        spawn = Mapper.draw_map(self.gamescene, self.map.blocks, self.blockHeight, self.blockWidth)


        self.setup_sidebar()

        self.timer = QTimer()                                   #  Start the timer
        self.timer.timeout.connect(self.update)
        self.timer.start(20)                                    # Frame-update-frequency in milliseconds



        #Create enemies!
        self.enemies = []
        self.enemycount = 6
        for i in range(self.enemycount):
            self.enemies.append(Enemy.Enemy(10, 1+0.3*i, QBrush(Qt.blue), spawn))    # (hp=10, speed=2, brush=QBrush(Qt.red), spawn,radius, direction)
            self.gamescene.addItem(self.enemies[i])



    """
    Initializes the window after pressing "play" from mainmenu
    """
    def init_gamewindow(self):

        #self.scene.clear()                          #Possible segfault after scene.clear()
        self.gamescene = QGraphicsScene()            #Attempt at fixing: Just add a new scene instead of using the last one
        self.view.setScene(self.gamescene)
        self.view.setGeometry(10, 10, 1000, 780)

        self.setGeometry(300, 150, 1250, 800)
        self.setWindowTitle("Peli")
        self.setCentralWidget(QWidget())

        self.h_box = QHBoxLayout()
        self.sidebox = QVBoxLayout()
        self.centralWidget().setLayout(self.h_box)
        self.h_box.addWidget(self.view)
        self.h_box.addLayout(self.sidebox)


    """
    Sets up the sidebar, add all the buttons etc here
    """
    def setup_sidebar(self):

        self.randomButton = QPushButton("random button")
        self.sidebox.addWidget(self.randomButton)

        self.randomButton2 = QPushButton("random button 2")
        self.sidebox.addWidget(self.randomButton2)



    """
    Call this every frame           (int(self.enemies[0].pos().x()/self.blockWidth), int(self.enemies[0].pos().y()/self.blockHeight)), position of an enemy
    """
    def update(self):
        for i in range(self.enemycount):

            """
            Find out if the enemy is on a checkpoint or not, and act accordingly. Ugly way to do it but I couldn't find an easier way just yet.
            """
            block = self.enemies[i].get_block(self.map.blocks, self.blockWidth, self.blockHeight)   #Block the enemy is on currently

            """
            Do whatever when the enemy gets to the end (NoneType-block for now)
            """
            if block == None:
                self.gamescene.removeItem(self.enemies[i])
                self.enemies.pop(i)
                self.enemycount -= 1
                continue

            enemy = self.enemies[i]                                                                 #Current enemy



            if enemy.direction == 1 and block.is_checkPoint and block.center[0]-1 < enemy.x()+enemy.radius and not enemy.in_a_checkpoint:
                enemy.in_a_checkpoint = True
                # Found a checkPoint, left or right?
                dir = self.map.left_or_right(floor(enemy.x() / self.blockWidth), floor(enemy.y() / self.blockHeight), enemy.direction)
                enemy.turn(dir)
            elif enemy.direction == 2 and block.is_checkPoint and block.center[1]-1 < enemy.y()+enemy.radius and not enemy.in_a_checkpoint:
                enemy.in_a_checkpoint = True
                dir = self.map.left_or_right(floor(enemy.x() / self.blockWidth), floor(enemy.y() / self.blockHeight), enemy.direction)
                enemy.turn(dir)
            elif enemy.direction == 3 and block.is_checkPoint and block.center[0]+1 > enemy.x()+enemy.radius and not enemy.in_a_checkpoint:
                enemy.in_a_checkpoint = True
                dir = self.map.left_or_right(floor(enemy.x() / self.blockWidth), floor(enemy.y() / self.blockHeight), enemy.direction)
                enemy.turn(dir)
            elif enemy.direction == 4 and block.is_checkPoint and block.center[1]+1 > enemy.y() + enemy.radius and not enemy.in_a_checkpoint:
                enemy.in_a_checkpoint = True
                dir = self.map.left_or_right(floor(enemy.x() / self.blockWidth), floor(enemy.y() / self.blockHeight), enemy.direction)
                enemy.turn(dir)

            if not self.map.blocks[floor(enemy.y() / self.blockHeight)][floor(enemy.x() / self.blockWidth)].is_checkPoint:
                enemy.in_a_checkpoint = False

            """
            Move in wanted direction
            """
            if enemy.direction == 1:                  #Dir: right=1, down=2, left=3, up=4
                enemy.moveBy(enemy.speed, 0)
            elif enemy.direction == 2:
                enemy.moveBy(0, enemy.speed)
            elif enemy.direction == 3:
                enemy.moveBy(-enemy.speed, 0)
            elif enemy.direction == 4:
                enemy.moveBy(0, -enemy.speed)



