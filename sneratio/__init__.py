from flask import (
    Blueprint, render_template, request,
)

import redis
from rq import Queue


import json
from sneratio.src.adapter import Methods

import io
import base64
import time


bp = Blueprint('', __name__)

r = redis.Redis()
q = Queue(connection=r)

Methods.initialise_options()


@bp.route('/', methods=('GET', 'POST'))
def main():
    fig = Methods.get_empty_plot()
    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)
    encoded_img_data = base64.b64encode(img_data.read())

    Methods.set_status_text("Welcome to the SNeRatio App..")

    return render_template('index.html',
                           data_field=Methods.get_data_field(),
                           img_data=encoded_img_data.decode(),
                           status=Methods.get_status_text())


@bp.route('/fit', methods=('GET', 'POST'))
def fit():
    fig = Methods.get_empty_plot()
    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)
    encoded_img_data = base64.b64encode(img_data.read())

    if request.method == 'POST':
        updated_data_field = json.loads(request.form["data_field"])

        if updated_data_field["results"]["ref_element_selected"] and updated_data_field["results"]["min_elements_selected"]:

            Methods.update_data_field(updated_data_field)
            Methods.fit()

            fig = Methods.get_fit_plot()
            img_data = io.BytesIO()
            fig.savefig(img_data, format="png")
            img_data.seek(0)
            encoded_img_data = base64.b64encode(img_data.read())

            Methods.set_status_text("Fitting completed..")

        else:
            Methods.set_status_text("Invalid Selections..")

        return render_template('index.html',
                               data_field=Methods.get_data_field(),
                               img_data=encoded_img_data.decode(),
                               status=Methods.get_status_text())

    return render_template('index.html',
                           data_field=Methods.get_data_field(),
                           img_data=encoded_img_data.decode(),
                           status=Methods.get_status_text())


def fit_loop_task(updated_data_field):
    Methods.update_data_field(updated_data_field)
    Methods.fit_loop()


@bp.route('/fit_loop', methods=('GET', 'POST'))
def fit_loop():
    fig = Methods.get_empty_plot()
    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)
    encoded_img_data = base64.b64encode(img_data.read())

    print("clicked fit_loop", time.time())
    #Methods.set_status_text(f"Fitting for all models.. (in progress) {time.time()}")
    #Methods.set_loop_status("in_loop")


    if request.method == 'POST':
        updated_data_field = json.loads(request.form["data_field_2"])
        #Methods.update_data_field(updated_data_field)

        print("###### loop status:", Methods.get_loop_status())

        if Methods.get_loop_status() == "idle":
            q.enqueue(fit_loop_task, updated_data_field)  # Send a job to the task queue

            Methods.set_loop_status("in_loop")
            Methods.set_status_text(f"Fitting for all models.. (started) {time.time()}")
            print("###### loop status:", Methods.get_loop_status())

        if Methods.get_loop_status() == "in_loop":
            Methods.set_status_text(f"Fitting for all models.. (in progress) {time.time()}")

        if Methods.get_loop_status() == "completed":
            fig = Methods.get_fit_loop_plot()
            img_data = io.BytesIO()
            fig.savefig(img_data, format="png")
            img_data.seek(0)
            encoded_img_data = base64.b64encode(img_data.read())

            Methods.set_loop_status("idle")
            Methods.set_status_text(f"Fitting for all models.. (completed) {time.time()}")

        return render_template('index.html',
                               data_field=Methods.get_data_field(),
                               img_data=encoded_img_data.decode(),
                               status=Methods.get_status_text())

    return render_template('index.html',
                           data_field=Methods.get_data_field(),
                           img_data=encoded_img_data.decode(),
                           status=Methods.get_status_text())

