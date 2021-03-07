from sneratio.src.lib import info
from sneratio.src.lib.table import Data
from sneratio.src.lib.stats import Stats
from sneratio.src.lib import plots


class Methods:
    @staticmethod
    def initialise_options():
        info.options_dict["Ia_table"] = info.get_keyword_content("Ia_table")
        info.options_dict["cc_table"] = info.get_keyword_content("cc_table")

    @staticmethod
    def get_data_field():
        data_field = {
            "options": info.options_dict,
            "selections": info.selected_option_dict,
            "elements": info.elements_dict,
            "results": info.results_dict,
            "loop_status": info.loop_status,
        }

        return data_field

    @staticmethod
    def update_data_field(data_field):
        info.options_dict = data_field["options"]
        info.selected_option_dict = data_field["selections"]
        info.elements_dict = data_field["elements"]
        info.results_dict = {
            "fit_results": {
                "chi_squared": "",
                "dof": "",
                "ratio": "",
            },

            "fit_results_text": "",
            "ref_element_selected": False,
            "min_elements_selected": False,
        }
        #info.loop_status = data_field["loop_status"]

    @staticmethod
    def fit():
        Data.read_Ia_table()
        Data.read_cc_table()
        Data.read_solar_table()
        Data.read_mass_number_table()
        Data.set_input_data()

        Data.set_elements_from_input_data()
        Data.set_ref_element()
        Data.set_ref_row_index()

        Data.initialise_merged_table()
        Data.normalise_input_data()
        Data.normalise_solar_table()

        Data.set_Ia_yields()
        Data.set_cc_yields()

        Data.set_mass_numbers()

        Stats.fit()

        info.results_dict["fit_results"] = Stats.get_fit_results()
        info.results_dict["fit_results_text"] = Stats.get_fit_results_text()
        info.plot_dict["fit_plot"] = plots.get_fit_plot()

    @staticmethod
    def fit_loop():
        Data.read_solar_table()
        Data.read_mass_number_table()
        Data.set_input_data()

        Data.set_elements_from_input_data()
        Data.set_ref_element()
        Data.set_ref_row_index()

        Data.initialise_merged_table()
        Data.normalise_input_data()
        Data.normalise_solar_table()

        Data.set_mass_numbers()

        Stats.fit_loop()

        info.results_dict["fit_results"] = Stats.get_fit_loop_results()
        info.results_dict["fit_results_text"] = Stats.get_fit_loop_results_text()
        info.plot_dict["fit_loop_plot"] = plots.get_fit_loop_plot()

    @staticmethod
    def get_fit_plot():
        return info.plot_dict["fit_plot"]

    @staticmethod
    def get_fit_loop_plot():
        return info.plot_dict["fit_loop_plot"]

    @staticmethod
    def get_empty_plot():
        return plots.get_empty_plot()

    @staticmethod
    def get_status_text():
        return info.status_text

    @staticmethod
    def set_status_text(new_text):
        info.status_text = new_text

    @staticmethod
    def get_fit_results():
        return Stats.get_fit_results()

    @staticmethod
    def get_fit_loop_results():
        return Stats.get_fit_loop_results()

    @staticmethod
    def get_loop_status():
        return info.loop_status

    @staticmethod
    def set_loop_status(status):
        info.loop_status = status
