from sneratio.src.lib import info
from sneratio.src.lib.table import Data
from sneratio.src.lib.stats import Stats
from sneratio.src.lib import plots

from flask import json
import time

import io
import base64
import os
import sys

import sqlite3


class Methods:
    db_path = None
    info_json_path = None

    @staticmethod
    def initialise_options():
        info.options_dict["Ia_table"] = info.get_keyword_content("Ia_table")
        info.options_dict["cc_table"] = info.get_keyword_content("cc_table")

        Methods.info_json_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "info.json")

        #Methods.write_info_to_json()
        #Methods.write_loop_info_to_json()
        Methods.db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sneratio.db")
        Methods.initialize_db(db_path=Methods.db_path)

    @staticmethod
    def get_data_field():
        data_field = {
            "options": info.options_dict,
            "selections": info.selected_option_dict,
            "elements": info.elements_dict,
            "results": info.results_dict,
        }

        return data_field

    @staticmethod
    def update_data_field(selections_data, elements_data):
        info.selected_option_dict = selections_data
        info.elements_dict = elements_data
        # info.results_dict = {}

        # info.options_dict = data_field["options"]
        # info.selected_option_dict = data_field["selections"]
        # info.elements_dict = data_field["elements"]
        # info.results_dict = {}

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
    def fit_loop_old():
        Methods.write_loop_info_to_json()

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

        print("fit_loop")
        Stats.fit_loop()

        info.results_dict["fit_results"] = Stats.get_fit_loop_results()
        info.results_dict["fit_results_text"] = Stats.get_fit_loop_results_text()
        info.plot_dict["fit_loop_plot"] = plots.get_fit_loop_plot()


        fig = Methods.get_fit_plot()
        img_data = io.BytesIO()
        fig.savefig(img_data, format="png")
        img_data.seek(0)
        encoded_img_data = base64.b64encode(img_data.read())

        loop_info = {
            "task_done": True,
            "img_data": encoded_img_data.decode()
        }

        Methods.write_loop_info_to_json(data_field=loop_info)

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
    def read_info_from_json():
        _path = Methods.get_info_json_path()
        with open(_path, 'r') as openfile:
          json_object = json.load(openfile)

        return json_object

    @staticmethod
    def write_info_to_json():
        _path = Methods.get_info_json_path()
        with open(_path, "w") as outfile:
            json.dump(Methods.get_data_field(), outfile, indent=4)

    @staticmethod
    def read_loop_info_from_json():
        print("read_loop_info_from_json")
        with open('/app/sneratio/src/loop_info.json', 'r') as openfile:
            json_object = json.load(openfile)

        return json_object

    @staticmethod
    def write_loop_info_to_json(data_field=None):
        print("write_loop_info_to_json")
        if data_field is None:
            data_field = {
                "task_done": False,
                "img_data": "",
                "fit_results": {
                    "chi_squared": "",
                    "dof": "",
                    "ratio": "",
                }
            }

        with open("/app/sneratio/src/loop_info.json", "w") as outfile:
            json.dump(data_field, outfile)

        print("write_loop_info_to_json ended!!")

    @staticmethod
    def get_db_path():
        #db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "api/sneratio/src/sneratio.db")
        #print("db path", db_path)
        #db_path = "/Users/kym/WebProjects/k-blog/api/sneratio/src/sneratio.db"
        return Methods.db_path

    @staticmethod
    def get_info_json_path():
        #json_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "api/sneratio/src/info.json")
        #print("json path", json_path)
        #json_path = "/Users/kym/WebProjects/k-blog/api/sneratio/src/info.json"
        return Methods.info_json_path

    @staticmethod
    def _create_db(db_path):
        print("_create_db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS loop_info
                    (id integer primary key, task_done bool, img_data text)''')

        conn.commit()
        conn.close()

    @staticmethod
    def _reset_db(db_path):
        print("_reset_db")

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''DELETE FROM loop_info''')

        conn.commit()
        conn.close()

    @staticmethod
    def _insert_empty_row_db(db_path):
        print("_insert_empty_row_db")

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        task_done = False
        img_data= ""

        c.execute("INSERT INTO loop_info (task_done, img_data) VALUES(?, ?)", (task_done, img_data))

        conn.commit()
        conn.close()

    @staticmethod
    def initialize_db(db_path):
        #db_path = Methods.get_db_path()
        #print("$$$",db_path)

        Methods._create_db(db_path)
        Methods._reset_db(db_path)
        Methods._insert_empty_row_db(db_path)

    @staticmethod
    def select_db(id=None):
        #db_path = Methods.get_db_path()

        conn = sqlite3.connect(Methods.db_path)
        c = conn.cursor()

        if id is None:
            c.execute('''SELECT * FROM loop_info''')
        else:
            c.execute('''SELECT * FROM loop_info WHERE id=?''', (id,))

        rows = c.fetchall()

        # for row in rows:
        # 	print(row)

        data_field = {
            "id": rows[0][0],
            "task_done": rows[0][1],
            "img_data": rows[0][2]
        }

        if data_field["task_done"] == 1:
            data_field["task_done"] = True
        elif data_field["task_done"] == 0:
            data_field["task_done"] = False

        conn.commit()
        conn.close()

        return data_field

    @staticmethod
    def update_db(data_field):
        #db_path = Methods.get_db_path()

        id = 1

        conn = sqlite3.connect(Methods.db_path)
        c = conn.cursor()

        id = data_field["id"]
        task_done = data_field["task_done"]
        img_data = data_field["img_data"]

        c.execute('''UPDATE loop_info set (task_done, img_data)=(?, ?) where id=?''', (task_done, img_data, id))

        conn.commit()
        conn.close()


def fit_loop_db(selections, elements_data):
    #print("asdasdasd")
    #print(os.path.dirname(os.path.realpath(__file__)))

    Methods.update_data_field(selections_data=selections, elements_data=elements_data)

    #Methods.initialize_db()
    #Methods.write_loop_info_to_json()

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


    Methods.initialise_options()
    print(Methods.get_data_field())

    Stats.fit_loop()

    info.results_dict["fit_results"] = Stats.get_fit_loop_results()
    info.results_dict["fit_results_text"] = Stats.get_fit_loop_results_text()
    info.plot_dict["fit_loop_plot"] = plots.get_fit_loop_plot()

    fig = Methods.get_fit_loop_plot()

    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)
    encoded_img_data = base64.b64encode(img_data.read())

    loop_info = {
        "id": 1,
        "task_done": True,
        "img_data": encoded_img_data.decode()
    }

    #Methods.write_loop_info_to_json(data_field=loop_info)
    #info_dict = Methods.read_loop_info_from_json()

    Methods.update_db(data_field=loop_info)
    info_dict = Methods.select_db()


def fit_loop(selections, elements_data):
    Methods.update_data_field(selections_data=selections, elements_data=elements_data)

    Methods.write_loop_info_to_json()

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


    Methods.initialise_options()
    print(Methods.get_data_field())

    Stats.fit_loop()

    info.results_dict["fit_results"] = Stats.get_fit_loop_results()
    info.results_dict["fit_results_text"] = Stats.get_fit_loop_results_text()
    info.plot_dict["fit_loop_plot"] = plots.get_fit_loop_plot()

    fig = Methods.get_fit_loop_plot()

    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)
    encoded_img_data = base64.b64encode(img_data.read())

    loop_info = {
        "task_done": True,
        "img_data": encoded_img_data.decode()
    }

    Methods.write_loop_info_to_json(data_field=loop_info)
    info_dict = Methods.read_loop_info_from_json()
    print("loop done")
    print(info_dict["task_done"])

    print("realpath, adapter.py", os.path.dirname(os.path.realpath(__file__)))
    print("list_dir adapter", os.listdir("/app/sneratio/src/"))
