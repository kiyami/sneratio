import os
from snratio.gui.qt_snratio import Ui_MainWindow
from snratio.lib.main import Calculator
from snratio.lib.utils import check_and_create_directory

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PySide2 import QtWidgets
from PySide2 import QtCore
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.plot_area_grid_layout = QtWidgets.QGridLayout(self.widget_plot_area)

        self.checkbox_dict = {"C": self.checkBox_C,
                              "N": self.checkBox_N,
                              "O": self.checkBox_O,
                              "Ne": self.checkBox_Ne,
                              "Mg": self.checkBox_Mg,
                              "Al": self.checkBox_Al,
                              "Si": self.checkBox_Si,
                              "S": self.checkBox_S,
                              "Ar": self.checkBox_Ar,
                              "Ca": self.checkBox_Ca,
                              "Fe": self.checkBox_Fe,
                              "Ni": self.checkBox_Ni}

        self.calculator = Calculator()

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
        #if path == "":
        #    self.calculator.update_selection("data", "test_data")
        #else:
        #    self.calculator.update_selection("data", "loaded_data")

        if path == "":
            path = self.calculator.data["test_data"]

        if os.path.exists(path):
            self.calculator.data["loaded_data"] = os.path.abspath(path)
            self.set_terminal("Data loaded: '{}'..".format(os.path.basename(path)))
        else:
            self.set_terminal("Warning: Can not open '{}'!".format(path))

        self.calculator.initialise_data_table()
        self.fill_checkboxes()


    def plot_fit(self):
        if self.calculator.plots is not None:
            self.fit_figure = self.calculator.plots.get_fit_plot()
        else:
            raise AttributeError("Figure class is not initialised!")

        canvas = FigureCanvas(self.fit_figure)
        self.plot_area_grid_layout.addWidget(canvas, 0, 0)

    def plot_likelihood(self):
        if self.calculator.plots is not None:
            self.likelihood_figure = self.calculator.plots.get_likelihood_plot()
        else:
            raise AttributeError("Figure class is not initialised!")

        canvas = FigureCanvas(self.likelihood_figure)
        self.plot_area_grid_layout.addWidget(canvas, 0, 0)

    def plot_chi(self):
        if self.calculator.plots is not None:
            self.chi_figure = self.calculator.plots.get_chi_plot()
        else:
            raise AttributeError("Figure class is not initialised!")

        canvas = FigureCanvas(self.chi_figure)
        self.plot_area_grid_layout.addWidget(canvas, 0, 0)

    def fit_func(self):
        self.calculator.initialise_data_table()

        selected_elements = []
        for element, checkbox in self.checkbox_dict.items():
            if checkbox.isChecked() == True:
                selected_elements.append(element)

        self.calculator.selected_elements = selected_elements
        self.calculator.initialise_selected_data()

        self.set_terminal("Reading tables..")
        self.calculator.initialise_all()
        self.set_terminal("Merging tables..")
        self.set_terminal("Fitting started..")
        self.calculator.fit()
        self.set_terminal("Fit completed..")
        self.calculator.initialise_after_fit()

        self.set_fit_results()
        self.plot_fit()


    def save_plots(self, path="outputs"):
        check_and_create_directory(os.path.join(os.curdir, path))

        if self.fit_figure is None:
            self.fit_figure = self.calculator.plots.get_fit_plot()

        self.fit_figure.set_size_inches(10, 7)
        self.fit_figure.savefig(os.path.join(path, "Figure_Fit.png"))

        if self.likelihood_figure is None:
            self.likelihood_figure = self.calculator.plots.get_likelihood_plot()

        self.likelihood_figure.set_size_inches(10, 7)
        self.likelihood_figure.savefig(os.path.join(path, "Figure_Likelihood.png"))

        if self.chi_figure is None:
            self.chi_figure = self.calculator.plots.get_chi_plot()

        self.chi_figure.set_size_inches(10, 7)
        self.chi_figure.savefig(os.path.join(path, "Figure_Chi_Squared.png"))

    def save_stats(self, path="outputs"):
        check_and_create_directory(os.path.join(os.curdir, path))

        file_name = "Log_File.txt"
        with open(os.path.join(path, file_name), mode="w") as f:
            f.writelines(self.calculator.stats.get_fit_results_text())

    def save_all(self):
        self.save_plots()
        self.save_stats()

    def set_sncc_table(self):
        new_selection_gui_keyword = self.box_sncc_table.currentText()
        new_selection_inner_keyword = self.calculator.get_inner_keyword(new_selection_gui_keyword)
        self.calculator.update_selection("cc_table_name", new_selection_inner_keyword)

        self.update_sncc_abund_box()

    def update_sncc_abund_box(self):
        new_cc_table_gui_keyword = self.box_sncc_table.currentText()
        new_cc_table_inner_keyword = self.calculator.get_inner_keyword(new_cc_table_gui_keyword)
        for _ in range(self.box_sncc_abund.count()):
            self.box_sncc_abund.removeItem(0)

        new_abund_values = self.calculator.cc_valid_abundances[new_cc_table_inner_keyword]
        self.box_sncc_abund.addItems(new_abund_values)

    def set_sncc_abund(self):
        new_selection_gui_keyword = self.box_sncc_abund.currentText()
        new_selection_inner_keyword = new_selection_gui_keyword
        self.calculator.update_selection("cc_abund", new_selection_inner_keyword)

    def set_mass(self):
        new_selection_gui_keyword = self.box_sncc_mass.currentText()
        new_selection_inner_keyword = self.calculator.get_inner_keyword(new_selection_gui_keyword)
        self.calculator.update_selection("cc_mass_range", new_selection_inner_keyword)

    def set_Ia_table(self):
        new_selection_gui_keyword = self.box_snIa_table.currentText()
        new_selection_inner_keyword = self.calculator.get_inner_keyword(new_selection_gui_keyword)
        self.calculator.update_selection("Ia_table_name", new_selection_inner_keyword)

        self.update_snIa_model_box()

    def update_snIa_model_box(self):
        new_Ia_table_gui_keyword = self.box_snIa_table.currentText()
        new_Ia_table_inner_keyword = self.calculator.get_inner_keyword(new_Ia_table_gui_keyword)
        for _ in range(self.box_snIa_model.count()):
            self.box_snIa_model.removeItem(0)

        new_model_values = self.calculator.Ia_valid_models["Ia_valid_models"][new_Ia_table_inner_keyword]
        self.box_snIa_model.addItems(new_model_values)

    def set_snIa_model(self):
        new_selection_gui_keyword = self.box_snIa_model.currentText()
        new_selection_inner_keyword = new_selection_gui_keyword
        self.calculator.update_selection("Ia_model", new_selection_inner_keyword)

    def set_solar_table(self):
        new_selection_gui_keyword = self.box_solar_table.currentText()
        new_selection_inner_keyword = self.calculator.get_inner_keyword(new_selection_gui_keyword)
        self.calculator.update_selection("solar_table_name", new_selection_inner_keyword)

    def set_ref(self):
        new_selection_gui_keyword = self.box_ref.currentText()
        new_selection_inner_keyword = self.calculator.get_inner_keyword(new_selection_gui_keyword)
        self.calculator.update_selection("ref_element", new_selection_inner_keyword)

    def set_sigma(self):
        new_selection_gui_keyword = self.box_sigma.currentText()
        new_selection_inner_keyword = self.calculator.get_inner_keyword(new_selection_gui_keyword)
        self.calculator.update_selection("sigma", new_selection_inner_keyword)

    def set_fit_results(self):
        text = self.calculator.stats.get_fit_results_text()
        self.plainTextEdit_fit_results.setPlainText(text)
        self.repaint()

    def set_terminal(self, text):
        modified_text = "term$ {}".format(text)
        self.plainTextEdit_terminal.appendPlainText(modified_text)
        self.repaint()


    def check_checkbox(self, element):
        self.checkbox_dict[element].setChecked(True)

    def uncheck_checkbox(self, element):
        self.checkbox_dict[element].setChecked(False)

    def set_checkbox_checkable(self, element):
        self.checkbox_dict[element].setDisabled(False)
        self.checkbox_dict[element].setCheckable(True)

    def set_checkbox_uncheckable(self, element):
        self.checkbox_dict[element].setCheckable(False)
        self.checkbox_dict[element].setDisabled(True)

    def set_checkbox_ref_element(self, element):
        self.checkbox_dict[element].setChecked(True)

    def fill_checkboxes(self):
        for element in self.checkbox_dict.keys():
            if element in self.calculator.all_elements:
                print(element)
                if element == self.calculator.ref_element:
                    self.set_checkbox_ref_element(element)
                else:
                    self.set_checkbox_checkable(element)
                    self.check_checkbox(element)
            else:
                self.set_checkbox_uncheckable(element)
                self.uncheck_checkbox(element)

        self.repaint()



"""
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
            for _ in range(self.box_sncc_abund.count()):
                self.box_sncc_abund.removeItem(0)

            self.box_sncc_abund.addItems(self.cc_info_dict["nomoto_2013"])

        elif self.box_sncc_table.currentText() == "Nomoto (2006)":

            for _ in range(self.box_sncc_abund.count()):
                self.box_sncc_abund.removeItem(0)

            self.box_sncc_abund.addItems(self.cc_info_dict["nomoto_2006"])

        if self.box_sncc_table.currentText() == "Tsujimoto (1995)":
            for _ in range(self.box_sncc_table.count()):
                self.box_sncc_abund.removeItem(0)

            self.box_sncc_abund.addItems(self.cc_info_dict["tsujimoto_1995"])

    def set_sncc_abund(self):
        Calculator.parameter_dict["CcTable"]["table_list"][1] = self.box_sncc_abund.currentText()

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
"""
