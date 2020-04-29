from snratio.lib.info import Paths
from snratio.lib.info import Keywords
from snratio.lib.info import CurrentSelections

from snratio.lib.table import Data
from snratio.lib.table import MassNumberTable
from snratio.lib.table import IaTable
from snratio.lib.table import CcTable
from snratio.lib.table import SolarTable

from snratio.lib.utils import merge_tables

from snratio.lib.stats import Stats
from snratio.lib.plots import Plots


class Calculator(Paths, Keywords, CurrentSelections):
    def __init__(self):
        self.data_table = None
        self.mass_number_table = None
        self.Ia_table = None
        self.cc_table = None
        self.solar_table = None

        self.merged_table = None

        self.stats = None
        self.plots = None

        self.all_elements = None
        self.ref_element = None
        self.selected_elements = None
        self.selected_data = None

    def initialise_data_table(self):
        path = self.get_path(self.get_selection("data"))
        self.ref_element = self.get_selection("ref_element")

        self.data_table = Data(path=path, ref_element=self.ref_element)
        self.all_elements = self.data_table.data["Element"].values

    def initialise_selected_data(self):
        filt = self.data_table.data["Element"].isin(self.selected_elements)
        self.selected_data = self.data_table.data[filt]

    def initialise_mass_number_table(self):
        path = self.get_path("mass_number")

        self.mass_number_table = MassNumberTable(path=path)

    def initialise_Ia_table(self):
        path = self.get_path(self.get_selection("Ia_table_name"))
        model = self.get_selection("Ia_model")

        self.Ia_table = IaTable(path=path, model=model)

    def initialise_cc_table(self):
        cc_table_name_selection = self.get_selection("cc_table_name")
        cc_abund_selection = self.get_selection("cc_abund")
        path = self.get_path([cc_table_name_selection, cc_abund_selection])
        abund = self.get_selection("cc_abund")
        mass_range = self.get_selection("cc_mass_range")

        self.cc_table = CcTable(path=path, abund=abund, mass_range=mass_range)

    def initialise_solar_table(self):
        path = self.get_path(self.get_selection("solar_table_name"))
        ref_element = self.get_selection("ref_element")

        self.solar_table = SolarTable(path=path, ref_element=ref_element)

    def initialise_stats(self):
        table = self.merged_table
        ref_element = self.get_selection("ref_element")
        sigma = self.get_selection("sigma")
        self.stats = Stats(table=table, ref_element=ref_element, sigma=sigma)

    def initialise_plots(self):
        table = self.merged_table
        ref_element = self.get_selection("ref_element")
        fit_results = self.stats.fit_results
        chi_list = self.stats.chi_list
        P_list = self.stats.P_list
        Ia_fraction_list = self.stats.Ia_fraction_list

        self.plots = Plots(table=table,
                           ref_element=ref_element,
                           fit_results=fit_results,
                           chi_list=chi_list,
                           P_list=P_list,
                           Ia_fraction_list=Ia_fraction_list)

    def initialise_all(self):
        #self.initialise_data_table()
        self.initialise_mass_number_table()
        self.initialise_Ia_table()
        self.initialise_cc_table()
        self.initialise_solar_table()

    def merge(self):
        #t1 = self.data_table.data
        t1 = self.selected_data
        t2 = self.mass_number_table.data
        t3 = self.Ia_table.model_yields
        t4 = self.cc_table.integrated_yields
        t5 = self.solar_table.data

        self.merged_table = merge_tables(t1, t2, t3, t4, t5)

    def fit(self):
        self.merge()
        self.initialise_stats()
        self.stats.fit()

    def initialise_after_fit(self):
        self.initialise_plots()

    def update_tables_for_new_selections(self):
        pass

    def set_selected_elements(self, element_list):
        self.selected_elements = element_list
        print("set_selected_elements")
