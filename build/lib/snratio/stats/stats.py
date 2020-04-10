import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class Stats:
    N = 1000
    sigma = 2.0

    def __init__(self, table, ref_element="Fe"):
        self.table = table
        self.Ia_column_name = "IaYields"
        self.cc_column_name = "CcYields"

        self.ref_element = ref_element

        self.chi_list = None
        self.P_list = None
        self.Ia_fraction_list = None
        self.cc_fraction_list = None

        self.fit_values = {}
        self.reduced_chi_sq = None
        self.best_chi_sq = None
        self.dof = None
        self.best_fit_values = ""

        self.fit_result_text = ""

    def function(self, fraction):
        a, b = fraction
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
        for i in self.table.index:
            c += ((contribution_list_sum[i] - self.table["{}_normalised_abund".format(self.ref_element)][i]) / self.table["{}_normalised_abund_err".format(self.ref_element)][i]) ** 2.0
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

        self.calculate_fit_values()
        self.set_fit_results()

    def calculate_fit_values(self):
        fit_values = {}
        sigma = self.sigma

        if sigma == 1.0:
            delta_P = 0.5
            delta_chi = 1.0
        elif sigma == 2.0:
            delta_P = 2.0
            delta_chi = 4.0
        else:
            delta_P = 2.0
            delta_chi = 4.0

        fit_values["precision"] = "{}%".format(100.0 / float(self.N))
        fit_values["confidence"] = "{:.1f} sigma".format(float(sigma))

        fit_values["chi_min"] = min(self.chi_list)
        fit_values["P_max"] = max(self.P_list)

        index = self.P_list.index(fit_values["P_max"])

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

        fit_values["min_cc"] = self.cc_fraction_list[index_min]
        fit_values["max_cc"] = self.cc_fraction_list[index_max]

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

        self.fit_values = fit_values

    def print_fit_values(self):
        for i, j in self.fit_values.items():
            print(i, j)

    @classmethod
    def set_iteration_number(cls, N):
        cls.N = N

    @classmethod
    def set_sigma(cls, sigma):
        cls.sigma = sigma

    def set_fit_results(self):
        self.best_chi_sq = self.fit_values['chi_min']
        self.dof = self.table["Element"].size - 2
        self.reduced_chi_sq = self.best_chi_sq / self.dof

        part1 = "reduced_chi_sq: {:.2f} ({:.2f}/{})".format(self.reduced_chi_sq, self.best_chi_sq, self.dof)
        part2 = "[SN Ia] / [SN Total] ratio = {:.4f} (-{:.4f},+{:.4f})".format(self.fit_values["best_Ia"],
                                                                               self.fit_values["negative_error_Ia"],
                                                                               self.fit_values["positive_error_Ia"])

        self.best_fit_values = "{}\n{}".format(part1, part2)

    def get_fit_results(self):
        part1 = "Reduced Chi Square: \n{:.2f} ({:.2f}/{})".format(self.reduced_chi_sq,
                                                                  self.best_chi_sq,
                                                                  self.dof)

        part2 = "SNIa Ratio: \n{:.1f} (-{:.1f},+{:.1f})".format(self.fit_values["best_Ia"],
                                                                self.fit_values["min_Ia"],
                                                                self.fit_values["max_Ia"])

        part3 = "SNcc Ratio: \n{:.1f} (-{:.1f},+{:.1f})".format(self.fit_values["best_cc"],
                                                                self.fit_values["min_cc"],
                                                                self.fit_values["max_cc"])

        result = "{}\n\n{}\n\n{}\n".format(part1, part2, part3)

        return result

    def print_fit_results(self):
        print(self.best_fit_values)

    def set_likelihood_limits(self):
        P_axis_max = self.fit_values["P_max"] + (self.fit_values["P_max"] - self.fit_values["P_min"]) * 0.5
        P_axis_min = self.fit_values["P_max"] - (self.fit_values["P_max"] - self.fit_values["P_min"]) * 2.0

        ratio_axis_max = self.fit_values["best_Ia"] + self.fit_values["positive_error_Ia"] * 2.0
        ratio_axis_min = self.fit_values["best_Ia"] - self.fit_values["negative_error_Ia"] * 2.0

        x_lim = [ratio_axis_min, ratio_axis_max]
        y_lim = [P_axis_min, P_axis_max]

        return x_lim, y_lim

    def get_chi_plot(self):
        min_chi = min(self.chi_list)

        fig = Figure(dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = fig.add_subplot(111)

        ax.plot(self.Ia_fraction_list, self.chi_list)
        ax.axhline(y=min_chi, color="red")

        return fig

    def get_likelihood_plot(self):
        fig = Figure(dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = fig.add_subplot(111)

        ax.plot(self.Ia_fraction_list, self.P_list, color="blue")
        ax.set_facecolor("lightgrey")
        ax.set_xlabel("Ratio (Ia / Total)")
        ax.set_ylabel("log Likelihood")

        ax.axhline(y=self.fit_values["P_max"], color="red")
        ax.axhline(y=self.fit_values["P_min"], color="red")

        ax.axvline(x=self.fit_values["best_Ia"], color="black",
                    label="Best fit values: {:.3f} (-{:.3f},+{:.3f})".format(self.fit_values["best_Ia"],
                                                                             self.fit_values["negative_error_Ia"],
                                                                             self.fit_values["positive_error_Ia"]))
        ax.axvline(x=self.fit_values["min_Ia"], color="black", ls="--")
        ax.axvline(x=self.fit_values["max_Ia"], color="black", ls="--")

        x_lim, y_lim = self.set_likelihood_limits()
        ax.set_xlim(*x_lim)
        ax.set_ylim(*y_lim)

        ax.legend()
        ax.set_title("Maximum Likelihood Estimation", fontsize=15)
        ax.grid(True)

        return fig

    def get_fit_plot(self):
        fig = Figure(dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = fig.add_subplot(111)

        contribution_Ia, contribution_Cc = zip(*self.fit_values["best_fit_contribution"])
        err_min, err_max = self.fit_values["best_fit_min_contribution_sum"], self.fit_values[
            "best_fit_max_contribution_sum"]

        ax.errorbar(x=self.table["Element"], y=self.table["{}_normalised_abund".format(self.ref_element)],
                     yerr=self.table["{}_normalised_abund_err".format(self.ref_element)], fmt='.k', markersize='15',
                     elinewidth=2.5)
        ax.set_facecolor("lightgrey")

        ax.bar(self.table["Element"], contribution_Ia, 0.3, label="SNIa", color="blue",
                alpha=0.5)
        ax.bar(self.table["Element"], contribution_Cc, 0.3, bottom=contribution_Ia, label="SNcc", color="green",
                alpha=0.5)
        ax.fill_between(self.table["Element"], err_min, err_max, facecolor="red", alpha=0.5,
                         label="{} confidence interval\nred_chi2 = {:.2f} ({:.2f}/{})".format(
                             self.fit_values["confidence"],
                             self.reduced_chi_sq,
                             self.best_chi_sq,
                             self.dof))

        ax.set_ylim(bottom=0)

        ax.set_xlabel("Elements", fontsize=15)
        ax.set_ylabel("[X/Fe]", fontsize=15)
        ax.set_title("Relative Abundances", fontsize=15)
        ax.legend(loc="upper left")
        ax.grid(True)

        return fig
