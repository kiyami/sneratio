from snratio.lib.calculator import Calculator

from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

        self.button_data_load.clicked.connect(self.load)
        self.button_fit.clicked.connect(self.fit_func)

        self.box_sncc_table.currentTextChanged.connect(self.change_sncc_table)
        self.box_sncc_year.currentTextChanged.connect(self.change_sncc_year)
        self.box_sncc_abund.currentTextChanged.connect(self.change_sncc_abund)

        self.box_snIa_model.currentTextChanged.connect(self.set_snIa_model)

        self.box_solar_table.currentTextChanged.connect(self.change_solar_table)
        self.box_solar_ref.currentTextChanged.connect(self.change_solar_ref)

        self.box_fit_sigma.currentTextChanged.connect(self.change_sigma)

        self.plot_area_grid_layout = QtWidgets.QGridLayout(self.plot_area)

    def load(self):
        print(Calculator.parameter_dict)

    def fit_func(self):
        Calculator.initialise()
        Calculator.merge()
        Calculator.fit()

        fig = Calculator.generate_plot()
        canvas = FigureCanvas(fig)
        self.plot_area_grid_layout.addWidget(canvas, 0, 0)

        #fig = Figure(dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        #ax = fig.add_subplot(111)
        #ax.plot([1, 2, 3], [1, 2, 3])
        #canvas = FigureCanvas(fig)
        #self.plot_area_grid_layout.addWidget(canvas, 0, 0)

    def change_sncc_table(self):
        Calculator.parameter_dict["CcTable"]["table_list"][0] = self.box_sncc_table.currentText()

        if self.box_sncc_table.currentIndex() == 0:
            for _ in range(self.box_sncc_year.count()):
                self.box_sncc_year.removeItem(0)

            self.box_sncc_year.addItems(nomoto_year)

        elif self.box_sncc_table.currentIndex() == 1:
            for _ in range(self.box_sncc_year.count()):
                self.box_sncc_year.removeItem(0)

            self.box_sncc_year.addItems(tsujimoto_year)

    def change_sncc_year(self):
        Calculator.parameter_dict["CcTable"]["table_list"][1] = self.box_sncc_year.currentText()

        if self.box_sncc_year.currentIndex() == 0:
            for _ in range(self.box_sncc_abund.count()):
                self.box_sncc_abund.removeItem(0)

            self.box_sncc_abund.addItems(nomoto_2006_abund)

        elif self.box_sncc_year.currentIndex() == 1:
            for _ in range(self.box_sncc_abund.count()):
                self.box_sncc_abund.removeItem(0)

            self.box_sncc_abund.addItems(tsujimoto_1995_abund)

    def change_sncc_abund(self):
        Calculator.parameter_dict["CcTable"]["table_list"][2] = self.box_sncc_abund.currentText()

    def set_snIa_model(self):
        Calculator.parameter_dict["IaTable"]["model"] = self.box_snIa_model.currentText()

    def change_solar_table(self):
        Calculator.parameter_dict["solar_table"]["table"] = self.box_solar_table.currentText()

    def change_solar_ref(self):
        Calculator.parameter_dict["ref_element"] = self.box_solar_ref.currentText()

    def change_sigma(self):
        Calculator.parameter_dict["stat"]["sigma"] = self.box_fit_sigma.currentText()


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
    #Calculator.initialise()
    #Calculator.merge()
    #Calculator.fit()
