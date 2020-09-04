import pandas as pd
import numpy as np

from snratio.lib.utils import division_error


class Reader:
    def __init__(self, path, with_header=True, read_from_gui=False, gui_elements=None, gui_values=None, gui_errors=None):
        self.path = path
        self.with_header = with_header
        self.data = None
        self.elements = None

        self.read_from_gui = read_from_gui
        self.gui_elements = gui_elements
        self.gui_values = gui_values
        self.gui_errors = gui_errors

        if not self.read_from_gui:
            try:
                self.read_data()
            except FileNotFoundError:
                raise FileNotFoundError("{}".format(path))

            if with_header:
                self.set_elements()

        else:
            self.set_from_gui()

    def read_data(self, sep="\s+"):
        if self.with_header is True:
            self.data = pd.read_csv(self.path, sep=sep)
        else:
            self.data = pd.read_csv(self.path, sep=sep, header=None)

    def set_elements(self):
        self.elements = self.data.iloc[:, 0].unique()

    def set_columns(self, columns):
        self.data.columns = columns

    def set_from_gui(self):
        self.data = pd.DataFrame({"Element": self.gui_elements,
                                  "Abund": self.gui_values,
                                  "AbundError": self.gui_errors})


class Data(Reader):
    def __init__(self, path, ref_element="Fe", with_header=False, read_from_gui=False, gui_elements=None, gui_values=None, gui_errors=None):
        Reader.__init__(self, path, with_header, read_from_gui, gui_elements, gui_values, gui_errors)
        self.ref_element = ref_element

        if "element" == str(self.data.iloc[0, 0]).lower():
            self.data.columns = self.data.iloc[0, :]
            self.data = self.data.iloc[1:]
        else:
            self.set_columns(["Element", "Abund", "AbundError"])

        self.set_elements()
        self.normalise_abund_data()

    def normalise_abund_data(self):
        if self.ref_element != "H":
            ref_row = self.data["Element"] == self.ref_element
            ref_value_ratio = self.data[ref_row]["Abund"]
            ref_value_ratio_err = self.data[ref_row]["AbundError"]

            if float(ref_value_ratio) == 1.0:
                ref_value_ratio_err = float(ref_value_ratio) * 0.001

            if float(ref_value_ratio_err) == 0.0:
                ref_value_ratio_err = float(ref_value_ratio) * 0.001


            normalised_values = []
            for r, r_err in zip(self.data["Abund"], self.data["AbundError"]):
                normalised_values.append(division_error(r, r_err, ref_value_ratio, ref_value_ratio_err))

            normalised_ratio, normalised_ratio_err = zip(*normalised_values)

            column_name_ratio = "{}_normalised_abund".format(self.ref_element)
            column_name_ratio_err = "{}_normalised_abund_err".format(self.ref_element)

            self.data[column_name_ratio] = normalised_ratio
            self.data[column_name_ratio_err] = normalised_ratio_err

            """
            # this part creates a bug when the Fe value is 1.0
            # disabled for now, so it normalises all the time even if the Fe is already 1.0
            
            if float(ref_value_ratio) != 1.0:
                normalised_values = []
                for r, r_err in zip(self.data["Abund"], self.data["AbundError"]):
                    normalised_values.append(division_error(r, r_err, ref_value_ratio, ref_value_ratio_err))

                normalised_ratio, normalised_ratio_err = zip(*normalised_values)

                column_name_ratio = "{}_normalised_abund".format(self.ref_element)
                column_name_ratio_err = "{}_normalised_abund_err".format(self.ref_element)

                self.data[column_name_ratio] = normalised_ratio
                self.data[column_name_ratio_err] = normalised_ratio_err
            else:
                column_name_ratio = "{}_normalised_abund".format(self.ref_element)
                column_name_ratio_err = "{}_normalised_abund_err".format(self.ref_element)

                self.data[column_name_ratio] = self.data["Abund"]
                self.data[column_name_ratio_err] = self.data["AbundError"]
            """
        else:
            column_name_ratio = "{}_normalised_abund".format(self.ref_element)
            column_name_ratio_err = "{}_normalised_abund_err".format(self.ref_element)

            self.data[column_name_ratio] = self.data["Abund"]
            self.data[column_name_ratio_err] = self.data["AbundError"]


class MassNumberTable(Reader):
    def __init__(self, path):
        Reader.__init__(self, path)


class SolarTable(Reader):
    def __init__(self, path, ref_element="Fe"):
        self.path = path
        self.ref_element = ref_element
        Reader.__init__(self, path)

        self.normalise_solar_table()

    def normalise_solar_table(self):
        ref_row = self.data["Element"] == self.ref_element
        ref_value = self.data[ref_row]["Solar"]
        temp_list = 10.0 ** (self.data["Solar"] - ref_value.values[0])
        column_name = "{}_normalised_solar".format(self.ref_element)
        self.data[column_name] = temp_list


class IaTable(Reader):
    def __init__(self, path, model):
        Reader.__init__(self, path)
        self.model = model
        self.model_list = self.data.columns[3:].values

        self.yields = pd.DataFrame()
        self.set_yields()

        self.model_yields = None
        self.set_model_yields()

    def set_yields(self):
        self.yields["Element"] = self.elements
        sum_yields_dict = {}

        for element in self.elements:
            element_sum_list = []
            for model in self.model_list:
                filt = self.data[self.data.columns[0]] == element
                element_sum_list.append(self.data[filt][model].astype(np.float).sum())

            sum_yields_dict[element] = element_sum_list

        for m, y in zip(self.model_list, zip(*sum_yields_dict.values())):
            self.yields[m] = y

    def set_model(self, model=None):
        if model is None:
            self.model = "W7"
        else:
            self.model = model

    def set_model_yields(self):
        if self.model not in self.model_list:
            self.model = "W7"
            print("Invalid model. Model is set to 'W7'...")

        self.model_yields = self.yields[["Element", self.model]]

        model_yields_column_name = "IaYields"
        self.model_yields.columns.values[-1] = model_yields_column_name


class CcTable(Reader):
    def __init__(self, path, abund, mass_range, integrated=False):
        Reader.__init__(self, path)
        self.abund = abund
        self.mass_range = mass_range
        self.integrated = integrated
        self.integral_steps = 250

        """
        if self.elements[1] == "Element":
            new_column_names = ["Element"]
            new_column_names.append(self.elements[0])
            new_column_names.append(self.elements[:2])

            self.data = self.data.reindex(columns=new_column_names)
            self.set_elements()
        """

        self.mass_list = self.data.columns[2:]

        self.yields = pd.DataFrame()
        self.set_yields()

        self.integrated_yields = None

        if self.integrated:
            self.select_integrated_mass_value()
        else:
            self.integrate_yields()

    def set_yields(self):
        self.yields["Element"] = self.elements
        sum_yields_dict = {}

        for element in self.elements:
            element_sum_list = []
            for mass in self.mass_list:
                filt = self.data[self.data.columns[0]] == element
                element_sum_list.append(self.data[filt][mass].sum())

            sum_yields_dict[element] = element_sum_list

        for m, y in zip(self.mass_list, zip(*sum_yields_dict.values())):
            self.yields[m] = y

    @staticmethod
    def salpeter_imf_integral(r1, r2):
        r1 = float(r1)
        r2 = float(r2)
        return -1.0 / 1.35 * (r2 ** (-1.35) - r1 ** (-1.35))

    def get_closest_mass_value(self, m):
        diff_list = [abs(m - int(float(M))) for M in self.mass_list]
        index = diff_list.index(min(diff_list))
        return self.mass_list[index]

    def integrate_yields(self):
        limits = [float(i) for i in self.mass_range.split("-")]
        steps = self.integral_steps

        mass_range = np.linspace(*limits, int(steps))
        delta_m = (limits[1] - limits[0]) / steps

        closest_mass_list = [self.get_closest_mass_value(m) for m in mass_range]
        yields_list = []

        for index, row in self.yields.iterrows():
            a = 0.0
            b = -1.0 / 1.35 * (limits[1] ** (-1.35) - limits[0] ** (-1.35))

            for m_rng, m_cls in zip(mass_range, closest_mass_list):
                a += row[m_cls] * m_rng ** (-2.35) * delta_m

            yields_list.append(a / b)

        self.yields["CcYields"] = yields_list
        self.integrated_yields = self.yields[["Element", "CcYields"]]

        integrated_yields_column_name = "CcYields"
        self.integrated_yields.columns.values[-1] = integrated_yields_column_name

    def select_integrated_mass_value(self, mass_value=50):
        self.integrated_yields = self.yields[["Element", str(mass_value)]]

        integrated_yields_column_name = "CcYields"
        self.integrated_yields.columns.values[-1] = integrated_yields_column_name

    @classmethod
    def set_integral_limits(cls, limits=None):
        if limits is None:
            limits = [10, 50]

        cls.integral_limits = limits

    @classmethod
    def set_integral_steps(cls, steps=250):
        cls.integral_steps = steps
