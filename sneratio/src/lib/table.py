import pandas as pd
import numpy as np
import os
from sneratio.src.lib import info
from sneratio.src.lib import utils


class Data:
    Ia_table = None
    cc_table = None
    solar_table = None
    mass_number_table = None
    input_data = None

    elements = None
    ref_element = None
    ref_row_index = None
    cc_table_integral_steps = 250

    merged_table = None

    @staticmethod
    def read_data(path, with_header=True, sep="\s+"):
        if not os.path.exists(path):
            raise FileNotFoundError("{}".format(path))

        if with_header is True:
            data = pd.read_csv(path, sep=sep)
        else:
            data = pd.read_csv(path, sep=sep, header=None)

        return data

    @staticmethod
    def read_Ia_table():
        Ia_table_path = info.get_selected_option_path("Ia_table")
        Data.Ia_table = Data.read_data(Ia_table_path)

    @staticmethod
    def read_cc_table():
        cc_table_path = info.get_selected_option_path("cc_table")
        Data.cc_table = Data.read_data(cc_table_path)

    @staticmethod
    def read_solar_table():
        solar_table_path = info.get_selected_option_path("solar_table")
        Data.solar_table = Data.read_data(solar_table_path)

    @staticmethod
    def read_mass_number_table():
        mass_number_table_path = info.get_selected_option_path("mass_number_table")
        Data.mass_number_table = Data.read_data(mass_number_table_path)

    @staticmethod
    def read_input_data():
        input_data_path = info.get_selected_option_path("input_data")
        Data.input_data = Data.read_data(input_data_path)

    @staticmethod
    def read_all_data():
        Data.read_Ia_table()
        Data.read_cc_table()
        Data.read_solar_table()
        Data.read_mass_number_table()
        Data.set_input_data()

    @staticmethod
    def print_all_info():
        print(Data.Ia_table.info())
        print(Data.cc_table.info())
        print(Data.solar_table.info())
        print(Data.mass_number_table.info())
        print(Data.input_data.info())

    @staticmethod
    def set_input_data():
        element_list = info.elements_dict["element"]
        abund_list = [float(a) for a in info.elements_dict["abund"]]
        abund_error_list = [float(a) for a in info.elements_dict["abund_err"]]

        columns = ["Element", "Abund", "AbundError"]
        Data.input_data = pd.DataFrame([*zip(element_list, abund_list, abund_error_list)], columns=columns)

    @classmethod
    def set_elements_from_input_data(cls):
        if cls.input_data is not None:
            cls.elements = cls.input_data.iloc[:, 0].unique()
        else:
            raise ValueError(f"Data.input_data is None!")

    @classmethod
    def set_ref_element(cls):
        cls.ref_element = info.get_selected_option("ref_element")

    @classmethod
    def set_ref_row_index(cls):
        try:
            cls.ref_row_index = np.where(cls.elements == cls.ref_element)[0][0]
        except:
            raise ValueError

    @classmethod
    def initialise_merged_table(cls):
        cls.merged_table = pd.DataFrame(cls.elements, columns=["Element"])

    @classmethod
    def normalise_input_data(cls):
        ref_element = info.get_selected_option("ref_element")
        if ref_element != "H":
            ref_row = cls.input_data["Element"] == ref_element
            cls.ref_row_index = list(ref_row).index(True)

            ref_value_ratio = cls.input_data[ref_row]["Abund"]
            ref_value_ratio_err = cls.input_data[ref_row]["AbundError"]

            if float(ref_value_ratio) == 1.0:
                ref_value_ratio_err = float(ref_value_ratio) * 0.001

            if float(ref_value_ratio_err) == 0.0:
                ref_value_ratio_err = float(ref_value_ratio) * 0.001

            normalised_values = []
            for r, r_err in zip(cls.input_data["Abund"], cls.input_data["AbundError"]):
                normalised_values.append(utils.division_error(r, r_err, ref_value_ratio, ref_value_ratio_err))

            normalised_ratio, normalised_ratio_err = zip(*normalised_values)

            cls.merged_table["Abund"] = normalised_ratio
            cls.merged_table["AbundError"] = normalised_ratio_err
        else:
            cls.merged_table["Abund"] = cls.input_data["Abund"]
            cls.merged_table["AbundError"] = cls.input_data["AbundError"]

    @classmethod
    def normalise_solar_table(cls):
        ref_element = info.get_selected_option("ref_element")
        ref_row = cls.solar_table["Element"] == ref_element
        ref_value = cls.solar_table[ref_row]["Solar"]

        temp_list = 10.0 ** (cls.solar_table["Solar"] - ref_value.values[0])
        column_name = "{}_normalised_solar".format(ref_element)
        cls.solar_table[column_name] = temp_list

        filt = cls.solar_table["Element"].isin( cls.elements)
        cls.merged_table["Solar"] = cls.solar_table[filt][column_name].values

    @classmethod
    def get_Ia_model(cls):
        try:
            model = cls.Ia_table.columns[2:].values[0]
            return model
        except:
            raise IndexError(f"Ia model couldn't read!")

    @classmethod
    def set_Ia_yields(cls):
        cls.Ia_yields = pd.DataFrame()

        if cls.elements is not None:
            cls.Ia_yields["Element"] = cls.elements
        else:
            raise ValueError(f"Element list is Null")

        model = cls.Ia_table.columns[-1]
        sum_yields_dict = {}

        for element in cls.elements:
            filt = cls.Ia_table[cls.Ia_table.columns[0]] == element
            element_sum = cls.Ia_table[filt][model].astype(np.float).sum()

            sum_yields_dict[element] = element_sum

        cls.merged_table["Ia_yields"] = [sum_yields_dict[element] for element in cls.elements]

    @classmethod
    def get_cc_mass_list(cls):
        return cls.cc_table.columns[2:]

    @classmethod
    def set_cc_yields(cls):
        cls.cc_yields = pd.DataFrame()

        if cls.elements is not None:
            cls.cc_yields["Element"] = cls.elements
        else:
            raise ValueError(f"Element list is Null")

        mass_range_selection = info.get_selected_option("cc_mass_range")
        limits = info.get_parsed_cc_mass_range_option(mass_range_selection)

        steps = cls.cc_table_integral_steps

        mass_list = cls.get_cc_mass_list()
        mass_list_length = mass_list.shape[0]

        mass_step_list = np.linspace(*limits, int(steps))
        delta_m = (limits[1] - limits[0]) / steps

        closest_mass_list = np.linspace(*limits, int(steps), dtype=np.str)

        j = 0
        for i in range(steps):
            if j < (mass_list_length - 1):
                if mass_step_list[i] < (float(mass_list[j+1]) + float(mass_list[j]))*0.5:
                    closest_mass_list[i] = mass_list[j]
                else:
                    closest_mass_list[i] = mass_list[j+1]
                    j += 1
            else:
                closest_mass_list[i] = mass_list[-1]

        yields_list = []

        for element in cls.elements:
            filt = cls.cc_table[cls.cc_table.columns[0]] == element
            summed_row = cls.cc_table[filt].iloc[:,2:].sum(axis=0)

            a = 0.0
            b = -1.0 / 1.35 * (limits[1] ** (-1.35) - limits[0] ** (-1.35))

            for msl, cml in zip(mass_step_list, closest_mass_list):
                a += summed_row[cml] * msl ** (-2.35) * delta_m

            yields_list.append(a / b)

        cls.merged_table["cc_yields"] = yields_list

    @classmethod
    def set_mass_numbers(cls):
        filt = cls.mass_number_table["Element"].isin(cls.elements)
        cls.merged_table["MassNumber"] = cls.mass_number_table[filt]["MassNumber"].values
