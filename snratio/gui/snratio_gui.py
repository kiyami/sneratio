from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide2 import QtCore
import sys
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

from snratio.gui.qt_snratio import Ui_MainWindow

nomoto_year = ["2013", "2006"]
nomoto_2013_abund = ["0.0", "0.001", "0.004", "0.008", "0.02", "0.05"]
nomoto_2006_abund = ["0.0", "0.001", "0.004", "0.02"]

tsujimoto_year = ["1995"]
tsujimoto_1995_abund = ["Default"]

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.button_fit.clicked.connect(self.fit_func)
        #self.cc_table.view().pressed.connect(self.deneme)
        self.box_sncc_table.currentTextChanged.connect(self.set_sncc_year)

        self.plot_area_grid_layout = QtWidgets.QGridLayout(self.plot_area)

    def fit_func(self):
        fig = Figure(dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3], [1, 2, 3])
        canvas = FigureCanvas(fig)
        self.plot_area_grid_layout.addWidget(canvas, 0, 0)

    def set_sncc_year(self):
        if self.box_sncc_table.currentIndex() == 0:
            for _ in range(self.box_sncc_table.count()):
                self.box_sncc_year.removeItem(0)

            self.box_sncc_year.addItems(nomoto_year)

        elif self.box_sncc_table.currentIndex() == 1:
            for _ in range(self.box_sncc_table.count()):
                self.box_sncc_year.removeItem(0)

            self.box_sncc_year.addItems(tsujimoto_year)




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()

    #print(dir(win.cc_table))

    win.show()

    sys.exit(app.exec_())
