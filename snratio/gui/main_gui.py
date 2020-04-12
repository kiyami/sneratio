import os
from snratio.lib.calculator import Calculator
from snratio.lib.utils import check_and_create_directory

from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PySide2 import QtCore
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

from snratio.gui.qt_snratio_test import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    Ia_info_dict = {
        "iwamoto_1999": ["W7", "W70", "WDD1", "WDD2", "WDD3", "CDD1", "CDD2"]
    }

    cc_info_dict = {
        "nomoto_2013": ["0.0", "0.001", "0.004", "0.008", "0.02", "0.05"],
        "nomoto_2006": ["0.0", "0.001", "0.004", "0.02"],
        "tsujimoto_1995": ["Default"]
    }

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.plot_area_grid_layout = QtWidgets.QGridLayout(self.widget_plot_area)

        self.set_terminal("AstroLab gururla sunar..")

        self.fit_figure = None
        self.likelihood_figure = None
        self.chi_figure = None

        self.button_load.clicked.connect(self.load)

        self.button_plot_fit.clicked.connect(self.plot_fit)
        self.button_plot_likelihood.clicked.connect(self.plot_likelihood)
        self.button_plot_chi.clicked.connect(self.plot_chi)

        self.button_fit.clicked.connect(self.fit_func)

        self.button_save_plots.clicked.connect(self.save_plots)
        self.button_save_stats.clicked.connect(self.save_stats)
        self.button_save_all.clicked.connect(self.save_all)

        self.box_snIa_model.currentTextChanged.connect(self.set_snIa_model)

        self.box_sncc_table.currentTextChanged.connect(self.set_sncc_table)
        self.box_sncc_abund.currentTextChanged.connect(self.set_sncc_abund)

        self.box_solar_table.currentTextChanged.connect(self.set_solar_table)

        self.box_ref.currentTextChanged.connect(self.set_ref)

        self.box_sigma.currentTextChanged.connect(self.set_sigma)

    def load(self):
        path = self.lineEdit_load.text()
        if os.path.exists(path):
            Calculator.parameter_dict["data"]["path"] = os.path.abspath(path)
            self.set_terminal("Data loaded: '{}'..".format(os.path.basename(path)))
        else:
            self.set_terminal("Warning: Can not open '{}'!".format(path))

    def plot_fit(self):
        self.fit_figure = Calculator.stat.get_fit_plot()
        canvas = FigureCanvas(self.fit_figure)
        self.plot_area_grid_layout.addWidget(canvas, 0, 0)

    def plot_likelihood(self):
        self.likelihood_figure = Calculator.stat.get_likelihood_plot()
        canvas = FigureCanvas(self.likelihood_figure)
        self.plot_area_grid_layout.addWidget(canvas, 0, 0)

    def plot_chi(self):
        self.chi_figure = Calculator.stat.get_chi_plot()
        canvas = FigureCanvas(self.chi_figure)
        self.plot_area_grid_layout.addWidget(canvas, 0, 0)

    def fit_func(self):
        self.set_terminal("Reading tables..")
        Calculator.initialise()
        self.set_terminal("Merging tables..")
        Calculator.merge()
        self.set_terminal("Fitting started..")
        Calculator.fit()
        self.set_terminal("Fit completed..")

        self.set_fit_results()

    def save_plots(self, path="outputs"):
        check_and_create_directory(os.path.join(os.curdir, path))

        if self.fit_figure is None:
            self.fit_figure = Calculator.stat.get_fit_plot()

        self.fit_figure.set_size_inches(10,7)
        self.fit_figure.savefig(os.path.join(path, "Figure_Fit.png"))

        if self.likelihood_figure is None:
            self.likelihood_figure = Calculator.stat.get_likelihood_plot()

        self.likelihood_figure.set_size_inches(10, 7)
        self.likelihood_figure.savefig(os.path.join(path, "Figure_Likelihood.png"))

        if self.chi_figure is None:
            self.chi_figure = Calculator.stat.get_chi_plot()

        self.chi_figure.set_size_inches(10, 7)
        self.chi_figure.savefig(os.path.join(path, "Figure_Chi_Squared.png"))

    def save_stats(self, path="outputs"):
        check_and_create_directory(os.path.join(os.curdir, path))

        file_name = "Log_File.txt"
        with open(os.path.join(path, file_name), mode="w") as f:
            f.writelines(Calculator.stat.get_fit_results())

    def save_all(self):
        self.save_plots()
        self.save_stats()

    def set_sncc_table(self):
        Calculator.parameter_dict["CcTable"]["table_list"][0] = self.box_sncc_table.currentText()

        if self.box_sncc_table.currentText() == "Nomoto (2013)":
            for _ in range(self.box_sncc_year.count()):
                self.box_sncc_abund.removeItem(0)

            self.box_sncc_abund.addItems(self.cc_info_dict["nomoto_2013"])

        elif self.box_sncc_table.currentText() == "Nomoto (2006)":

            for _ in range(self.box_sncc_year.count()):
                self.box_sncc_abund.removeItem(0)

            self.box_sncc_abund.addItems(self.cc_info_dict["nomoto_2006"])

        if self.box_sncc_table.currentText() == "Tsujimoto (1995)":
            for _ in range(self.box_sncc_year.count()):
                self.box_sncc_abund.removeItem(0)

            self.box_sncc_abund.addItems(self.cc_info_dict["tsujimoto_1995"])

    def set_sncc_abund(self):
        Calculator.parameter_dict["CcTable"]["table_list"][2] = self.box_sncc_abund.currentText()

    def set_mass(self):
        Calculator.parameter_dict["CcTable"]["integral_limits"] = self.box_sncc_mass.currentText()

    def set_snIa_model(self):
        Calculator.parameter_dict["IaTable"]["model"] = self.box_snIa_model.currentText()

    def set_solar_table(self):
        Calculator.parameter_dict["solar_table"]["table"] = self.box_solar_table.currentText()

    def set_ref(self):
        Calculator.parameter_dict["ref_element"] = self.box_solar_ref.currentText()

    def set_sigma(self):
        Calculator.parameter_dict["stat"]["sigma"] = self.box_fit_sigma.currentText()

    def set_fit_results(self):
        text = Calculator.stat.get_fit_results()
        self.plainTextEdit_fit_results.setPlainText(text)
        self.repaint()

    def set_terminal(self, text):
        modified_text = "term$ {}".format(text)
        self.plainTextEdit_terminal.appendPlainText(modified_text)
        self.repaint()
