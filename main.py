from sneratio_api import print_options, fit, fit_all


# to print the avalable options
# update the 'my_selections' part accordint to the printed options
# put a '#' at the beginning of the following line to disable the 'print_options' function.
print_options()


# update your selections
my_selections = {
    "abund_data": "data/test_data.txt",
    "solar_data": "aspl.txt",
    "mass_number_data": "mass_number.txt",
    "snIa_data": "Seitenzahl_2013_N40.txt",
    "sncc_data": "Nomoto_2013_0.02.txt",

    "imf": "salpeter",
    "sncc_mass_range": [10, 50],

    "ref_element": "Fe",
    "confidence": "1.0",
}


# to do a fit with your selections
# the fit results will be saved into the 'outputs' folder
# put a '#' at the beginning of the following line to disable the 'fit' function.
fit(my_selections)

# to do multiple fits with all of the available sn yield model combinations with your selections.
# the fit results will be saved into the 'outputs' folder
# put a '#' at the beginning of the following line to disable the 'fit_all' function.
#fit_all(my_selections)
