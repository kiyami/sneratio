import pandas as pd
import numpy as np

from snratio.lib.utils import division_error
from snratio.lib.utils import generate_path

# sep="\s+|\t+|\s+\t+|\t+\s+|,"


class Reader:
    def __init__(self, file_name, with_header=True):
        self.file_name = file_name
        self.with_header = with_header
        self.data = None
        self.elements = None

        try:
            self.read_data()
        except FileNotFoundError:
            raise FileNotFoundError("{}".format(file_name))

        self.set_elements()

    def read_data(self, sep="\s+"):
        if self.with_header is True:
            self.data = pd.read_csv(self.file_name, sep=sep)
        else:
            self.data = pd.read_csv(self.file_name, sep=sep, header=None)

    def set_elements(self):
        self.elements = self.data.iloc[:, 0].unique()

    def print_data(self):
        print(self.data)

    def set_columns(self, columns):
        self.data.columns = columns

    def print_columns(self):
        print(self.data.columns)


class Data(Reader):
    def __init__(self, path, ref_element="Fe", with_header=True):
        Reader.__init__(self, path, with_header=with_header)
        self.ref_element = ref_element

        if self.with_header is False:
            self.set_columns(["Element", "Abund", "AbundError"])

        self.normalise_abund_data()

    def normalise_abund_data(self):
        ref_row = self.data["Element"] == self.ref_element
        ref_value_ratio = self.data[ref_row]["Abund"]
        ref_value_ratio_err = self.data[ref_row]["AbundError"]

        if int(ref_value_ratio_err) == 0:
            ref_value_ratio_err = 0.1

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


class MassNumberTable(Reader):
    #file_name = generate_path("snratio/data/mass_numbers/mass_number.txt")
    file_name = generate_path("snratio/data/mass_numbers/mass_number.txt")

    def __init__(self):
        Reader.__init__(self, MassNumberTable.file_name)


class SolarTable(Reader):
    file_names = {
        "lodd": generate_path("snratio/data/solar/lodd.txt"),
        "angr": generate_path("snratio/data/solar/angr.txt"),
        "aspl": generate_path("snratio/data/solar/aspl.txt")
    }

    def __init__(self, solar_table="lodd", ref_element="Fe"):
        self.solar_table = solar_table
        self.ref_element = ref_element
        Reader.__init__(self, SolarTable.file_names[solar_table])

        self.normalise_solar_table()

    def normalise_solar_table(self):
        ref_row = self.data["Element"] == self.ref_element
        ref_value = self.data[ref_row]["Solar"]
        temp_list = 10.0 ** (self.data["Solar"] - ref_value.values[0])
        column_name = "{}_normalised_solar".format(self.ref_element)
        self.data[column_name] = temp_list


class IaTable(Reader):
    file_name = generate_path("snratio/data/yields/Ia/iwamoto/Iwamoto_ApJ_1999_Table4.txt")
    model = "W7"

    def __init__(self):
        Reader.__init__(self, IaTable.file_name)

        self.model_list = self.data.columns[3:]

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

    @classmethod
    def set_model(cls, model=None):
        if model is None:
            IaTable.model = "W7"
            print("Model is set to 'W7'...")
        else:
            IaTable.model = model

        cls.model = model

    def set_model_yields(self):
        if IaTable.model not in self.model_list:
            IaTable.model = "W7"
            print("Invalid model. Model is set to 'W7'...")

        self.model_yields = self.yields[["Element", IaTable.model]]

        model_yields_column_name = "IaYields"
        self.model_yields.columns.values[-1] = model_yields_column_name


class CcTable(Reader):
    Nomoto_2006_z_0 = generate_path("snratio/data/yields/cc/nomoto_2006/Nomoto_2006_Table2_Z_0.txt")
    Nomoto_2006_z_0_001 = generate_path("snratio/data/yields/cc/nomoto_2006/Nomoto_2006_Table2_Z_0_001.txt")
    Nomoto_2006_z_0_004 = generate_path("snratio/data/yields/cc/nomoto_2006/Nomoto_2006_Table2_Z_0_004.txt")
    Nomoto_2006_z_0_02 = generate_path("snratio/data/yields/cc/nomoto_2006/Nomoto_2006_Table2_Z_0_02.txt")

    Nomoto_2013_z_0 = generate_path("snratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0.txt")
    Nomoto_2013_z_0_001 = generate_path("snratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_001.txt")
    Nomoto_2013_z_0_004 = generate_path("snratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_004.txt")
    Nomoto_2013_z_0_008 = generate_path("snratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_008.txt")
    Nomoto_2013_z_0_02 = generate_path("snratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_02.txt")
    Nomoto_2013_z_0_05 = generate_path("snratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_05.txt")

    Tsujimoto_file = generate_path("snratio/data/yields/cc/tsujimoto/Tsujimoto_1995_integrated_Table2.txt")

    table_dict = {
        "nomoto": {
            "2006": {
                "0": Nomoto_2006_z_0,
                "0.001": Nomoto_2006_z_0_001,
                "0.004": Nomoto_2006_z_0_004,
                "0.02": Nomoto_2006_z_0_02
            },
            "2013": {
                "0": Nomoto_2013_z_0,
                "0.001": Nomoto_2013_z_0_001,
                "0.004": Nomoto_2013_z_0_004,
                "0.008": Nomoto_2013_z_0_008,
                "0.02": Nomoto_2013_z_0_02,
                "0.05": Nomoto_2013_z_0_05
            }
        },
        "iwamoto": Tsujimoto_file
    }

    integral_limits = [10, 50]
    integral_steps = 250

    table = "nomoto"
    year = "2013"
    abund = "0.02"

    def __init__(self, integrated=False):
        file_name = CcTable.get_file_name()
        Reader.__init__(self, file_name)

        self.integrated = integrated
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
        limits = self.integral_limits
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

    @classmethod
    def set_table(cls, table=None, year=None, abund=None):
        if table is not None:
            table = table.lower()
        else:
            raise ValueError("Enter a SNcc table name!")

        if year is not None:
            year = str(year)

        if abund is not None:
            abund = str(abund)

        if table in cls.table_dict:
            cls.table = table
        else:
            raise ValueError("Invalid SNcc table name!")

        if isinstance(cls.table_dict[table], type(dict())):
            if year in cls.table_dict[table]:
                cls.year = year
            else:
                raise ValueError("Invalid SNcc table year!")
        else:
            cls.year = None

            if isinstance(cls.table_dict[table][year], type(dict())):
                if abund in cls.table_dict[table][year]:
                    cls.abund = abund
                else:
                    raise ValueError("Invalid SNcc table abund value!")
            else:
                cls.abund = None

    @classmethod
    def get_file_name(cls):
        temp_file = cls.table_dict

        if cls.table is not None:
            temp_file = temp_file[cls.table]
            if cls.year is not None:
                temp_file = temp_file[cls.year]
                if cls.abund is not None:
                    temp_file = temp_file[cls.abund]
        else:
            raise ValueError("Table name is not set yet!")

        return temp_file
