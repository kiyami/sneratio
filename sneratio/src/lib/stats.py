import numpy as np
from scipy.optimize import leastsq

from sneratio.src.lib.table import Data
from sneratio.src.lib import info
from sneratio.src.lib import utils


class Stats:
    Ia_model = None
    cc_model = None
    input_data = None

    ref_index = None
    solar_data = None
    mass_number_data = None

    merged_table = None
    initial_ratio_value = 0.3

    fit_results = {
        "chi_squared": None,
        "dof": None,

        "Ia_contribution": [],
        "cc_contribution": [],
        "total_contribution": [],

        "ratio": None,
        "ratio_error_n": None,
        "ratio_error_p": None,

        "ratio_percent": None,
        "ratio_percent_error_n": None,
        "ratio_percent_error_p": None,
    }

    fit_loop_results = {
        "chi_squared": None,
        "ratio": None,
        "ratio_percent": None,
        "ratio_percent_error_n": None,
        "ratio_percent_error_p": None,

        "best_Ia_index": None,
        "best_cc_index": None,

        "best_Ia_model": None,
        "best_cc_model": None,

        "chi_min": None,
        "chi_max": None,
        "ratio_percent_min": None,
        "ratio_percent_max": None,

        "chi_list": None,
        "ratio_list": None,
        "ratio_percent_error_n_list": None,
        "ratio_percent_error_p_list": None,
        "ratio_percent_list": None,
        "model_index_list": None,
    }

    @staticmethod
    def calc_contributions(ratio):
        ratio_percent = ratio / (1.0 + ratio)
        ref_index = Data.ref_row_index

        y_Ia = Data.merged_table["Ia_yields"] * ratio_percent
        y_cc = Data.merged_table["cc_yields"] * (1.0 - ratio_percent)

        y_Ia_ref = Data.merged_table["Ia_yields"][ref_index] * ratio_percent
        y_cc_ref = Data.merged_table["cc_yields"][ref_index] * (1.0 - ratio_percent)

        mref_mx = Data.merged_table["MassNumber"][ref_index] / Data.merged_table["MassNumber"]
        solar = Data.merged_table["Solar"]

        cont_Ia = (y_Ia / (y_Ia_ref + y_cc_ref)) * (mref_mx / solar)
        cont_cc = (y_cc / (y_Ia_ref + y_cc_ref)) * (mref_mx / solar)

        total_cont = cont_Ia + cont_cc

        return (total_cont, cont_Ia, cont_cc)

    @staticmethod
    def chi_squared(ratio):
        total_cont, cont_Ia, cont_cc = Stats.calc_contributions(ratio)

        chi = (Data.merged_table["Abund"] - total_cont) / Data.merged_table["AbundError"]
        chi_sq = np.array([i ** 2.0 for i in chi])
        chi_sq_sum = chi_sq.sum()

        return chi_sq_sum

    @staticmethod
    def chi_squared_interval(ratio, chi, delta_chi):
        target_chi = abs(Stats.chi_squared(ratio) - chi - delta_chi)
        return target_chi

    @staticmethod
    def find_interval(ratio, chi, delta_chi):
        init_positive = ratio * 2.0
        result_positive = leastsq(Stats.chi_squared_interval, np.array([init_positive]), args=(chi, delta_chi))
        ratio_max = result_positive[0][0]

        init_negative = ratio / 2.0
        result_negative = leastsq(Stats.chi_squared_interval, np.array([init_negative]), args=(chi, delta_chi))
        ratio_min = result_negative[0][0]

        return (ratio_min, ratio_max)

    @staticmethod
    def fit():
        result = leastsq(Stats.chi_squared, np.array([Stats.initial_ratio_value]))
        best_ratio = result[0][0]
        best_ratio_percent = best_ratio / (1.0 + best_ratio)

        total_cont, cont_Ia, cont_cc = Stats.calc_contributions(best_ratio)

        best_chi_squared = Stats.chi_squared(best_ratio)

        sigma = info.get_selected_option("sigma")
        delta_chi = utils.get_chi_interval_value(sigma)

        ratio_min, ratio_max = Stats.find_interval(best_ratio, best_chi_squared, delta_chi)
        ratio_min_percent = ratio_min / (1.0 + ratio_min)
        ratio_max_percent = ratio_max / (1.0 + ratio_max)

        Stats.fit_results["chi_squared"] = best_chi_squared
        Stats.fit_results["dof"] = len(Data.elements) - 2

        Stats.fit_results["Ia_contribution"] = list(cont_Ia.values)
        Stats.fit_results["cc_contribution"] = list(cont_cc.values)
        Stats.fit_results["total_contribution"] = list(total_cont.values)

        Stats.fit_results["ratio"] = best_ratio
        Stats.fit_results["ratio_error_n"] = best_ratio - ratio_min
        Stats.fit_results["ratio_error_p"] = ratio_max - best_ratio

        Stats.fit_results["ratio_percent"] = best_ratio_percent
        Stats.fit_results["ratio_percent_error_n"] = best_ratio_percent - ratio_min_percent
        Stats.fit_results["ratio_percent_error_p"] = ratio_max_percent - best_ratio_percent

        return best_chi_squared

    @staticmethod
    def _fit_for_loop():
        result = leastsq(Stats.chi_squared, np.array([Stats.initial_ratio_value]))
        best_ratio = result[0][0]

        best_chi_squared = Stats.chi_squared(best_ratio)

        sigma = info.get_selected_option("sigma")
        delta_chi = utils.get_chi_interval_value(sigma)

        best_ratio_min, best_ratio_max = Stats.find_interval(best_ratio, best_chi_squared, delta_chi)

        return best_chi_squared, best_ratio, best_ratio_min, best_ratio_max

    @staticmethod
    def fit_loop(chi_min = None, chi_max = None, ratio_percent_min = None, ratio_percent_max = None):
        Ia_model_count = len(info.options_dict["Ia_table"])
        cc_model_count = len(info.options_dict["cc_table"])

        total_model_count = Ia_model_count * cc_model_count
        print("total_model_count", total_model_count)

        chi_list = np.zeros(total_model_count)
        ratio_list = np.zeros(total_model_count)
        ratio_percent_list = np.zeros(total_model_count)
        ratio_percent_error_n_list = np.zeros(total_model_count)
        ratio_percent_error_p_list = np.zeros(total_model_count)
        model_index_list = np.array(range(total_model_count))

        for i in range(Ia_model_count):
            for j in range(cc_model_count):
                info.results_dict["fit_loop_progress_percent"] = "{}".format(int(((i+1)*(j+1) / total_model_count) * 100))

                info.set_selected_option("Ia_table", i)
                info.set_selected_option("cc_table", j)

                Data.read_Ia_table()
                Data.read_cc_table()

                Data.set_Ia_yields()
                Data.set_cc_yields()

                index = i * cc_model_count + j
                best_chi_squared, best_ratio, best_ratio_min, best_ratio_max = Stats._fit_for_loop()

                chi_list[index] = best_chi_squared
                ratio_list[index] = best_ratio

                best_ratio_percent = best_ratio / (1.0 + best_ratio)
                ratio_percent_list[index] = best_ratio_percent

                best_ratio_min_percent = best_ratio_min / (1.0 + best_ratio_min)
                ratio_percent_error_n = best_ratio_percent - best_ratio_min_percent
                ratio_percent_error_n_list[index] = ratio_percent_error_n

                best_ratio_max_percent = best_ratio_max / (1.0 + best_ratio_max)
                ratio_percent_error_p = best_ratio_max_percent - best_ratio_percent
                ratio_percent_error_p_list[index] = ratio_percent_error_p

                print("index: {}, i: {}, j: {} chisq: {:.3f}, ratio: {:.3f}, ratio_Ia: {:.3f} (-{:.3f},+{:.3f})".format(index, info.get_selected_option("Ia_table"), info.get_selected_option("cc_table"),
                                                                                                                        best_chi_squared,
                                                                                                                        best_ratio,
                                                                                                                        best_ratio_percent,
                                                                                                                        ratio_percent_error_n,
                                                                                                                        ratio_percent_error_p))

        filt_chi_list = chi_list
        filt_ratio_list = ratio_list
        filt_ratio_percent_list = ratio_percent_list
        filt_best_ratio_percent_error_n_list = ratio_percent_error_n_list
        filt_best_ratio_percent_error_p_list = ratio_percent_error_p_list
        filt_model_index_list = model_index_list

        if chi_min is not None:
            filt_indexes = np.where(chi_list >= chi_min)
            filt_chi_list = filt_chi_list[filt_indexes]
            filt_ratio_list = filt_ratio_list[filt_indexes]
            filt_ratio_percent_list = filt_ratio_percent_list[filt_indexes]
            filt_best_ratio_percent_error_n_list = filt_best_ratio_percent_error_n_list[filt_indexes]
            filt_best_ratio_percent_error_p_list = filt_best_ratio_percent_error_p_list[filt_indexes]
            filt_model_index_list = filt_model_index_list[filt_indexes]

        if chi_max is not None:
            filt_indexes = np.where(chi_list <= chi_max)
            filt_chi_list = filt_chi_list[filt_indexes]
            filt_ratio_list = filt_ratio_list[filt_indexes]
            filt_ratio_percent_list = filt_ratio_percent_list[filt_indexes]
            filt_best_ratio_percent_error_n_list = filt_best_ratio_percent_error_n_list[filt_indexes]
            filt_best_ratio_percent_error_p_list = filt_best_ratio_percent_error_p_list[filt_indexes]
            filt_model_index_list = filt_model_index_list[filt_indexes]

        if ratio_percent_min is not None:
            filt_indexes = np.where(ratio_percent_list >= ratio_percent_min)
            filt_chi_list = filt_chi_list[filt_indexes]
            filt_ratio_list = filt_ratio_list[filt_indexes]
            filt_ratio_percent_list = filt_ratio_percent_list[filt_indexes]
            filt_best_ratio_percent_error_n_list = filt_best_ratio_percent_error_n_list[filt_indexes]
            filt_best_ratio_percent_error_p_list = filt_best_ratio_percent_error_p_list[filt_indexes]
            filt_model_index_list = filt_model_index_list[filt_indexes]

        if ratio_percent_max is not None:
            filt_indexes = np.where(ratio_percent_list <= ratio_percent_max)
            filt_chi_list = filt_chi_list[filt_indexes]
            filt_ratio_list = filt_ratio_list[filt_indexes]
            filt_ratio_percent_list = filt_ratio_percent_list[filt_indexes]
            filt_best_ratio_percent_error_n_list = filt_best_ratio_percent_error_n_list[filt_indexes]
            filt_best_ratio_percent_error_p_list = filt_best_ratio_percent_error_p_list[filt_indexes]
            filt_model_index_list = filt_model_index_list[filt_indexes]

        best_chi = filt_chi_list.min()
        best_chi_index = np.where(filt_chi_list == best_chi)

        best_ratio = filt_ratio_list[best_chi_index][0]
        best_ratio_percent = filt_ratio_percent_list[best_chi_index][0]
        best_ratio_percent_error_n = filt_best_ratio_percent_error_n_list[best_chi_index][0]
        best_ratio_percent_error_p = filt_best_ratio_percent_error_p_list[best_chi_index][0]
        best_model_index = filt_model_index_list[best_chi_index][0]

        best_Ia_index = best_model_index // cc_model_count
        best_cc_index = best_model_index % cc_model_count

        Stats.fit_loop_results["chi_squared"] = best_chi
        Stats.fit_loop_results["ratio"] = best_ratio
        Stats.fit_loop_results["ratio_percent"] = best_ratio_percent
        Stats.fit_loop_results["ratio_percent_error_n"] = best_ratio_percent_error_n
        Stats.fit_loop_results["ratio_percent_error_p"] = best_ratio_percent_error_p

        Stats.fit_loop_results["best_Ia_index"] = best_Ia_index
        Stats.fit_loop_results["best_cc_index"] = best_cc_index

        Stats.fit_loop_results["best_Ia_model"] = info.options_dict["Ia_table"][best_Ia_index]
        Stats.fit_loop_results["best_cc_model"] = info.options_dict["cc_table"][best_cc_index]

        Stats.fit_loop_results["chi_min"] = chi_min
        Stats.fit_loop_results["chi_max"] = chi_max
        Stats.fit_loop_results["ratio_percent_min"] = ratio_percent_min
        Stats.fit_loop_results["ratio_percent_max"] = ratio_percent_max

        Stats.fit_loop_results["chi_list"] = filt_chi_list
        Stats.fit_loop_results["ratio_list"] = filt_ratio_list
        Stats.fit_loop_results["ratio_percent_list"] = filt_ratio_percent_list
        Stats.fit_loop_results["ratio_percent_error_n_list"] = ratio_percent_error_n_list
        Stats.fit_loop_results["ratio_percent_error_p_list"] = ratio_percent_error_p_list
        Stats.fit_loop_results["model_index_list"] = filt_model_index_list

    @classmethod
    def get_fit_results(cls):
        _fit_results = {
            "chi_squared": "",
            "dof": "",
            "ratio": "",
        }

        try:
            _fit_results["chi_squared"] = "{:.2f}".format(cls.fit_results["chi_squared"])
            _fit_results["dof"] = cls.fit_results["dof"]
            _fit_results["ratio"] = "{:.1f} (-{:.1f},+{:.1f})".format(100 * cls.fit_results["ratio_percent"],
                                                                      100 * cls.fit_results["ratio_percent_error_n"],
                                                                      100 * cls.fit_results["ratio_percent_error_p"],)
        except:
            pass

        return _fit_results

    @classmethod
    def get_fit_results_text(cls):
        text_Ia_model = "SNIa Model: {}".format(info.get_selected_option("Ia_table").rsplit(".",1)[0])
        text_cc_model = "SNcc Model: {}".format(info.get_selected_option("cc_table").rsplit(".",1)[0])
        text_solar_table = "Solar Table: {}".format(info.get_selected_option("solar_table").rsplit(".",1)[0])

        text1 = "Chi-Squared: {:.3f}".format(cls.fit_results["chi_squared"])
        text2 = "Dof: {:.3f}".format(cls.fit_results["dof"])

        text3 = "Elements: {}".format(" ".join(Data.elements))

        Ia_contribution = ["{:.3f}".format(Ia) for Ia in cls.fit_results["Ia_contribution"]]
        text4 = "Ia-Contributions: {}".format(Ia_contribution)

        cc_contribution = ["{:.3f}".format(cc) for cc in cls.fit_results["cc_contribution"]]
        text5 = "cc-Contributions: {}".format(cc_contribution)

        total_contribution = ["{:.3f}".format(t) for t in cls.fit_results["total_contribution"]]
        text6 = "Total-Contributions: {}".format(total_contribution)

        text7 = "Ratio (Ia/cc): {:.3f} (-{:.3f},+{:.3f})".format(cls.fit_results["ratio"],
                                                                 cls.fit_results["ratio_error_n"],
                                                                 cls.fit_results["ratio_error_p"])

        text8 = "Ratio % (Ia/Total): {:.3f} (-{:.3f},+{:.3f})".format(cls.fit_results["ratio_percent"],
                                                                 cls.fit_results["ratio_percent_error_n"],
                                                                 cls.fit_results["ratio_percent_error_p"])

        text9 = "Confidence: {} sigma".format(info.get_selected_option("sigma"))

        result_text = "\n".join([text_Ia_model, text_cc_model, text_solar_table, " ", text1, text2, " ", text3, text4, text5, text6, " ", text7, text8, text9])

        return result_text

    @classmethod
    def get_fit_loop_results(cls):
        _fit_results = {
            "chi_squared": "",
            "dof": "",
            "ratio": "",
        }

        return _fit_results

    @classmethod
    def get_fit_loop_results_text(cls):
        """
        print("\n----- Fit Loop Results ----------------------")
        print("chi_squared", cls.fit_loop_results["chi_squared"])
        print("ratio", cls.fit_loop_results["ratio"])
        print("Ratio % (Ia/Total): {:.3f} (-{:.3f},+{:.3f})".format(cls.fit_loop_results["ratio_percent"],
                                                                    cls.fit_loop_results["ratio_percent_error_n"],
                                                                    cls.fit_loop_results["ratio_percent_error_p"]))

        print("best_Ia_index", cls.fit_loop_results["best_Ia_index"])
        print("best_cc_index", cls.fit_loop_results["best_cc_index"])

        print("best_Ia_model", cls.fit_loop_results["best_Ia_model"])
        print("best_cc_model", cls.fit_loop_results["best_cc_model"])

        print("chi_min", cls.fit_loop_results["chi_min"])
        print("chi_max", cls.fit_loop_results["chi_max"])
        print("ratio_percent_min", cls.fit_loop_results["ratio_percent_min"])
        print("ratio_percent_max", cls.fit_loop_results["ratio_percent_max"])
        """

        result_text = "\n".join(["{}:\n{}".format(k,v) for k,v in cls.fit_loop_results.items()])

        return result_text