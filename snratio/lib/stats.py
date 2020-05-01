import numpy as np

class Stats:
    def __init__(self, table, ref_element, sigma):
        self.N = 1000
        self.sigma = sigma

        self.table = table
        self.Ia_column_name = "IaYields"
        self.cc_column_name = "CcYields"
        self.ref_element = ref_element

        self.chi_list = None
        self.P_list = None
        self.Ia_fraction_list = None
        self.cc_fraction_list = None

        self.fit_results = {}
        self.fit_results_text = ""

    def function(self, fraction):
        a, b = fraction
        if self.ref_element == "H":
            ref_index = None
        else:
            ref_index = self.table[self.table.Element == self.ref_element].index[0]

        contribution_list = []
        for i in self.table.index:
            arg1_Ia = a * self.table[self.Ia_column_name][i]
            arg1_cc = b * self.table[self.cc_column_name][i]
            arg2 = a * self.table[self.Ia_column_name][ref_index] + b * self.table[self.cc_column_name][ref_index]
            arg3 = 1.0 / self.table["{}_normalised_solar".format(self.ref_element)][i]
            arg4 = self.table["MassNumber"][ref_index] / self.table["MassNumber"][i]
            contribution = ((arg1_Ia / arg2) * arg3 * arg4, (arg1_cc / arg2) * arg3 * arg4)
            contribution_list.append(contribution)
        return contribution_list

    def chi2(self, fraction):
        contribution_list = self.function(fraction)
        contribution_list_sum = [sum(i) for i in contribution_list]
        c = 0.0

        norm_abund_col = self.table["{}_normalised_abund".format(self.ref_element)]
        norm_abund_err_col = self.table["{}_normalised_abund_err".format(self.ref_element)]

        for i in self.table.index:
            c += ((contribution_list_sum[i] - norm_abund_col[i]) / norm_abund_err_col[i]) ** 2.0
        return c

    def P(self, fraction):
        return -0.5 * self.chi2(fraction)

    def fit(self):
        chi_list = []
        P_list = []

        Ia_fraction_list = np.linspace(0.0, 1.0, int(self.N + 1))
        cc_fraction_list = np.linspace(1.0, 0.0, int(self.N + 1))

        for fraction in zip(Ia_fraction_list, cc_fraction_list):
            chi_list.append(self.chi2(fraction))
            P_list.append(self.P(fraction))
        print("fit done!")

        self.chi_list = chi_list
        self.P_list = P_list
        self.Ia_fraction_list = Ia_fraction_list
        self.cc_fraction_list = cc_fraction_list

        self.calculate_fit_results()
        self.set_fit_results_text()

    def calculate_fit_results(self):
        fit_values = {}
        sigma = float(self.sigma)

        if sigma == 1.0:
            delta_P = 0.5
            delta_chi = 1.0
        elif sigma == 2.0:
            delta_P = 2.0
            delta_chi = 4.0
        else:
            raise ValueError("Invalid sigma value!")

        fit_values["precision"] = "{}%".format(100.0 / float(self.N))
        fit_values["confidence"] = "{:.1f} sigma".format(float(sigma))

        fit_values["chi_min"] = min(self.chi_list)
        fit_values["P_max"] = max(self.P_list)

        index = self.P_list.index(fit_values["P_max"])

        # if ratio is too close to zero, the index becomes also zero.
        # but index should be greater than index_min.
        # if index is zero, set it to 1
        if index == 0:
            index = 1

        fit_values["best_Ia"] = self.Ia_fraction_list[index]
        fit_values["best_cc"] = self.cc_fraction_list[index]

        fit_values["P_min"] = fit_values["P_max"] - delta_P
        fit_values["chi_max"] = fit_values["chi_min"] + delta_chi

        diff_list_P = [abs(i - fit_values["P_min"]) for i in self.P_list]

        index_min = diff_list_P.index(min(diff_list_P[:index]))
        index_max = diff_list_P.index(min(diff_list_P[index:]))

        fit_values["min_Ia"] = self.Ia_fraction_list[index_min]
        fit_values["max_Ia"] = self.Ia_fraction_list[index_max]

        fit_values["negative_error_Ia"] = abs(fit_values["best_Ia"] - fit_values["min_Ia"])
        fit_values["positive_error_Ia"] = abs(fit_values["best_Ia"] - fit_values["max_Ia"])

        fit_values["min_cc"] = self.cc_fraction_list[index_max]
        fit_values["max_cc"] = self.cc_fraction_list[index_min]

        fit_values["negative_error_cc"] = abs(fit_values["best_cc"] - fit_values["min_cc"])
        fit_values["positive_error_cc"] = abs(fit_values["best_cc"] - fit_values["max_cc"])

        best_fit_ratios = [fit_values["best_Ia"], fit_values["best_cc"]]
        fit_values["best_fit_contribution"] = self.function(best_fit_ratios)
        fit_values["best_fit_contribution_sum"] = [sum(i) for i in fit_values["best_fit_contribution"]]

        best_fit_min_ratios = [fit_values["min_Ia"], fit_values["min_cc"]]
        fit_values["best_fit_min_contribution"] = self.function(best_fit_min_ratios)
        fit_values["best_fit_min_contribution_sum"] = [sum(i) for i in fit_values["best_fit_min_contribution"]]

        best_fit_max_ratios = [fit_values["max_Ia"], fit_values["max_cc"]]
        fit_values["best_fit_max_contribution"] = self.function(best_fit_max_ratios)
        fit_values["best_fit_max_contribution_sum"] = [sum(i) for i in fit_values["best_fit_max_contribution"]]

        fit_values["dof"] = self.table["Element"].size - 2
        fit_values["reduced_chi_sq"] = fit_values["chi_min"] / fit_values["dof"]

        self.fit_results = fit_values

    def set_fit_results_text(self):
        part1 = "Reduced Chi Square: \n{:.2f} ({:.2f}/{})".format(self.fit_results["reduced_chi_sq"],
                                                                  self.fit_results["chi_min"],
                                                                  self.fit_results["dof"])

        part2 = "SNIa Ratio: \n{:.1f}% (-{:.1f},+{:.1f})".format(self.fit_results["best_Ia"] * 100,
                                                                 self.fit_results["negative_error_Ia"] * 100,
                                                                 self.fit_results["positive_error_Ia"] * 100)

        part3 = "SNcc Ratio: \n{:.1f}% (-{:.1f},+{:.1f})".format(self.fit_results["best_cc"] * 100,
                                                                 self.fit_results["negative_error_cc"] * 100,
                                                                 self.fit_results["positive_error_cc"] * 100)

        self.fit_results_text = "--------------------\n# Fit Results \n--------------------\n{}\n\n{}\n\n{}\n--------------------".format(
            part1, part2, part3)

    def get_fit_results_text(self):
        return self.fit_results_text
