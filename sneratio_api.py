import pandas as pd
import numpy as np

from scipy import interpolate
from scipy.integrate import trapezoid
from scipy.optimize import least_squares, curve_fit

import matplotlib.pyplot as plt

import datetime
import json
from json import JSONEncoder
import os
import time

# SNeRatio class --------------------------------------------

class SNeRatio:
    
    df_master = None

    df_solar = None
    df_mass = None
    
    df_Ia = None
    df_cc = None

    elements = None
        
    default_selections = {
        "abund_data": "test_data.txt",
        "solar_data": "aspl.txt",
        "mass_number_data": "mass_number.txt",
        "snIa_data": "Seitenzahl_2013_N40.txt",
        "sncc_data": "Nomoto_2013_0.02.txt",

        "imf": "salpeter",
        "sncc_mass_range": [10.0, 50.0],
        "ref_element": "Fe",
        "confidence": "1.0",
    }

    _paths = {
        "abund_data": "data",
        "solar_data": "data/solar",
        "mass_number_data": "data",
        "snIa_data": "data/snIa",
        "sncc_data": "data/sncc",
    }

    options = {
        "abund_data": ["test_data.txt"],
        "solar_data": os.listdir(_paths["solar_data"]),
        "mass_number_data": ["mass_number.txt"],
        "snIa_data": os.listdir(_paths["snIa_data"]),
        "sncc_data": os.listdir(_paths["sncc_data"]),
        "ref_element": ["Fe"],
    }
    
    selections = default_selections
    
    imf_dict = {
        "salpeter": lambda m: m**(-2.35),
        "top_heavy": None
    }

    sigma_to_delta_chisq = {
        "1.0": 1.0,
        "2.0": 4.0,
        "3.0": 9.0,
    }

    @classmethod
    def print_options(cls):
        print("\nSNeRatio OPTIONS:\n")
        for key,values in cls.options.items():
            print(f"-{key}:")

            for i,value in enumerate(values):
                print(f"\t{i+1}) {value}")

            print("")

        print("-imf's:")

        for i,value in enumerate(cls.imf_dict.keys()):
            print(f"\t{i+1}) {value}")

        print("")

        print("-confidence intervals:")

        for i,value in enumerate(cls.sigma_to_delta_chisq.keys()):
            print(f"\t{i+1}) {value} sigma")

        print("")

    @classmethod
    def get_file_path(cls, key):
        file_path = cls._paths[key]
        data_file = cls.selections[key]

        return os.path.join(file_path, data_file)
    
    @classmethod
    def set_selections(cls, selections):
        for key, value in selections.items():
            cls.selections[key] = value

    @classmethod
    def set_a_selection(cls, key, value):
        cls.selections[key] = value
    
    @staticmethod
    def read_data(filename):
        df = pd.read_csv(filename, sep="\s+")
        
        # fixing column name duplications. it happens with Nomoto_2013_0.0.txt
        dup_list = [col for col in df.columns if len(col.split("."))>2]
        if len(dup_list) > 0:
            for dup_name in dup_list:
                old_name = dup_name
                new_name = dup_name.rsplit(".",1)[0] + "01"
                df.rename(columns={old_name: new_name}, inplace=True)

        return df
    
    @classmethod
    def read_all(cls):
        # abund_data is taken as a path from the user, the others are not.
        abund_path = cls.selections["abund_data"]
        cls.df_master = cls.read_data(abund_path)

        solar_path = cls.get_file_path("solar_data")
        cls.df_solar = cls.read_data(solar_path)

        mass_number_path = cls.get_file_path("mass_number_data")
        cls.df_mass = cls.read_data(mass_number_path)

        snIa_path = cls.get_file_path("snIa_data")
        cls.df_Ia = cls.read_data(snIa_path)

        sncc_path = cls.get_file_path("sncc_data")
        cls.df_cc = cls.read_data(sncc_path)

        cls.elements = cls.df_master.Element.values
    
    @staticmethod
    def division_error(x, x_err, y, y_err):
        x = float(x)
        x_err = float(x_err)
        y = float(y)
        y_err = float(y_err)

        z = x/y
        z_err = z * ((x_err / x) ** 2.0 + (y_err / y) ** 2.0) ** 0.5

        return z, z_err
    
    @staticmethod
    def _calc_snIa_yields(df_Ia, elements):
        Ia_yields = []

        for e in elements:
            y = df_Ia[df_Ia.Element == e][[df_Ia.columns[2]]].sum().values[0]
            Ia_yields.append(y)

        return Ia_yields
    
    @staticmethod
    def _calc_sncc_yields(df_cc, elements, imf, mass_range):
        
        cc_yields = []
        mass_min, mass_max = mass_range

        x = df_cc.columns[2:].astype(float)
        for e in elements:
            y = df_cc[df_cc.Element == e][df_cc.columns[2:]].sum().values
            
            m_range = np.linspace(mass_min, mass_max, 1000)
            imf_range = imf(m_range)
            f = interpolate.interp1d(x, y, fill_value='extrapolate')
            f_range = f(m_range)

            q = trapezoid(f_range * imf_range, m_range)
            w = trapezoid(imf_range, m_range)

            integrated_yields = q/w

            cc_yields.append(integrated_yields)

        return cc_yields

    @classmethod
    def set_snIa_yields(cls):

        elements = cls.elements
        
        Ia_yields = cls._calc_snIa_yields(cls.df_Ia, elements)

        cls.df_master["Ia_yields"] = Ia_yields
        
    @classmethod
    def set_sncc_yields(cls):

        elements = cls.elements
        imf = cls.imf_dict[cls.selections["imf"]]
        mass_range = cls.selections["sncc_mass_range"]

        cc_yields = cls._calc_sncc_yields(cls.df_cc, elements, imf, mass_range)
            
        cls.df_master["cc_yields"] = cc_yields
                
    @classmethod
    def set_solar(cls):
        cls.df_master["Solar"] = cls.df_solar[cls.df_solar.Element.isin(cls.elements)].Solar.values
        
    @classmethod
    def set_mass_number(cls):
        cls.df_master["MassNumber"] = cls.df_mass[cls.df_mass.Element.isin(cls.elements)].MassNumber.values

    @classmethod
    def set_normalisations(cls):
        ref_row = cls.df_master.Element == cls.selections["ref_element"]
        cls.df_master[ref_row]


        norm_abund = cls.df_master.Abund.values / cls.df_master[ref_row].Abund.values
        cls.df_master["norm_abund"] = norm_abund


        ref_abund = cls.df_master[ref_row].Abund
        ref_abund_err = cls.df_master[ref_row].AbundError

        _, norm_abund_err = zip(*[cls.division_error(cls.df_master.Abund.values[i], cls.df_master.AbundError.values[i], ref_abund, ref_abund_err) for i in range(len(cls.elements))])
        cls.df_master["norm_abund_err"] = norm_abund_err


        ref_solar = cls.df_master[ref_row].Solar

        norm_solar = cls.df_master.Solar.apply(lambda x: 10**(x-ref_solar))
        cls.df_master["norm_solar"] = norm_solar


# SNeStats class --------------------------------------------

class SNeStats:
    
    fit_results = None
    fit_results_all = None
    fit_results_all_df = None

    @staticmethod
    def _ratio2percent(r):

        r_Ia = r / (1.0+r)
        r_cc = 1.0 / (1.0+r)
        
        return r_Ia, r_cc
    
    @staticmethod
    def _percent2ratio(r_Ia, r_cc):
        return r_Ia/r_cc
    
    @staticmethod
    def _calc_contribution(r_Ia, r_cc, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element):
        
        x = range(len(elements))
        
        ref_index = elements == ref_element
        
        y_Ia = Ia_yields * r_Ia
        y_cc = cc_yields * r_cc
        
        y_Ia_ref = Ia_yields[ref_index] * r_Ia
        y_cc_ref = cc_yields[ref_index] * r_cc
        
        mref_mx = mass_number[ref_index] / mass_number[x]
        solar = norm_solar
        
        norm = y_Ia_ref + y_cc_ref

        cont_Ia = (y_Ia / norm) * (mref_mx / solar)
        cont_cc = (y_cc / norm) * (mref_mx / solar)

        total_cont = cont_Ia + cont_cc
        
        return total_cont, cont_Ia, cont_cc
    
    @staticmethod
    def _modified_fit_func(Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element):
        
        def _fit_func(x, r):
            r_Ia, r_cc = SNeStats._ratio2percent(r)
            total_cont, _, _ = SNeStats._calc_contribution(r_Ia, r_cc, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)
                    
            return total_cont

        return _fit_func
    
    @staticmethod
    def _chisq(norm_abund, norm_abund_err, total_cont):
            
        chi = (((norm_abund - total_cont) / norm_abund_err)**2.0).sum()
        
        return chi
    
    @staticmethod
    def _modified_fit_func_conf(norm_abund, norm_abund_err, min_chi, delta_chi, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element):
        
        def _fit_func_conf(r):
            r_Ia, r_cc = SNeStats._ratio2percent(r)
            total_cont, _, _ = SNeStats._calc_contribution(r_Ia, r_cc, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)
                    
            target_chi = abs(SNeStats._chisq(norm_abund, norm_abund_err, total_cont) - min_chi - delta_chi)

            return target_chi

        return _fit_func_conf

    
    @classmethod
    def calc_contribution(cls, r_Ia, r_cc, SNeRatio):
        
        Ia_yields = SNeRatio.df_master["Ia_yields"].values
        cc_yields = SNeRatio.df_master["cc_yields"].values

        mass_number = SNeRatio.df_master["MassNumber"].values
        norm_solar = SNeRatio.df_master["norm_solar"].values

        elements = SNeRatio.df_master["Element"].values
        ref_element = SNeRatio.selections["ref_element"]
        
        total_cont, cont_Ia, cont_cc = cls._calc_contribution(r_Ia, r_cc, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)

        return total_cont, cont_Ia, cont_cc
    
    @classmethod
    def fit(cls, SNeRatio):
        
        # read parameters from SNeRatio class
        Ia_table_name = os.path.basename(SNeRatio.selections["snIa_data"]).rsplit(".",1)[0]
        cc_table_name = os.path.basename(SNeRatio.selections["sncc_data"]).rsplit(".",1)[0]
        
        Ia_yields, cc_yields, = SNeRatio.df_master["Ia_yields"].values, SNeRatio.df_master["cc_yields"].values
        mass_number, norm_solar = SNeRatio.df_master["MassNumber"].values, SNeRatio.df_master["norm_solar"].values
        elements, ref_element = SNeRatio.df_master["Element"].values, SNeRatio.selections["ref_element"]

        x = range(len(elements))
        norm_abund = SNeRatio.df_master.norm_abund
        norm_abund_err = SNeRatio.df_master.norm_abund_err

        
        # fit
        r_init = 0.5        
        modified_fit_func = cls._modified_fit_func(Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)
        r_best, _ = curve_fit(modified_fit_func, x, norm_abund, sigma=norm_abund_err, p0=[r_init], bounds=(0,np.inf))
        
        # best r contributions
        r_Ia_best, r_cc_best = SNeStats._ratio2percent(r_best)
        total_cont, cont_Ia, cont_cc = cls._calc_contribution(r_Ia_best, r_cc_best, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)
        
        # delta chi for uncertainties
        min_chi = cls._chisq(norm_abund, norm_abund_err, total_cont)
        delta_chi = SNeRatio.sigma_to_delta_chisq[SNeRatio.selections["confidence"]]

        modified_fit_func_conf = cls._modified_fit_func_conf(norm_abund, norm_abund_err, min_chi, delta_chi, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)

        # lower uncertainty
        r_low_init = r_best/1.5
        fit_result_low = least_squares(modified_fit_func_conf, x0=r_low_init)
        r_low = fit_result_low.x

        # upper uncertainty
        r_high_init = min(r_best*1.5, 1.0) # should not exceed 1.0
        fit_result_high = least_squares(modified_fit_func_conf, x0=r_high_init)
        r_high = fit_result_high.x
                
        # error values
        r_Ia_best = r_best/(1.0 + r_best)
        r_Ia_low = r_low/(1.0 + r_low)
        r_Ia_high = r_high/(1.0 + r_high)
        
        r_Ia_err_n = r_Ia_best - r_Ia_low
        r_Ia_err_p = r_Ia_high - r_Ia_best

        r_cc_best = 1.0 - r_Ia_best
        r_cc_err_n = r_Ia_err_p
        r_cc_err_p = r_Ia_err_n

        # fit results
        dof = len(elements)-1-1
        
        fit_results = {
            "Ia_table": Ia_table_name,
            "cc_table": cc_table_name,

            "elements": elements,

            "total_cont": total_cont,
            "cont_Ia": cont_Ia,
            "cont_cc": cont_cc,

            "r_Ia": r_Ia_best[0],
            "r_Ia_err_n": r_Ia_err_n[0],
            "r_Ia_err_p": r_Ia_err_p[0],

            "r_cc": r_cc_best[0],
            "r_cc_err_n": r_cc_err_n[0],
            "r_cc_err_p": r_cc_err_p[0],

            "chisq": min_chi,
            "dof": dof,
        }
        
        cls.fit_results = fit_results
        
        return fit_results
    
    @classmethod
    def fit_all_old(cls, SNeRatio):

        snIa_tables = [f for f in SNeRatio.options["snIa_data"] if f.endswith(".txt")]
        sncc_tables = [f for f in SNeRatio.options["sncc_data"] if f.endswith(".txt")]
        
        n_Ia = len(snIa_tables)
        n_cc = len(sncc_tables)

        Ia_yields_list = np.arange(n_Ia, dtype=np.ndarray)
        cc_yields_list = np.arange(n_cc, dtype=np.ndarray)
        
        # non-changing values for fitting all combinations
        mass_number, norm_solar = SNeRatio.df_master["MassNumber"].values, SNeRatio.df_master["norm_solar"].values
        elements, ref_element = SNeRatio.df_master["Element"].values, SNeRatio.selections["ref_element"]
        
        imf = SNeRatio.imf_dict[SNeRatio.selections["imf"]]
        mass_range = SNeRatio.selections["sncc_mass_range"]
        
        x = range(len(elements))
        norm_abund = SNeRatio.df_master.norm_abund
        norm_abund_err = SNeRatio.df_master.norm_abund_err

        # yields for all tables
        for i,Ia in enumerate(snIa_tables):
            Ia_path = SNeRatio._paths["snIa_data"]
            temp_df_Ia = SNeRatio.read_data(os.path.join(Ia_path, Ia))
            temp_Ia_yields = SNeRatio._calc_snIa_yields(temp_df_Ia, elements)
            Ia_yields_list[i] = np.array(temp_Ia_yields)
             
        for i,cc in enumerate(sncc_tables):
            cc_path = SNeRatio._paths["sncc_data"]
            temp_df_cc = SNeRatio.read_data(os.path.join(cc_path, cc))
            temp_cc_yields = SNeRatio._calc_sncc_yields(temp_df_cc, elements, imf, mass_range)
            cc_yields_list[i] = np.array(temp_cc_yields)
            
        total_cont_list = np.arange(n_Ia*n_cc, dtype=np.ndarray).reshape(n_Ia,n_cc)
        cont_Ia_list = np.arange(n_Ia*n_cc, dtype=np.ndarray).reshape(n_Ia,n_cc)
        cont_cc_list = np.arange(n_Ia*n_cc, dtype=np.ndarray).reshape(n_Ia,n_cc)
        
        ratio_Ia_list = np.arange(n_Ia*n_cc*3, dtype=float).reshape(n_Ia,n_cc,3)
        ratio_cc_list = np.arange(n_Ia*n_cc*3, dtype=float).reshape(n_Ia,n_cc,3)
        
        chisq_list = np.arange(n_Ia*n_cc, dtype=float).reshape(n_Ia,n_cc)

        for i,Ia_yields in enumerate(Ia_yields_list):
            
            for j,cc_yields in enumerate(cc_yields_list):
                
                # fit
                r_init = 0.5        
                modified_fit_func = cls._modified_fit_func(Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)
                r_best, cov = curve_fit(modified_fit_func, x, norm_abund, sigma=norm_abund_err, p0=[r_init], bounds=(0,np.inf))

                # best r contributions
                r_Ia_best = r_best / (1.0+r_best)
                r_cc_best = 1.0 / (1.0+r_best)
                total_cont, cont_Ia, cont_cc = cls._calc_contribution(r_Ia_best, r_cc_best, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)

                # delta chi for uncertainties
                min_chi = cls._chisq(norm_abund, norm_abund_err, total_cont)
                delta_chi = SNeRatio.sigma_to_delta_chisq[SNeRatio.selections["confidence"]]

                modified_fit_func_conf = cls._modified_fit_func_conf(norm_abund, norm_abund_err, min_chi, delta_chi, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)
                
                # lower uncertainty
                r_low_init = r_best/1.5
                fit_result_low = least_squares(modified_fit_func_conf, x0=r_low_init)
                r_low = fit_result_low.x

                # upper uncertainty
                r_high_init = min(r_best*1.5, 1.0) # should not exceed 1.0
                fit_result_high = least_squares(modified_fit_func_conf, x0=r_high_init)
                r_high = fit_result_high.x

                # error values
                r_Ia_best = r_best/(1.0 + r_best)
                r_Ia_low = r_low/(1.0 + r_low)
                r_Ia_high = r_high/(1.0 + r_high)

                r_Ia_err_n = r_Ia_best - r_Ia_low
                r_Ia_err_p = r_Ia_high - r_Ia_best

                r_cc_best = 1.0 - r_Ia_best
                r_cc_err_n = r_Ia_err_p
                r_cc_err_p = r_Ia_err_n

                # fit results
                total_cont_list[i][j] = total_cont
                cont_Ia_list[i][j] = cont_Ia
                cont_cc_list[i][j] = cont_cc

                ratio_Ia_list[i][j] = [r_Ia_best[0], r_Ia_err_n[0], r_Ia_err_p[0]]
                ratio_cc_list[i][j] = [r_cc_best[0], r_cc_err_n[0], r_cc_err_p[0]]
                
                chisq_list[i][j] = min_chi
                
        fit_results_all = {
            "n_Ia": n_Ia,
            "n_cc": n_cc,
            "Ia_table": snIa_tables,
            "cc_table": sncc_tables,
            "elements": elements,
            "total_cont": total_cont_list,
            "cont_Ia": cont_Ia_list,
            "cont_cc": cont_cc_list,
            "ratio_Ia": ratio_Ia_list,
            "ratio_cc": ratio_cc_list,
            "chisq": chisq_list,
            "dof": len(elements)-1-1,
        }

        cls.fit_results_all = fit_results_all
                
        return fit_results_all

    @classmethod
    def fit_all(cls, SNeRatio):

        snIa_tables = [f for f in SNeRatio.options["snIa_data"] if f.endswith(".txt")]
        sncc_tables = [f for f in SNeRatio.options["sncc_data"] if f.endswith(".txt")]
        
        n_Ia = len(snIa_tables)
        n_cc = len(sncc_tables)

        Ia_yields_list = np.arange(n_Ia, dtype=np.ndarray)
        cc_yields_list = np.arange(n_cc, dtype=np.ndarray)
        
        # non-changing values for fitting all combinations
        mass_number, norm_solar = SNeRatio.df_master["MassNumber"].values, SNeRatio.df_master["norm_solar"].values
        elements, ref_element = SNeRatio.df_master["Element"].values, SNeRatio.selections["ref_element"]
        
        imf = SNeRatio.imf_dict[SNeRatio.selections["imf"]]
        mass_range = SNeRatio.selections["sncc_mass_range"]
        
        x = range(len(elements))
        norm_abund = SNeRatio.df_master.norm_abund
        norm_abund_err = SNeRatio.df_master.norm_abund_err

        # yields for all tables
        for i,Ia in enumerate(snIa_tables):
            Ia_path = SNeRatio._paths["snIa_data"]
            temp_df_Ia = SNeRatio.read_data(os.path.join(Ia_path, Ia))
            temp_Ia_yields = SNeRatio._calc_snIa_yields(temp_df_Ia, elements)
            Ia_yields_list[i] = np.array(temp_Ia_yields)
             
        for i,cc in enumerate(sncc_tables):
            cc_path = SNeRatio._paths["sncc_data"]
            temp_df_cc = SNeRatio.read_data(os.path.join(cc_path, cc))
            temp_cc_yields = SNeRatio._calc_sncc_yields(temp_df_cc, elements, imf, mass_range)
            cc_yields_list[i] = np.array(temp_cc_yields)

        col_names_t = ["Ia_table", "cc_table"]
        col_names_r = ["r_Ia", "r_Ia_err_n", "r_Ia_err_p", "r_cc", "r_cc_err_n", "r_cc_err_p"]
        col_names_s = ["chisq", "dof"]
        col_names_tot = [f"Total_cont_{e}" for e in elements]
        col_names_Ia = [f"Ia_cont_{e}" for e in elements]
        col_names_cc = [f"cc_cont_{e}" for e in elements]

        col_names = col_names_t + col_names_r + col_names_s + col_names_tot + col_names_Ia + col_names_cc

        r_Ia_array = np.arange(n_Ia*n_cc, dtype=float)
        r_Ia_err_n_array = np.arange(n_Ia*n_cc, dtype=float)
        r_Ia_err_p_array = np.arange(n_Ia*n_cc, dtype=float)

        r_cc_array = np.arange(n_Ia*n_cc, dtype=float)
        r_cc_err_n_array = np.arange(n_Ia*n_cc, dtype=float)
        r_cc_err_p_array = np.arange(n_Ia*n_cc, dtype=float)

        chisq_array = np.arange(n_Ia*n_cc, dtype=float)
        dof_array = np.arange(n_Ia*n_cc, dtype=float)

        total_cont_array_dict = {
            e:np.arange(n_Ia*n_cc, dtype=float) for e in elements
            }

        Ia_cont_array_dict = total_cont_array_dict.copy()
        cc_cont_array_dict = total_cont_array_dict.copy()


        for i,Ia_yields in enumerate(Ia_yields_list):
            
            for j,cc_yields in enumerate(cc_yields_list):
                
                # fit
                r_init = 0.5        
                modified_fit_func = cls._modified_fit_func(Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)
                r_best, cov = curve_fit(modified_fit_func, x, norm_abund, sigma=norm_abund_err, p0=[r_init], bounds=(0,np.inf))

                # best r contributions
                r_Ia_best = r_best / (1.0+r_best)
                r_cc_best = 1.0 / (1.0+r_best)
                total_cont, cont_Ia, cont_cc = cls._calc_contribution(r_Ia_best, r_cc_best, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)

                # delta chi for uncertainties
                min_chi = cls._chisq(norm_abund, norm_abund_err, total_cont)
                delta_chi = SNeRatio.sigma_to_delta_chisq[SNeRatio.selections["confidence"]]

                modified_fit_func_conf = cls._modified_fit_func_conf(norm_abund, norm_abund_err, min_chi, delta_chi, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)
                
                # lower uncertainty
                r_low_init = r_best/1.5
                fit_result_low = least_squares(modified_fit_func_conf, x0=r_low_init)
                r_low = fit_result_low.x

                # upper uncertainty
                r_high_init = min(r_best*1.5, 1.0) # should not exceed 1.0
                fit_result_high = least_squares(modified_fit_func_conf, x0=r_high_init)
                r_high = fit_result_high.x

                # error values
                r_Ia_best = r_best/(1.0 + r_best)
                r_Ia_low = r_low/(1.0 + r_low)
                r_Ia_high = r_high/(1.0 + r_high)

                r_Ia_err_n = r_Ia_best - r_Ia_low
                r_Ia_err_p = r_Ia_high - r_Ia_best

                r_cc_best = 1.0 - r_Ia_best
                r_cc_err_n = r_Ia_err_p
                r_cc_err_p = r_Ia_err_n

                # fit results
                index = int(i*n_cc + j)

                #Ia_table_array[index] = snIa_tables[i]
                #cc_table_array[index] = sncc_tables[j]

                r_Ia_array[index] = r_Ia_best
                r_Ia_err_n_array[index] = r_Ia_err_n
                r_Ia_err_p_array[index] = r_Ia_err_p

                r_cc_array[index] = r_cc_best
                r_cc_err_n_array[index] = r_cc_err_n
                r_cc_err_p_array[index] = r_cc_err_p

                for k,e in enumerate(elements):
                    total_cont_array_dict[e][index] = total_cont[k]
                    Ia_cont_array_dict[e][index] = cont_Ia[k]
                    cc_cont_array_dict[e][index] = cont_cc[k]

                chisq_array[index] = min_chi
                dof_array[index] = len(elements)-1-1
                

        Ia_table_array, cc_table_array = np.array(np.meshgrid(snIa_tables, sncc_tables)).reshape(2,-1)

        fit_results_all = {
            "Ia_table": Ia_table_array,
            "cc_table": cc_table_array,

            "r_Ia": r_Ia_array,
            "r_Ia_err_n": r_Ia_err_n_array,
            "r_Ia_err_p": r_Ia_err_p_array,

            "r_cc": r_cc_array,
            "r_cc_err_n": r_cc_err_n_array,
            "r_cc_err_p": r_cc_err_p_array,

            "chisq": chisq_array,
            "dof": dof_array,
        }

        for k in range(len(elements)):
            fit_results_all[col_names_tot[k]] = total_cont_array_dict[e]
            fit_results_all[col_names_Ia[k]] = Ia_cont_array_dict[e]
            fit_results_all[col_names_cc[k]] = cc_cont_array_dict[e]


        cls.fit_results_all = fit_results_all
        cls.fit_results_all_df = pd.DataFrame(fit_results_all)

        print(cls.fit_results_all_df.info())
        print(cls.fit_results_all_df.iloc[:5])
        
        return cls.fit_results_all_df

    @classmethod
    def save_fit_results(cls):

        now = datetime.datetime.now()
        now_str = now.strftime(r'%Y-%m-%d_%H-%M-%S')
        filename = "outputs/fit_results_{}.txt".format(now_str)

        saveable_fit_results = dict()

        try:
            if cls.fit_results is not None:

                for key,value in cls.fit_results.items():
                    
                    if isinstance(value, np.ndarray):
                        saveable_fit_results[key] = value.tolist()

                    else:
                        saveable_fit_results[key] = value

            with open(filename, "w+") as f:

                f.write("Fit Results (Single Fit):\n")
                f.write(json.dumps(saveable_fit_results, indent=4))

        except:
            print("WARNING: Couldn't save the fit_results!")


    @classmethod
    def save_fit_all_results_old(cls):

        now = datetime.datetime.now()
        now_str = now.strftime(r'%Y-%m-%d_%H-%M-%S')
        filename_all = "outputs/fit_all_results_{}.txt".format(now_str)

        saveable_fit_results_all = dict()

        try:
            if cls.fit_results_all is not None:

                for key,value in cls.fit_results_all.items():
                    if isinstance(value, np.ndarray):
                        saveable_fit_results_all[key] = value.flatten().tolist()

                    else:
                        saveable_fit_results_all[key] = value

            with open(filename_all, "w+") as f:

                f.write("\n\nFit Results (All Combinations):\n")
                f.write(json.dumps(saveable_fit_results_all, indent=4, cls=NumpyArrayEncoder))

        except:
            print("WARNING: Couldn't save the fit_all_results!")


    @classmethod
    def save_fit_all_results(cls):

        now = datetime.datetime.now()
        now_str = now.strftime(r'%Y-%m-%d_%H-%M-%S')
        filename_csv = "outputs/fit_all_results_{}.csv".format(now_str)
        filename_xlsx = "outputs/fit_all_results_{}.xlsx".format(now_str)

        try:

            if cls.fit_results_all_df is not None:

                with open(filename_csv, "w+") as f:
                    cls.fit_results_all_df.to_csv(filename_csv, sep=",")

        except:
            print("WARNING: Couldn't save the fit_all_results!")

        try:
            import openpyxl
        
            with open(filename_xlsx, "w+") as f:
                cls.fit_results_all_df.to_excel(filename_xlsx, encoding="utf-8")

        except:
            print("WARNING: Couldn't save as .xslx!")


 
# SNePlots class --------------------------------------------

class SNePlots:
    
    @staticmethod
    def plot_contribution(SNeRatio, SNeStats):
        
        norm_abund = SNeRatio.df_master.norm_abund
        norm_abund_err = SNeRatio.df_master.norm_abund_err
        
        elements = SNeRatio.df_master["Element"].values
        ref_element = SNeRatio.selections["ref_element"]
        
        font = {'size'   : 14}
        plt.rc('font', **font)

        fig, ax = plt.subplots(1,1, figsize=(8,6))
        
        ax.errorbar(x=elements, y=norm_abund, yerr=norm_abund_err, fmt=".", color="black", lw=2.0)
        
        x_values = list(range(len(elements)))
        
        Ia_table = SNeStats.fit_results["Ia_table"]
        cc_table = SNeStats.fit_results["cc_table"]
        
        total_cont = SNeStats.fit_results["total_cont"]
        cont_Ia = SNeStats.fit_results["cont_Ia"]
        cont_cc = SNeStats.fit_results["cont_cc"]

        rIa = SNeStats.fit_results["r_Ia"]
        rIa_n = SNeStats.fit_results["r_Ia_err_n"]
        rIa_p = SNeStats.fit_results["r_Ia_err_p"]

        rcc = SNeStats.fit_results["r_cc"]
        rcc_n = SNeStats.fit_results["r_cc_err_n"]
        rcc_p = SNeStats.fit_results["r_cc_err_p"]

        ax.bar(x=x_values, height=cont_Ia, color="red", width=0.4, alpha=0.6, label="SNIa(%): {:.1f}(-{:.1f},+{:.1f}) [{}]".format(rIa*100, rIa_n*100, rIa_p*100, Ia_table))
        ax.bar(x=x_values, height=cont_cc, bottom=cont_Ia, color="teal", width=0.4, alpha=0.6, label="SNcc(%): {:.1f}(-{:.1f},+{:.1f}) [{}]".format(rcc*100, rcc_n*100, rcc_p*100, cc_table))
            
        ax.axhline(y=1.0, color="black", ls="--")    
            
        # calculating ylim
        max_data = max(norm_abund + norm_abund_err)
        max_model = max(total_cont)
        max_y = max(max_data, max_model)
        y_lim = max_y * 1.25

        ax.set_ylim([0, y_lim])
        
        ax.set_xlabel("Elements")
        ax.set_ylabel("$[X/Fe]_\odot$")
        
        ax.legend(prop={'size':12})
        fig.savefig("outputs/plot_fit.jpeg", dpi=200)
        
    @staticmethod
    def plot_statistics(SNeRatio, SNeStats):
        chisq = SNeStats.fit_results["chisq"]
        dof = SNeStats.fit_results["dof"]
        
        norm_abund = SNeRatio.df_master.norm_abund
        norm_abund_err = SNeRatio.df_master.norm_abund_err
                
        Ia_yields, cc_yields, = SNeRatio.df_master["Ia_yields"].values, SNeRatio.df_master["cc_yields"].values
        mass_number, norm_solar = SNeRatio.df_master["MassNumber"].values, SNeRatio.df_master["norm_solar"].values
        elements, ref_element = SNeRatio.df_master["Element"].values, SNeRatio.selections["ref_element"]

        x_list = np.linspace(0.0, 1.0, 2000)
        chi_list = np.array([((norm_abund - SNeStats._calc_contribution(x, 1.0-x, Ia_yields, cc_yields, mass_number, norm_solar, elements, ref_element)[0])**2.0 / norm_abund_err**2.0).sum() for x in x_list])
        chi_min = chi_list.min()
        
        min_index = np.where(chi_min == chi_list)
        best_ratio1 = x_list[min_index]

        rIa = SNeStats.fit_results["r_Ia"]
        rIa_n = SNeStats.fit_results["r_Ia_err_n"]
        rIa_p = SNeStats.fit_results["r_Ia_err_p"]

        rcc = SNeStats.fit_results["r_cc"]
        rcc_n = SNeStats.fit_results["r_cc_err_n"]
        rcc_p = SNeStats.fit_results["r_cc_err_p"]
        
        print("R_snIa: {:.3f} (-{:.3f},+{:.3f})".format(rIa, rIa_n, rIa_p))
        print("R_sncc: {:.3f} (-{:.3f},+{:.3f})".format(rcc, rcc_n, rcc_p))
        
        font = {'size'   : 14}
        plt.rc('font', **font)

        fig, ax = plt.subplots(1,1, figsize=(8,6))

        ax.plot(x_list,chi_list)

        ax.axvline(x=best_ratio1, color="red", label="SNIa/(SNIa+SNcc)(%): {:.1f}(-{:.1f},+{:.1f})".format(rIa*100, rIa_n*100, rIa_p*100))
        ax.axvline(x=best_ratio1 - rIa_n, color="red", ls="--", label="${}\sigma$ conf. interval".format(SNeRatio.selections["confidence"]))
        ax.axvline(x=best_ratio1 + rIa_p, color="red", ls="--")

        delta_chisq = SNeRatio.sigma_to_delta_chisq[SNeRatio.selections["confidence"]]

        ax.axhline(y=chi_list.min(), color="black", label="$\chi^{2}_{min}$" + "={:.1f}".format(chi_min))
        ax.axhline(y=chi_list.min()+delta_chisq, color="black", ls="--", label="$\chi^{2}_{min} + \Delta\chi^{2}$" + "={:.1f}".format(chi_min+delta_chisq))

        ax.set_xlim([max(rIa - 2.0*rIa_n, 0), rIa + 2.0*rIa_p])
        ax.set_ylim([chi_min-(0.3*delta_chisq), chi_min+(2.5*delta_chisq)])
                
        ax.set_xlabel("Ratio (SNIa/(SNIa+SNcc))")
        ax.set_ylabel("$\chi^2$")
        
        ax.legend(prop={'size':10})
        fig.savefig("outputs/plot_statistics.jpeg", dpi=200)
        
    @staticmethod
    def plot_fit_all_old(SNeRatio, SNeStats):
        
        n_Ia = SNeStats.fit_results_all["n_Ia"]
        n_cc = SNeStats.fit_results_all["n_cc"]
        
        n_total = n_Ia * n_cc
        
        cc_tables = SNeStats.fit_results_all["cc_table"]
        Ia_tables = SNeStats.fit_results_all["Ia_table"]

        chisq = SNeStats.fit_results_all["chisq"]
        ratio_Ia, ratio_Ia_err_n, ratio_Ia_err_p = np.dsplit(SNeStats.fit_results_all["ratio_Ia"], 3)
        
        ratio_Ia = ratio_Ia.reshape(n_Ia, n_cc)
        ratio_Ia_err_n = ratio_Ia_err_n.reshape(n_Ia, n_cc)
        ratio_Ia_err_p = ratio_Ia_err_p.reshape(n_Ia, n_cc)
        
        font = {'size'   : 8}
        plt.rc('font', **font)

        fig = plt.figure(dpi=200, figsize=(10,10), facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = [fig.add_subplot(141),
              fig.add_subplot(142),
              fig.add_subplot(143)]

        fig.subplots_adjust(left=0.15,
                            bottom=0.175,
                            right=0.95,
                            top=0.95,
                            wspace=0.0,
                            hspace=0.0)
        
        #---------------------------------------------------------------------------------
        
        xlabel = [t.rsplit(".", 1)[0] for t in cc_tables]
        ax[0].set_xticks(range(n_cc))
        ax[0].set_xticklabels(xlabel, rotation=80, size=5)

        ylabel = [t.rsplit(".", 1)[0] for t in Ia_tables]
        ax[0].set_yticks(range(n_Ia))
        ax[0].set_yticklabels(ylabel, size=5)

        im0 = ax[0].imshow(chisq, cmap=plt.cm.get_cmap('Greens'))

        for i in range(len(xlabel)):
            for j in range(len(ylabel)):
                text = ax[0].text(i, j, "{:.2f}".format(chisq[j, i]), ha="center", va="center",
                                  color="black", fontsize=5)

        ax[0].set_title("$\chi^2$")
        
        #---------------------------------------------------------------------------------

        ax[1].set_xticks(range(n_cc))
        ax[1].set_xticklabels(xlabel, rotation=80, size=5)

        ylabel = ["" for _ in Ia_tables]
        ax[1].set_yticks(range(n_Ia))
        ax[1].set_yticklabels(ylabel, size=5)

        im1 = ax[1].imshow(ratio_Ia, vmin=0, vmax=1, cmap=plt.cm.get_cmap('autumn_r'))

        for i in range(len(xlabel)):
            for j in range(len(ylabel)):
                text = ax[1].text(i, j, "{:.2f}".format(ratio_Ia[j, i]), ha="center", va="center",
                                  color="black", fontsize=5)

        ax[1].set_title("SNIa Ratio")
        
        #---------------------------------------------------------------------------------
        
        ax[2].set_xticks(range(n_cc))
        ax[2].set_xticklabels(xlabel, rotation=80, size=5)

        ylabel = ["" for _ in Ia_tables]
        ax[2].set_yticks(range(n_Ia))
        ax[2].set_yticklabels(ylabel, size=5)

        ax[2].imshow(ratio_Ia_err_n, vmin=0, vmax=1, cmap=plt.cm.get_cmap('summer_r'))

        for i in range(len(xlabel)):
            for j in range(len(ylabel)):
                avg_err = (abs(ratio_Ia_err_n[j, i]) + abs(ratio_Ia_err_p[j, i]))/2.0
                text = ax[2].text(i, j, "{:.2f}".format(avg_err), ha="center", va="center",
                                  color="black", fontsize=5)

        ax[2].set_title("Avg. Error")
        
        #---------------------------------------------------------------------------------
        
        cbar0 = plt.colorbar(im0, ax=ax[0], orientation='vertical', aspect=60)
        cbar0.ax.tick_params(axis="both", labelsize=7)
        
        cbar1 = plt.colorbar(im1, ax=ax[1], orientation='vertical', aspect=60)
        cbar1.ax.tick_params(axis="both", labelsize=7)

        fig.tight_layout()
        fig.savefig("outputs/plot_fit_all.jpeg", dpi=200)


    @staticmethod
    def plot_fit_all(SNeRatio, SNeStats):
        
        Ia_tables = SNeStats.fit_results_all_df["Ia_table"].unique()
        cc_tables = SNeStats.fit_results_all_df["cc_table"].unique()

        n_Ia = len(Ia_tables)
        n_cc = len(cc_tables)
                
        font = {'size'   : 8}
        plt.rc('font', **font)

        fig = plt.figure(dpi=200, figsize=(10,10), facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        ax = [fig.add_subplot(141),
              fig.add_subplot(142),
              fig.add_subplot(143)]

        fig.subplots_adjust(left=0.15,
                            bottom=0.175,
                            right=0.95,
                            top=0.95,
                            wspace=0.0,
                            hspace=0.0)
        
        #---------------------------------------------------------------------------------
        
        chisq_data = SNeStats.fit_results_all_df.groupby(["Ia_table","cc_table"])["chisq"].mean().unstack().values
        
        r_Ia_data = SNeStats.fit_results_all_df.groupby(["Ia_table","cc_table"])["r_Ia"].mean().unstack().values
        
        r_Ia_err_n_data = SNeStats.fit_results_all_df.groupby(["Ia_table","cc_table"])["r_Ia_err_n"].mean().unstack().values
        r_Ia_err_p_data = SNeStats.fit_results_all_df.groupby(["Ia_table","cc_table"])["r_Ia_err_p"].mean().unstack().values
        
        r_Ia_err_data = (r_Ia_err_n_data + r_Ia_err_p_data)/2.0

        xlabel = [t.rsplit(".", 1)[0] for t in cc_tables]
        ax[0].set_xticks(range(n_cc))
        ax[0].set_xticklabels(xlabel, rotation=80, size=5)

        ylabel = [t.rsplit(".", 1)[0] for t in Ia_tables]
        ax[0].set_yticks(range(n_Ia))
        ax[0].set_yticklabels(ylabel, size=5)

        im0 = ax[0].imshow(chisq_data, cmap=plt.cm.get_cmap('Greens'))

        for i in range(len(xlabel)):
            for j in range(len(ylabel)):
                text = ax[0].text(i, j, "{:.2f}".format(chisq_data[j, i]), ha="center", va="center",
                                  color="black", fontsize=5)

        ax[0].set_title("$\chi^2$")
        
        #---------------------------------------------------------------------------------

        ax[1].set_xticks(range(n_cc))
        ax[1].set_xticklabels(xlabel, rotation=80, size=5)

        ylabel = ["" for _ in Ia_tables]
        ax[1].set_yticks(range(n_Ia))
        ax[1].set_yticklabels(ylabel, size=5)

        im1 = ax[1].imshow(r_Ia_data, vmin=0, vmax=1, cmap=plt.cm.get_cmap('autumn_r'))

        for i in range(len(xlabel)):
            for j in range(len(ylabel)):
                text = ax[1].text(i, j, "{:.2f}".format(r_Ia_data[j, i]), ha="center", va="center",
                                  color="black", fontsize=5)

        ax[1].set_title("SNIa Ratio")
        
        #---------------------------------------------------------------------------------
        
        ax[2].set_xticks(range(n_cc))
        ax[2].set_xticklabels(xlabel, rotation=80, size=5)

        ylabel = ["" for _ in Ia_tables]
        ax[2].set_yticks(range(n_Ia))
        ax[2].set_yticklabels(ylabel, size=5)

        ax[2].imshow(r_Ia_err_data, vmin=0, vmax=1, cmap=plt.cm.get_cmap('summer_r'))

        for i in range(len(xlabel)):
            for j in range(len(ylabel)):
                avg_err = r_Ia_err_data[j,i]
                text = ax[2].text(i, j, "{:.2f}".format(avg_err), ha="center", va="center",
                                  color="black", fontsize=5)

        ax[2].set_title("Avg. Error")
        
        #---------------------------------------------------------------------------------
        
        cbar0 = plt.colorbar(im0, ax=ax[0], orientation='vertical', aspect=60)
        cbar0.ax.tick_params(axis="both", labelsize=7)
        
        cbar1 = plt.colorbar(im1, ax=ax[1], orientation='vertical', aspect=60)
        cbar1.ax.tick_params(axis="both", labelsize=7)

        fig.tight_layout()
        fig.savefig("outputs/plot_fit_all.jpeg", dpi=200)


 # Numpy Array to JSON encoder class --------------------------------------------

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


 # Functions to import --------------------------------------------

def print_options():
    SNeRatio.print_options()


def fit(selections):
    # to apply the selections
    SNeRatio.set_selections(selections)

    # to read the selected data options and do the calculations
    SNeRatio.read_all()
    SNeRatio.set_snIa_yields()
    SNeRatio.set_sncc_yields()
    SNeRatio.set_solar()
    SNeRatio.set_mass_number()
    SNeRatio.set_normalisations()

    # to do a single fit with your selections
    # and measure the calculation time
    t1 = time.time()
    fit_results = SNeStats.fit(SNeRatio)
    t2 = time.time()
    print("fit time:",t2-t1)

    # to save the fit results as a text file in the 'outputs' folder
    SNeStats.save_fit_results()

    # to saves the plots in the 'outputs' folder
    SNePlots.plot_contribution(SNeRatio, SNeStats)
    SNePlots.plot_statistics(SNeRatio, SNeStats)

    return fit_results


def fit_all(selections):
    # to apply the selections
    SNeRatio.set_selections(selections)

    # to read the selected data options and do the calculations
    SNeRatio.read_all()
    SNeRatio.set_snIa_yields()
    SNeRatio.set_sncc_yields()
    SNeRatio.set_solar()
    SNeRatio.set_mass_number()
    SNeRatio.set_normalisations()

    # to do a multiple fit with all of the sn yield model combinations with your other selections
    # and measure the calculation time
    t1 = time.time()
    fit_results_list = SNeStats.fit_all(SNeRatio)
    t2 = time.time()
    print("fit all time:",t2-t1)

    # to save the fit results as a text file in the 'outputs' folder
    SNeStats.save_fit_all_results()

    # to saves the plots in the 'outputs' folder
    SNePlots.plot_fit_all(SNeRatio, SNeStats)

    return fit_results_list
