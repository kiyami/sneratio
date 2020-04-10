from snratio.lib.table import Data
from snratio.lib.table import MassNumberTable
from snratio.lib.table import SolarTable
from snratio.lib.table import IaTable
from snratio.lib.table import CcTable

from snratio.lib.utils import merge_tables
from snratio.lib.utils import generate_path

from snratio.stats.stats import Stats


class Calculator:
    parameter_dict = {
        "data": {
            "path": generate_path("snratio/data/test_data/test_data.txt"),
            "with_header": True
        },

        "mass_number_table": {},

        "solar_table": {
            "table": "lodd"
        },

        "IaTable": {
            "table": "Iwamoto",
            "model": "W7"
        },

        "CcTable": {
            "table_list": ["Nomoto", "2013", "0.02"],
            "integral_limits": [10,50],
            "integral_steps": 250
        },

        "ref_element": "Fe",

        "stat": {
            "iteration_number": 1000,
            "sigma": 1.0
        }
    }

    data = None
    mass_number_table = None
    solar_table = None
    merged_table = None

    stat = None
    fit_stat_text = ""

    fig_chi = None
    fig_fit = None

    @classmethod
    def initialise(cls):
        cls.data = Data(cls.parameter_dict["data"]["path"], with_header=cls.parameter_dict["data"]["with_header"])

        cls.mass_number_table = MassNumberTable()

        # solar_tables = ["lodd", "angr", "aspl"]
        cls.solar_table = SolarTable(cls.parameter_dict["solar_table"]["table"])

        IaTable.set_model(cls.parameter_dict["IaTable"]["model"])
        cls.Ia_table = IaTable()

        # ------------------
        # cc_yield tables
        # ------------------
        # Nomoto
        #   2006
        #       0
        #       0.001
        #       0.004
        #       0.02
        #   2013
        #       0
        #       0.001
        #       0.004
        #       0.008
        #       0.02
        #       0.05
        # ------------------
        # Tsujimoto
        # ------------------

        table, year, abund = cls.parameter_dict["CcTable"]["table_list"]
        CcTable.set_table(table=table, year=year, abund=abund)
        CcTable.set_integral_limits(cls.parameter_dict["CcTable"]["integral_limits"])
        CcTable.set_integral_steps(cls.parameter_dict["CcTable"]["integral_steps"])

        cls.cc_table = CcTable()

        #data.print_columns()
        #mass_number_table.print_columns()
        #solar_table.print_columns()
        #Ia_table.print_columns()
        #cc_table.print_columns()
        #data.print_data()

    @classmethod
    def merge(cls):
        t1 = cls.mass_number_table.data
        t2 = cls.data.data
        t3 = cls.solar_table.data
        t4 = cls.Ia_table.model_yields
        t5 = cls.cc_table.integrated_yields

        cls.merged_table = merge_tables(t1, t2, t3, t4, t5)
        #print(merged_table)

    @classmethod
    def fit(cls):
        cls.stat = Stats(table=cls.merged_table, ref_element=cls.parameter_dict["ref_element"])

        cls.stat.set_iteration_number(N=cls.parameter_dict["stat"]["iteration_number"])
        cls.stat.set_sigma(sigma=cls.parameter_dict["stat"]["sigma"])
        cls.stat.fit()
        #cls.stat.print_fit_values()

