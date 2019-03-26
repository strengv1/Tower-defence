import sys
from PyQt5.QtWidgets import QApplication
from src import Peli


def main():

    global app
    app = QApplication(sys.argv)
    peli = Peli.Peli()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
