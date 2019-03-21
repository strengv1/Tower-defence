import sys
from PyQt5.QtWidgets import QApplication
import mainmenu
import Game

def main():

    global app
    app = QApplication(sys.argv)
    ex = Game.Game()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
