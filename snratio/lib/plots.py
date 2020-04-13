from matplotlib.figure import Figure


class Plots:
    def __init__(self, table, ref_element, fit_results, chi_list, P_list, Ia_fraction_list):
        self.table = table
        self.ref_element = ref_element
        self.fit_results = fit_results
        self.chi_list = chi_list
        self.P_list = P_list
        self. Ia_fraction_list = Ia_fraction_list

    def get_likelihood_limits(self):
        P_axis_max = self.fit_results["P_max"] + (self.fit_results["P_max"] - self.fit_results["P_min"]) * 0.5
        P_axis_min = self.fit_results["P_max"] - (self.fit_results["P_max"] - self.fit_results["P_min"]) * 2.0

        ratio_axis_max = self.fit_results["best_Ia"] + self.fit_results["positive_error_Ia"] * 2.0
        ratio_axis_min = self.fit_results["best_Ia"] - self.fit_results["negative_error_Ia"] * 2.0

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

        ax.axhline(y=self.fit_results["P_max"], color="red")
        ax.axhline(y=self.fit_results["P_min"], color="red")

        ax.axvline(x=self.fit_results["best_Ia"], color="black",
                    label="Best fit values: {:.3f} (-{:.3f},+{:.3f})".format(self.fit_results["best_Ia"],
                                                                             self.fit_results["negative_error_Ia"],
                                                                             self.fit_results["positive_error_Ia"]))
        ax.axvline(x=self.fit_results["min_Ia"], color="black", ls="--")
        ax.axvline(x=self.fit_results["max_Ia"], color="black", ls="--")

        x_lim, y_lim = self.get_likelihood_limits()
        ax.set_xlim(*x_lim)
        ax.set_ylim(*y_lim)

        ax.legend()
        ax.set_title("Maximum Likelihood Estimation", fontsize=15)
        ax.grid(True)

        return fig

    def get_fit_plot(self):
        fig = Figure(dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = fig.add_subplot(111)

        contribution_Ia, contribution_cc = zip(*self.fit_results["best_fit_contribution"])
        err_min, err_max = self.fit_results["best_fit_min_contribution_sum"], self.fit_results[
            "best_fit_max_contribution_sum"]

        ax.errorbar(x=self.table["Element"], y=self.table["{}_normalised_abund".format(self.ref_element)],
                     yerr=self.table["{}_normalised_abund_err".format(self.ref_element)], fmt='.k', markersize='15',
                     elinewidth=2.5)
        ax.set_facecolor("lightgrey")

        ax.bar(self.table["Element"], contribution_Ia, 0.3, label="SNIa", color="blue",
                alpha=0.5)
        ax.bar(self.table["Element"], contribution_cc, 0.3, bottom=contribution_Ia, label="SNcc", color="green",
                alpha=0.5)
        ax.fill_between(self.table["Element"], err_min, err_max, facecolor="red", alpha=0.5,
                         label="{} confidence interval\nred_chi2 = {:.2f} ({:.2f}/{})".format(
                             self.fit_results["confidence"],
                             self.fit_results["reduced_chi_sq"],
                             self.fit_results["chi_min"],
                             self.fit_results["dof"]))

        ax.set_ylim(bottom=0)

        ax.set_xlabel("Elements", fontsize=15)
        ax.set_ylabel("[X/Fe]", fontsize=15)
        ax.set_title("Relative Abundances", fontsize=15)
        ax.legend(loc="upper left")
        ax.grid(True)

        return fig

