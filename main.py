import sys
from PyQt5.QtWidgets import QApplication
import Peli


def main():

    global app
    app = QApplication(sys.argv)
    #ex = mainmenu.MainMenu()
    #ex = Game.Game()
    peli = Peli.Peli()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
