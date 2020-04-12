from snratio.lib.info import Paths
from snratio.lib.info import Keywords
from snratio.lib.info import CurrentSelections

from snratio.lib.table import Data
from snratio.lib.table import MassNumberTable
from snratio.lib.table import IaTable
from snratio.lib.table import CcTable
from snratio.lib.table import SolarTable


class Calculator(Paths, Keywords, CurrentSelections):
    def __init__(self):
        self.data_table = None
        self.mass_number_table = None
        self.Ia_table = None
        self.cc_table = None
        self.solar_table = None

        self.stats = None
        self.plots = None

    def initialise_data_table(self):
        path = self.get_path(self.get_selection("Ia_table_name"))
        ref_element = self.get_selection("ref_element")

        self.data_table = Data(path=path, ref_element=ref_element)

    def initialise_mass_number_table(self):
        path = self.get_path("mass_number")

        self.mass_number_table = MassNumberTable(path=path)

    def initialise_Ia_table(self):
        pass

    def initialise_cc_table(self):
        pass

    def initialise_solar_table(self):
        pass
