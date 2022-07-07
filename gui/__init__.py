import sys

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
except ImportError:
    print("Unable to find module tkinter. Aborting.")
    sys.exit(1)

from .window import Window

app = QtWidgets.QApplication(sys.argv)

window = Window()

sys.exit(app.exec())
