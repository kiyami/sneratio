from sneratio.src.lib import utils
import os


__all__ = [
    "path_dict", "get_path", "get_path_content", "get_keyword_content",
    "options_dict", "get_options", "get_option_count", "get_option_path", "get_option_index", "get_parsed_Ia_option", "get_parsed_cc_option",
    "selected_option_dict", "get_selected_option", "get_selected_option_path", "set_selected_option",
    "elements_dict", "results_dict", "plot_dict", "status_text", "loop_status"
]


path_dict = {
    "Ia_table": "sneratio/src/data/Ia_table",
    "cc_table": "sneratio/src/data/cc_table",

    "solar_table": "sneratio/src/data/solar_table",
    "mass_number_table": "sneratio/src/data/mass_number_table",

    "input_data": "sneratio/src/data/input_data",
}


def get_path(keyword):
    path = path_dict[keyword]
    package_path = utils.generate_package_path(path)

    return package_path


def get_path_content(path):
    content = os.listdir(path)
    filtered_content = [c for c in content if (not c.startswith("_")) and (not c.startswith("."))]
    filtered_content.sort()

    return filtered_content


def get_keyword_content(key):
    path = get_path(key)
    content = get_path_content(path)

    return content


options_dict = {
    "Ia_table": [],

    "cc_table": [],
    "cc_mass_range": ["10-50 Msun", "10-70 Msun"],
    # "cc_imf": ["Salpeter", "Top-Heavy"],
    "cc_imf": ["Salpeter"],

    "solar_table": ["aspl.txt", "angr.txt", "lodd.txt"],

    # "ref_element": ["Fe", "H"],
    "ref_element": ["Fe"],
    "sigma": ["1.0", "2.0"],

    "mass_number_table": ["mass_number.txt"],
    "input_data": ["test_data.txt"],
}


def get_options(key):
    return options_dict[key]


def get_option_count(key):
    return len(options_dict[key])


def get_option_path(key, index):
    if index > get_option_count(key):
        raise IndexError(f"Invalid index! Key:{key}, Index:{index}")

    option_name = get_options(key)[index]

    relative_path = get_path(key)
    root = utils.generate_package_path(relative_path)
    path = os.path.join(root, option_name)

    return path


def get_option_index(key, value):
    index = options_dict[key].index(value)
    return index


def get_parsed_Ia_option(option):
    without_suffix = option.rsplit(".", 1)[0]
    name, year, param = zip(*[c.split("_") for c in without_suffix])
    param = f"0.{param}"

    parsed_option = f"{name}({year}) {param}"

    return parsed_option


def get_parsed_cc_option(option):
    without_suffix = option.rsplit(".", 1)[0]
    name, year, param = zip(*[c.split("_") for c in without_suffix])
    param = f"0.{param}"

    parsed_option = f"{name}({year}) Z{param}"

    return parsed_option


def get_parsed_cc_mass_range_option(option):
    parsed = option.split(" ")[0]
    parsed = parsed.split("-")
    limits = [float(parsed[0]), float(parsed[1])]

    return limits


selected_option_dict = {
    "Ia_table": 0,

    "cc_table": 0,
    "cc_mass_range": 0,
    "cc_imf": 0,

    "solar_table": 0,

    "ref_element": 0,
    "sigma": 0,

    "input_data": 0,
    "mass_number_table": 0,
}


def get_selected_option(key):
    index = selected_option_dict[key]
    return options_dict[key][index]


def get_selected_option_index(key):
    return selected_option_dict[key]


def get_selected_option_path(key):
    selected_option_index = selected_option_dict[key]
    selected_option_path = get_option_path(key, selected_option_index)

    return selected_option_path


def set_selected_option(key, value):
    selected_option_dict[key] = value


elements_dict = {
    "element": [],
    "abund": [],
    "abund_err": [],
}


results_dict = {
    "fit_results": {
        "chi_squared": "",
        "dof": "",
        "ratio": "",
    },

    "fit_results_text": "",
    "ref_element_selected": False,
    "min_elements_selected": False,
}


plot_dict = {
    "fit_plot": None,
    "fit_loop_plot": None,
}


status_text = "Welcome to SNeRatio App.."

loop_status = "idle"
