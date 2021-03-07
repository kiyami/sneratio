"""from flask import (
    Blueprint, render_template, request,
)

import json
from sneratio.src.adapter import Methods

import io
import base64

#from sneratio import bp
from sneratio import r
from sneratio import q
from sneratio.tasks import task_fit_all


bp = Blueprint('', __name__)

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


@bp.route('/fit_loop', methods=('GET', 'POST'))
def fit_loop():
    fig = Methods.get_empty_plot()
    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)
    encoded_img_data = base64.b64encode(img_data.read())

    if request.method == 'POST':
        updated_data_field = json.loads(request.form["data_field_2"])

        if Methods.get_loop_status == "idle":
            Methods.update_data_field(updated_data_field)
            task = q.enqueue(Methods.fit_loop)  # Send a job to the task queue

            Methods.set_status_text("Fitting for all models.. (started)")

        if Methods.get_loop_status == "in_loop":
            Methods.set_status_text("Fitting for all models.. (in progress)")

        if Methods.get_loop_status == "completed":
            fig = Methods.get_fit_loop_plot()
            img_data = io.BytesIO()
            fig.savefig(img_data, format="png")
            img_data.seek(0)
            encoded_img_data = base64.b64encode(img_data.read())

            Methods.set_loop_status("idle")
            Methods.set_status_text("Fitting for all models.. (completed)")

        return render_template('index.html',
                               data_field=Methods.get_data_field(),
                               img_data=encoded_img_data.decode(),
                               status=Methods.get_status_text())

    return render_template('index.html',
                           data_field=Methods.get_data_field(),
                           img_data=encoded_img_data.decode(),
                           status=Methods.get_status_text())
"""