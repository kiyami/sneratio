from flask import Flask

app = Flask(__name__, instance_relative_config=True, static_folder="templates/static", template_folder="templates")
#app = Flask(__name__, instance_relative_config=True)

from flask import (
    Blueprint, redirect, json, render_template, request, url_for
)

import json
from sneratio.src.adapter import Methods
import sneratio.src.adapter as adapter

import io
import base64
import os

from redis import Redis
from rq import Queue, Worker

from worker import conn

bp = Blueprint('', __name__)
Methods.initialise_options()
print("methods db path", Methods.db_path)

#queue = Queue(connection=Redis())
queue = Queue(connection=conn)

@bp.route('/')
@bp.route('/sneratio')
def index():
    return render_template('index.html')

# @bp.route('/')
# @bp.route('/sneratio')
# def index():
#     return {"a": "1"}
#

@bp.route('/sneratio/get_info')
def sneratio():
    return Methods.read_info_from_json()
    #return Methods.select_db()


@bp.route('/sneratio/get_empty_plot')
def get_empty_plot():
    fig = Methods.get_empty_plot()
    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)
    encoded_img_data = base64.b64encode(img_data.read())

    return {'img_data': encoded_img_data.decode()}


@bp.route('/sneratio/fit', methods=['GET', 'POST'])
def fit():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        selections = request_data["selections"]
        elements = request_data["elements"]

        vapec_elements = ['C', 'N', 'O', 'Ne', 'Mg', 'Al', 'Si', 'S', 'Ar', 'Ca', 'Fe', 'Ni']
        elements_list, abund_list, abund_err_list = [], [], []

        for e in vapec_elements:
            if elements[f"chb_{e}"] == 1:
                elements_list.append(e)
                abund_list.append(elements[f"val_{e}"])
                abund_err_list.append(elements[f"err_{e}"])

        elements_data = {
            "element": elements_list,
            "abund": abund_list,
            "abund_err": abund_err_list,
        }

        Methods.update_data_field(selections_data=selections, elements_data=elements_data)
        Methods.fit()

        fig = Methods.get_fit_plot()
        img_data = io.BytesIO()
        fig.savefig(img_data, format="png")
        img_data.seek(0)
        encoded_img_data = base64.b64encode(img_data.read())

        Methods.set_status_text("Fitting completed..")
        results = Methods.get_data_field()["results"]

        return {"results": results, "img_data": encoded_img_data.decode(), "status": Methods.get_status_text()}

    return {'201': '/fit GET!'}


@bp.route('/sneratio/start_fit_loop', methods=['POST'])
def start_fit_loop():
    request_data = json.loads(request.data)
    selections = request_data["selections"]
    elements = request_data["elements"]

    vapec_elements = ['C', 'N', 'O', 'Ne', 'Mg', 'Al', 'Si', 'S', 'Ar', 'Ca', 'Fe', 'Ni']
    elements_list, abund_list, abund_err_list = [], [], []

    for e in vapec_elements:
        if elements[f"chb_{e}"] == 1:
            elements_list.append(e)
            abund_list.append(elements[f"val_{e}"])
            abund_err_list.append(elements[f"err_{e}"])

    elements_data = {
        "element": elements_list,
        "abund": abund_list,
        "abund_err": abund_err_list,
    }

    Methods.update_data_field(selections_data=selections, elements_data=elements_data)

    # _path = './loop_info.json'
    # if os.path.exists(_path):
    #     os.remove(_path)

    #Methods.write_loop_info_to_json()

    #res = queue.enqueue(adapter.fit_loop, selections=selections, elements_data=elements_data)
    Methods.initialize_db(db_path=Methods.db_path)
    res = queue.enqueue(adapter.fit_loop_db, selections=selections, elements_data=elements_data)

    empty_results = {
        "fit_results": {
            "chi_squared": "",
            "dof": "",
            "ratio": "",
        },

        "fit_results_text": "",
        "ref_element_selected": False,
        "min_elements_selected": False,
    }

    fig = Methods.get_empty_plot()
    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)
    encoded_img_data = base64.b64encode(img_data.read())

    Methods.set_status_text("Fit loop started.. (This may take a while..) ")

    return {"task_done": False, "results": empty_results, "img_data": encoded_img_data.decode(), 'status': Methods.get_status_text()}


@bp.route('/sneratio/check_fit_loop')
def check_fit_loop():
    #info_dict = Methods.read_loop_info_from_json()
    info_dict = Methods.select_db()

    _status_text = Methods.get_status_text()
    _new_status_text = f"{_status_text}#"
    Methods.set_status_text(_new_status_text)

    # _path = '/app/sneratio/src/loop_info.json'
    # if os.path.exists(_path):
    #     # os.remove(_path)
    #     print("path exist")
    # else:
    #     print("path doesnt exist")


    return {"task_done": info_dict["task_done"], "status": Methods.get_status_text()}


@bp.route('/sneratio/get_fit_loop_result')
def get_fit_loop_results():
    #info_dict = Methods.read_loop_info_from_json()
    info_dict = Methods.select_db()

    Methods.set_status_text("Fitting loop completed..")

    results = Methods.get_data_field()["results"]

    return {"results": results, "img_data": info_dict["img_data"], "status": Methods.get_status_text()}


app.register_blueprint(bp)
# app.add_url_rule('/', endpoint='index')


if __name__ == '__main__':
    app.run(threaded=True)
