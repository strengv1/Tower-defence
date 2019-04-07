import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import QTimer, Qt
from math import floor

from src import Mapper, Enemy, Tower, Player

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
    Define what "spawn an enemy" button does in the sidebar
    """
    def spawn_enemy(self):

        self.enemycount += 1

        self.enemies.append(Enemy.Enemy(self.spawn))  # (spawn, type="basic")
        self.gamescene.addItem(self.enemies[self.enemycount-1])

    def spawn_fast_enemy(self):
        self.enemycount += 1
        self.enemies.append(Enemy.Enemy(self.spawn, "fast"))
        self.gamescene.addItem(self.enemies[self.enemycount-1])
    """
    Go back to main menu, not saving the game (yet)
    """
    def back_to_menu(self):
        self.close()
        self.init_mainmenu()


    """
    Spawn a basicturret and set its original position (Outside the playable map)
    """
    def basicTurret_clicked(self):

        if self.player.money >= 200:

            self.player.money -= 200
            self.towers.append(Tower.Tower())
            self.towers[self.towercount].moveBy(len(self.map.blocks[0]) * self.blockWidth,
                                                len(self.map.blocks) * self.blockHeight / 2)
            self.gamescene.addItem(self.towers[self.towercount])
            self.towercount += 1
        else:
            print("NOT ENOUGH CASH u poor mf")

    """
    Define what the "Play" button does
    """
    def game_setup(self):

        self.blockHeight = 30
        self.blockWidth = 30
        self.player = Player.Player()
        self.map = Mapper.Map()

        self.init_gamewindow()
        self.spawn = Mapper.draw_map(self.gamescene, self.map.blocks, self.blockHeight, self.blockWidth)


        self.setup_sidebar()

        self.timer = QTimer()                                   #  Start the timer
        self.timer.timeout.connect(self.update)
        self.timer.start(50)                                    # Frame-update-frequency in milliseconds

        #Towers!
        self.towers = []
        self.towercount = 0
        #Create enemies!
        self.enemies = []
        self.enemycount = 1
        for i in range(self.enemycount):
            self.enemies.append(Enemy.Enemy(self.spawn))    # (spawn, type="basic")
            self.gamescene.addItem(self.enemies[i])



    """
    Initializes the window after pressing "play" from mainmenu
    """
    def init_gamewindow(self):

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

        self.basicTurret = QPushButton("Basic Turret (200$)")
        self.sidebox.addWidget(self.basicTurret)
        self.basicTurret.clicked.connect(self.basicTurret_clicked)


        self.spawnEnemy = QPushButton("spawn an enemy")
        self.sidebox.addWidget(self.spawnEnemy)
        self.spawnEnemy.clicked.connect(self.spawn_enemy)

        self.spawnFastEnemy = QPushButton("Spawn a fast enemy")
        self.sidebox.addWidget(self.spawnFastEnemy)
        self.spawnFastEnemy.clicked.connect(self.spawn_fast_enemy)

        self.backtomainmenu = QPushButton("Back to main menu")
        self.sidebox.addWidget(self.backtomainmenu)
        self.backtomainmenu.clicked.connect(self.back_to_menu)



    """
    Call this every frame           
    """
    def update(self):
        """
        Move the enemies
        """
        index = 0
        for enemy in self.enemies:
            # Block the enemy is currently on
            block = enemy.get_block(self.map.blocks, self.blockWidth, self.blockHeight)

            #Do whatever when the enemy gets to the end (NoneType-block for now)
            if block == None:
                self.gamescene.removeItem(enemy)
                self.enemies.remove(enemy)
                self.enemycount -= 1
                continue

            # Check whether we are supposed to turn or not
            Enemy.check_for_checkpoint(enemy, block, self.map, self.blockWidth, self.blockHeight)
            enemy.move()
            # Determine who the towers want to aim at
            for q in self.towers:
                if enemy.collidesWithItem(q.rangeIndicator) and enemy.distance > q.furthestTarget[0]:
                    q.furthestTarget = (enemy.distance, index)


            index += 1

        # Take aim at the enemy we determined earlier, and reset it after
        for tow in self.towers:
            if tow.furthestTarget is not (0, 0):
                tow.aim_at(self.enemies[tow.furthestTarget[1]].pos().x(), self.enemies[tow.furthestTarget[1]].pos().y())
                tow.furthestTarget = (0, 0)

