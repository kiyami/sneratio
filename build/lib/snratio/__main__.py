from snratio.gui.main_gui import MainWindow
from PySide2 import QtWidgets
import sys


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
