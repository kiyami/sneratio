import unittest
from snratio.lib.table import MassNumberTable

mass_number_file_name = "snratio/data/mass_numbers/mass_number.txt"
solar_file_name = "snratio/data/solar/angr.txt"
Ia_file_name = "snratio/data/yields/Ia/iwamoto/Iwamoto_ApJ_1999_Table4.txt"
cc_file_name = "snratio/data/yields/cc/nomoto/2013/Nomoto_2013_all.txt"


class DataReading(unittest.TestCase):
    mass_number_table = MassNumberTable(mass_number_file_name)
    mass_number_table.read_data()

    def test_mass_number_table_column_order(self):
        '''Correct column order should be ["Elements", "MassNumber]"'''
        correct_columns = ["Element", "MassNumber"]

        read_result = self.mass_number_table.data.columns
        for i in range(len(correct_columns)):
            self.assertEqual(correct_columns[i], read_result[i])

    def test_mass_number_set_columns(self):
        test_columns = ["TestElement", "TestMassNumber"]
        self.mass_number_table.set_columns(test_columns)

        read_result = self.mass_number_table.data.columns
        for i in range(len(test_columns)):
            self.assertEqual(test_columns[i], read_result[i])


if __name__ == '__main__':
    unittest.main()
