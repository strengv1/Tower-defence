import sys
from PyQt5.QtWidgets import QApplication, QWidget


def window():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle('Ikkuna')


    w.show()
    sys.exit(app.exec())

window()



