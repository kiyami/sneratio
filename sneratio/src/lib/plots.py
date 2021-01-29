from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib

from sneratio.src.lib.stats import Stats
from sneratio.src.lib.table import Data
from sneratio.src.lib import info


def get_fit_plot():
    fig = Figure(dpi=200, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    ax = fig.add_subplot(111)

    contribution_Ia = Stats.fit_results["Ia_contribution"]
    contribution_cc = Stats.fit_results["cc_contribution"]

    ref_element = Data.ref_element
    ref_row_index = Data.ref_row_index
    elements = Data.merged_table["Element"]
    norm_abund = Data.merged_table["Abund"]
    norm_abund_err = Data.merged_table["AbundError"]
    norm_abund_err[ref_row_index] = 0.0

    ax.errorbar(x=elements, y=norm_abund, yerr=norm_abund_err, fmt='.k', markersize='12', elinewidth=2.0)

    ax.bar(elements, contribution_Ia, 0.4, label="SNIa", color="blue", alpha=0.5)
    ax.bar(elements, contribution_cc, 0.4, bottom=contribution_Ia, label="SNcc", color="green", alpha=0.5)

    ax.set_ylim(bottom=0)

    # ax.set_xlabel("Elements", fontsize=16)
    ax.set_ylabel("[X/{}]".format(ref_element), fontsize=12)

    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=12)

    # ax.set_title("{} Normalised Relative Abundances".format(self.ref_element), fontsize=15)
    ax.legend(loc="upper left", fontsize=12)
    ax.grid(True)

    return fig


def get_fit_loop_plot():
    Ia_model_count = len(info.options_dict["Ia_table"])
    cc_model_count = len(info.options_dict["cc_table"])

    total_models = Ia_model_count * cc_model_count
    print("total_models", total_models)

    new_chi_list = Stats.fit_loop_results["chi_list"].reshape(Ia_model_count, cc_model_count)
    new_ratio_list = Stats.fit_loop_results["ratio_percent_list"].reshape(Ia_model_count, cc_model_count)
    new_ratio_error_n_list = Stats.fit_loop_results["ratio_percent_error_n_list"].reshape(Ia_model_count,
                                                                                          cc_model_count)
    new_ratio_error_p_list = Stats.fit_loop_results["ratio_percent_error_p_list"].reshape(Ia_model_count,
                                                                                          cc_model_count)


    fig = Figure(dpi=200, figsize=(10,10), facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    ax = [fig.add_subplot(141),
          fig.add_subplot(142),
          fig.add_subplot(143),
          fig.add_subplot(144)]

    fig.subplots_adjust(left=0.15,
                        bottom=0.175,
                        right=0.95,
                        top=0.95,
                        wspace=0.0,
                        hspace=0.0)

    xlabel = [t.rsplit(".", 1)[0] for t in info.options_dict["cc_table"]]
    ax[0].set_xticks(range(cc_model_count))
    ax[0].set_xticklabels(xlabel, rotation=80, size=5)

    ylabel = [t.rsplit(".", 1)[0] for t in info.options_dict["Ia_table"]]
    ax[0].set_yticks(range(Ia_model_count))
    ax[0].set_yticklabels(ylabel, size=5)

    ax[0].imshow(new_chi_list, cmap=matplotlib.cm.get_cmap('winter_r'))

    for i in range(len(xlabel)):
        for j in range(len(ylabel)):
            text = ax[0].text(i, j, "{:.2f}".format(new_chi_list[j, i]), ha="center", va="center",
                              color="black", fontsize=5)

    ax[0].set_title("Chi")

    xlabel = [t.rsplit(".", 1)[0] for t in info.options_dict["cc_table"]]
    ax[1].set_xticks(range(cc_model_count))
    ax[1].set_xticklabels(xlabel, rotation=80, size=5)

    ylabel = ["" for _ in info.options_dict["Ia_table"]]
    ax[1].set_yticks(range(Ia_model_count))
    ax[1].set_yticklabels(ylabel, size=5)

    ax[1].imshow(new_ratio_list, cmap=matplotlib.cm.get_cmap('autumn_r'))

    for i in range(len(xlabel)):
        for j in range(len(ylabel)):
            text = ax[1].text(i, j, "{:.2f}".format(new_ratio_list[j, i]), ha="center", va="center",
                              color="black", fontsize=5)

    ax[1].set_title("Ratio")

    xlabel = [t.rsplit(".", 1)[0] for t in info.options_dict["cc_table"]]
    ax[2].set_xticks(range(cc_model_count))
    ax[2].set_xticklabels(xlabel, rotation=80, size=5)

    ylabel = ["" for _ in info.options_dict["Ia_table"]]
    ax[2].set_yticks(range(Ia_model_count))
    ax[2].set_yticklabels(ylabel, size=5)

    ax[2].imshow(new_ratio_list, cmap=matplotlib.cm.get_cmap('summer_r'))

    for i in range(len(xlabel)):
        for j in range(len(ylabel)):
            text = ax[2].text(i, j, "{:.2f}".format(new_ratio_error_n_list[j, i]), ha="center", va="center",
                              color="black", fontsize=5)

    ax[2].set_title("(-)")

    xlabel = [t.rsplit(".", 1)[0] for t in info.options_dict["cc_table"]]
    ax[3].set_xticks(range(cc_model_count))
    ax[3].set_xticklabels(xlabel, rotation=80, size=5)

    ylabel = ["" for _ in info.options_dict["Ia_table"]]
    ax[3].set_yticks(range(Ia_model_count))
    ax[3].set_yticklabels(ylabel, size=5)

    ax[3].imshow(new_ratio_list, cmap=matplotlib.cm.get_cmap('summer_r'))

    for i in range(len(xlabel)):
        for j in range(len(ylabel)):
            text = ax[3].text(i, j, "{:.2f}".format(new_ratio_error_p_list[j, i]), ha="center", va="center",
                              color="black", fontsize=5)

    ax[3].set_title("(+)")

    return fig


def get_empty_plot():
    fig = Figure(dpi=200, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    #ax = fig.add_subplot(111)


    #ax.plot([0,1,2,3], [0,1,2,3])

    return fig