import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer

import random
from configparser import ConfigParser

from src import Mapper, Enemy, Tower, Player, WaveManager

class Peli(QMainWindow):

    def __init__(self):
        super().__init__()
        self.parser = ConfigParser()
        self.parser.read('config.ini')

        self.title = self.parser.get("menu_window", "title")
        self.left = self.parser.getint("menu_window", "left")
        self.top = self.parser.getint("menu_window", "top")
        self.width = self.parser.getint("menu_window", "width")
        self.height = self.parser.getint("menu_window", "height")
        self.icon_path = self.parser.get("file_path", "icon")

        self.init_mainmenu()

    """
    Initialize main menu
    """
    def init_mainmenu(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.scene = QGraphicsScene()

        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, self.width-20, self.height-20)

        label = QLabel()
        label.setPixmap(QPixmap("data/menu_label.png"))
        play = QPushButton("Play")
        exit = QPushButton("Exit")
        settings = QPushButton("Settings")


        self.scene.addWidget(label)
        label.setGeometry(-190, -60, 480, 128)
        self.scene.addWidget(play)
        play.setGeometry(0,100, 100, 50)
        self.scene.addWidget(settings)
        settings.setGeometry(0, 200, 100, 50)
        self.scene.addWidget(exit)
        exit.setGeometry(0, 300, 100, 50)


        play.setIcon(QtGui.QIcon(self.icon_path))
        play.setIconSize(QtCore.QSize(30, 30))


        self.show()

        play.clicked.connect(self.game_setup)
        exit.clicked.connect(self.close_game)
        settings.clicked.connect(self.settings)
    """
    Define what the "Play" button does
    """
    def game_setup(self):

        self.waveManager = WaveManager.WaveManager()

        self.blockHeight = self.parser.getint("game", "block_height")
        self.blockWidth = self.parser.getint("game", "block_width")
        self.player = Player.Player()
        self.map = Mapper.Map(self.parser.get("file_path","map"))

        self.init_gamewindow()
        self.spawn = self.map.draw_map(self.gamescene, self.blockHeight, self.blockWidth)

        self.setup_sidebar()

        self.timer = QTimer()  # Start the timer
        self.timer.timeout.connect(self.update)
        self.timer.start(17)  # Frame-update-frequency in milliseconds (60fps => 1/60 = 0.01666, hence 17ms)

        self.towers = []
        self.enemies = []
        self.projectiles = []

    def settings(self):

        self.settingsScene = QGraphicsScene()
        self.settingsScene.setSceneRect(0, 0, 500, 300)
        self.view.setScene(self.settingsScene)
        self.setWindowTitle("Settings")

        map1 = QPushButton("Map1")
        map2 = QPushButton("Map2")
        back = QPushButton("Back")
        text = QGraphicsTextItem("Choose a map")
        text.setFont(QFont("helvetica"))
        map1.clicked.connect(self.map1_clicked)
        map2.clicked.connect(self.map2_clicked)
        back.clicked.connect(self.back_to_menu)

        self.settingsScene.addItem(text)
        text.setPos(180, -50)
        self.settingsScene.addWidget(map1)
        map1.setGeometry(200, 0, 100, 50)
        self.settingsScene.addWidget(map2)
        map2.setGeometry(200, 100, 100, 50)
        self.settingsScene.addWidget(back)
        back.setGeometry(200, 250, 100, 50)

    def map1_clicked(self):
        self.parser.set("file_path", "map", "map1.txt")
    def map2_clicked(self):
        self.parser.set("file_path", "map", "map2.txt")


    """
    Initializes the window after pressing "play" from mainmenu
    """
    def init_gamewindow(self):
        left = self.parser.getint("gamewindow", "left")
        top = self.parser.getint("gamewindow", "top")
        width = self.parser.getint("gamewindow", "width")
        height = self.parser.getint("gamewindow", "height")
        title = self.parser.get("gamewindow", "title")

        self.setGeometry(left, top, width, height)
        self.setWindowTitle(title)
        self.setCentralWidget(QWidget())

        self.gamescene = QGraphicsScene()
        self.gamescene.setSceneRect(0, 0, width-300, height-100)
        self.view.setScene(self.gamescene)
        self.view.setGeometry(10, 10, width-300, 0)


        self.moneyText = QGraphicsTextItem("Money: " + str(self.player.money) + "$")
        self.moneyText.setFont(QFont("helvetica"))
        self.moneyText.setPos(0, -30)
        self.gamescene.addItem(self.moneyText)

        self.hpText = QGraphicsTextItem("Health: " + str(self.player.health))
        self.hpText.setFont(QFont("helvetica"))
        self.hpText.setPos(200, -30)
        self.gamescene.addItem(self.hpText)

        self.waveText = QGraphicsTextItem("Wave: " + str(self.waveManager.wave))
        self.waveText.setFont(QFont("helvetica"))
        self.waveText.setPos(400, -30)
        self.gamescene.addItem(self.waveText)

        self.h_box = QHBoxLayout()
        self.sidebox = QVBoxLayout()
        self.centralWidget().setLayout(self.h_box)
        self.h_box.addWidget(self.view)
        self.h_box.addLayout(self.sidebox)

    """
    Sets up the sidebar, add all the buttons etc here
    """
    def setup_sidebar(self):
        basicprice = self.parser.getint("turretprices","basic")
        sniperprice = self.parser.getint("turretprices","sniper")
        fastprice = self.parser.getint("turretprices", "fast")

        self.basicTurret = QPushButton("Basic Turret ({}$)".format(basicprice))
        self.sidebox.addWidget(self.basicTurret)
        self.basicTurret.clicked.connect(self.basicTurret_clicked)

        self.sniperTurret = QPushButton("Sniper ({}$)".format(sniperprice))
        self.sidebox.addWidget(self.sniperTurret)
        self.sniperTurret.clicked.connect(self.sniperTurret_clicked)

        self.fastTurret = QPushButton("Fast turret ({}$)".format(fastprice))
        self.sidebox.addWidget(self.fastTurret)
        self.fastTurret.clicked.connect(self.fastTurret_clicked)


        self.nextWave = QPushButton("Next wave")
        self.sidebox.addWidget(self.nextWave)
        self.nextWave.clicked.connect(self.nextWaveClicked)

        self.backtomainmenu = QPushButton("Back to main menu")
        self.sidebox.addWidget(self.backtomainmenu)
        self.backtomainmenu.clicked.connect(self.back_to_menu)

    """
    Define what the exit button does
    """
    def close_game(self):
        self.close()

    def spawn_enemy(self, health):
        self.enemies.append(Enemy.Enemy(self.spawn, self.blockWidth, self.blockHeight, health))  # (spawn, width, height type="basic")
        self.gamescene.addItem(self.enemies[len(self.enemies) - 1])

    def spawn_fast_enemy(self, health):
        self.enemies.append(Enemy.Enemy(self.spawn, self.blockWidth, self.blockHeight, health, "fast"))
        self.gamescene.addItem(self.enemies[len(self.enemies) - 1])


    """
    Go back to main menu, not saving the game (yet)
    """
    def back_to_menu(self):
        self.close()
        self.init_mainmenu()

    def nextWaveClicked(self):
        self.waveManager.next_wave()
        self.waveText.setHtml("Wave: " + str(self.waveManager.wave))

    """
    Spawn a basicturret and set its original position (Outside the playable map)
    """
    def basicTurret_clicked(self):
        # Count basic turrets:
        count = 0
        for i in self.towers:
            if i.type == "basic":
                count += 1

        price = self.parser.getint("turretprices", "basic") + count*30
        if self.player.money >= price:

            self.player.money -= price
            self.moneyText.setHtml("Money: " + str(self.player.money) + "$")
            self.basicTurret.setText("Basic Turret ({}$)".format(price + 30))

            self.towers.append(Tower.Tower(self.blockHeight, self.blockWidth, self.map.blocks))
            self.towers[len(self.towers)-1].setPos(len(self.map.blocks[0]) * self.blockWidth,
                                                len(self.map.blocks) * self.blockHeight / 2)
            self.gamescene.addItem(self.towers[len(self.towers)-1])
        else:
            print("Not enough money!")

    def fastTurret_clicked(self):
        count = 0
        for i in self.towers:
            if i.type == "fast":
                count += 1

        price = self.parser.getint("turretprices", "fast") + count * 30
        if self.player.money >= price:

            self.player.money -= price
            self.moneyText.setHtml("Money: " + str(self.player.money) + "$")
            self.fastTurret.setText("Fast Turret ({}$)".format(price + 30))

            self.towers.append(Tower.Tower(self.blockHeight, self.blockWidth, self.map.blocks, "fast"))
            self.towers[len(self.towers) - 1].setPos(len(self.map.blocks[0]) * self.blockWidth,
                                                     len(self.map.blocks) * self.blockHeight / 2)
            self.gamescene.addItem(self.towers[len(self.towers) - 1])
        else:
            print("Not enough money!")

    def sniperTurret_clicked(self):
        count = 0
        for i in self.towers:
            if i.type == "sniper":
                count += 1

        price = self.parser.getint("turretprices", "sniper") + count*50

        if self.player.money >= price:

            self.player.money -= price
            self.moneyText.setHtml("Money: " + str(self.player.money) + "$")
            self.sniperTurret.setText("Sniper Turret ({}$)".format(price+50))

            self.towers.append(Tower.Tower(self.blockHeight, self.blockWidth, self.map.blocks, "sniper"))
            self.towers[len(self.towers)-1].setPos( len(self.map.blocks[0]) * self.blockWidth,
                                                    len(self.map.blocks) * self.blockHeight / 2)
            self.gamescene.addItem(self.towers[len(self.towers)-1])
        else:
            print("Not enough money!")


    """
    Call this every frame           
    """
    def update(self):
        if not self.player.am_i_alive():
            self.close()

        """
        Wavecontrol:
        a really messy way to make turns get harder, but I had to settle for this because I ran out of time.
        """
        randomizer = random.randint(0, 1)

        if self.waveManager.update():
            if self.waveManager.wave <= 2:
                self.spawn_enemy(10)
            elif self.waveManager.wave == 3:
                self.spawn_fast_enemy(6)
            elif self.waveManager.wave > 3 and self.waveManager.wave < 5 and randomizer == 0:
                self.spawn_fast_enemy(6)
            elif self.waveManager.wave > 3 and self.waveManager.wave < 5 and randomizer == 1:
                self.spawn_enemy(10)

            elif self.waveManager.wave >= 5 and self.waveManager.wave < 8 and randomizer == 0:
                self.spawn_fast_enemy(6+self.waveManager.wave/2.3)
            elif self.waveManager.wave >= 5 and self.waveManager.wave < 8 and randomizer == 1:
                self.spawn_enemy(10+self.waveManager.wave/2.3)

            elif self.waveManager.wave >= 8 and randomizer == 0:
                self.spawn_fast_enemy(6+self.waveManager.wave/1.5)
            elif self.waveManager.wave >= 8 and randomizer == 1:
                self.spawn_enemy(10+self.waveManager.wave/1.5)



        """
        Update the enemies
        """
        index = 0
        for enemy in self.enemies:
            if enemy.hp <= 0:
                enemy.delete(self.gamescene, self.enemies)
                self.player.money += enemy.prize
                self.moneyText.setHtml("Money: " + str(self.player.money) + "$")
                continue
            enemy.hpBar.setRect(0, -5, enemy.hp*2, 3)
            # Block the enemy is currently on
            block = enemy.get_block(self.map.blocks, self.blockWidth, self.blockHeight)

            if block == None:
                enemy.delete(self.gamescene, self.enemies)
                continue
            if block.is_goal:
                self.player.health -= enemy.damage
                self.hpText.setHtml("Health: " + str(self.player.health))

                enemy.delete(self.gamescene, self.enemies)

            # Check whether we are supposed to turn or not
            Enemy.check_for_checkpoint(enemy, block, self.map, self.blockWidth, self.blockHeight)
            enemy.move()
            # Determine who the towers want to aim at
            for q in self.towers:
                if q.active and enemy.collidesWithItem(q.rangeIndicator) and enemy.distance > q.furthestTarget[0]:
                    q.furthestTarget = (enemy.distance, index, enemy)
            index += 1

        # Take aim at the enemy we determined earlier, and reset it after. Also shoot
        for tow in self.towers:
            if tow.active and len(self.enemies) != 0 and tow.furthestTarget[0] != 0:
                tow.aim_at(self.enemies[tow.furthestTarget[1]].pos().x(), self.enemies[tow.furthestTarget[1]].pos().y())
                tow.shoot(tow.furthestTarget[2], self.gamescene, self.projectiles)
                tow.furthestTarget = (0, 0, None)

        for proj in self.projectiles:
            proj.move(self.projectiles, self.gamescene)
