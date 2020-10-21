from sneratio.lib.utils import generate_package_path


class Paths:
    data = {
        "test_data": "sneratio/data/test_data/test_data.txt",
        "loaded_data": ""
    }
    mass_number = {
        "mass_number": "sneratio/data/mass_numbers/mass_number.txt"
    }

    Ia = {
        "iwamoto": "sneratio/data/yields/Ia/iwamoto/Iwamoto_ApJ_1999_Table4.txt"
    }

    cc = {
        # "nomoto_2013_0.0": "sneratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0.txt",
        "nomoto_2013_0.001": "sneratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_001.txt",
        "nomoto_2013_0.004": "sneratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_004.txt",
        "nomoto_2013_0.008": "sneratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_008.txt",
        "nomoto_2013_0.02": "sneratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_02.txt",
        "nomoto_2013_0.05": "sneratio/data/yields/cc/nomoto_2013/Nomoto_2013_z_0_05.txt",

        "nomoto_2006_0.0": "sneratio/data/yields/cc/nomoto_2006/Nomoto_2006_Table2_Z_0.txt",
        "nomoto_2006_0.001": "sneratio/data/yields/cc/nomoto_2006/Nomoto_2006_Table2_Z_0_001.txt",
        "nomoto_2006_0.004": "sneratio/data/yields/cc/nomoto_2006/Nomoto_2006_Table2_Z_0_004.txt",
        "nomoto_2006_0.02": "sneratio/data/yields/cc/nomoto_2006/Nomoto_2006_Table2_Z_0_02.txt",

        "tsujimoto_0.0": "sneratio/data/yields/cc/tsujimoto/Tsujimoto_1995_integrated_Table2.txt"
    }

    solar = {
        "lodd": "sneratio/data/solar/lodd.txt",
        "angr": "sneratio/data/solar/angr.txt",
        "aspl": "sneratio/data/solar/aspl.txt"
    }

    path_dictionaries = [data, mass_number, Ia, cc, solar]

    @classmethod
    def get_path(cls, keywords):
        key_separator = "_"
        path = None

        if isinstance(keywords, list):
            master_key = key_separator.join(keywords)
        else:
            master_key = keywords

        for dictionary in cls.path_dictionaries:
            if master_key in dictionary:
                path = dictionary[master_key]

        return generate_package_path(path)


class Keywords:
    Ia = {
        "iwamoto": "Iwamoto (1999)"
    }

    Ia_valid_models = {
        "iwamoto": ["W7", "W70", "WDD1", "WDD2", "WDD3", "CDD1", "CDD2"]
    }

    cc = {
        "nomoto_2013": "Nomoto (2013)",
        "nomoto_2006": "Nomoto (2006)",
        "tsujimoto": "Tsujimoto (1995)",
    }

    cc_valid_abundances = {
        # "nomoto_2013": ["0.0", "0.001", "0.004", "0.008", "0.02", "0.05"],
        "nomoto_2013": ["0.001", "0.004", "0.008", "0.02", "0.05"],
        "nomoto_2006": ["0.0", "0.001", "0.004", "0.02"],
        "tsujimoto": ["0.0"]
    }

    cc_mass_range = {
        "10-50": "10-50 M sun",
        "10-70": "10-70 M sun"
    }

    solar = {
        "lodd": "Lodd",
        "angr": "Angr",
        "aspl": "Aspl",
    }

    ref_elements = {
        "Fe": "Fe",
        "H": "H"
    }

    sigma = {
        "1.0": "1.0",
        "2.0": "2.0"
    }

    keyword_dictionaries = [Ia, cc, cc_mass_range, solar, ref_elements, sigma]
    validation_dictionaries = [Ia_valid_models, cc_valid_abundances]

    @classmethod
    def get_inner_keyword(cls, gui_keyword):
        for dictionary in cls.keyword_dictionaries:
            for inner, gui in dictionary.items():
                if gui_keyword == gui:
                    return inner

    @classmethod
    def get_gui_keyword(cls, inner_keyword):
        for dictionary in cls.keyword_dictionaries:
            for inner, gui in dictionary.items():
                if inner_keyword == inner:
                    return gui


class CurrentSelections:
    selection_dictionary = {
        "data": "test_data",

        "Ia_table_name": "iwamoto",
        "Ia_model": "W7",

        "cc_table_name": "nomoto_2013",
        "cc_abund": "0.02",
        "cc_mass_range": "10-50",

        "solar_table_name": "lodd",

        "ref_element": "Fe",
        "sigma": "1.0"
    }

    @classmethod
    def get_selection(cls, key):
        return cls.selection_dictionary[key]

    @classmethod
    def update_selection(cls, key, value):
        cls.selection_dictionary[key] = value
