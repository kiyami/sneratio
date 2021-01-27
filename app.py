from flask import Flask

#import main

app = Flask(__name__, instance_relative_config=True)

#################################

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import json
from sneratio.src.adapter import Methods

import io
import base64


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

    return render_template('sneratio/templates/index.html',
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
        #print("updated_data_field elements", updated_data_field["selections"])

        Methods.update_data_field(updated_data_field)
        Methods.fit()

        fig = Methods.get_fit_plot()
        img_data = io.BytesIO()
        fig.savefig(img_data, format="png")
        img_data.seek(0)
        encoded_img_data = base64.b64encode(img_data.read())

        Methods.set_status_text("Fitting completed..")

        return render_template('sneratio/templates/index.html',
                               data_field=Methods.get_data_field(),
                               img_data=encoded_img_data.decode(),
                               status=Methods.get_status_text())

    return render_template('sneratio/templates/index.html',
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

        Methods.update_data_field(updated_data_field)
        Methods.fit_loop()

        fig = Methods.get_fit_loop_plot()
        img_data = io.BytesIO()
        fig.savefig(img_data, format="png")
        img_data.seek(0)
        encoded_img_data = base64.b64encode(img_data.read())

        Methods.set_status_text("Fitting for all models completed..")

        return render_template('sneratio/templates/index.html',
                               data_field=Methods.get_data_field(),
                               img_data=encoded_img_data.decode(),
                               status=Methods.get_status_text())

    return render_template('sneratio/templates/index.html',
                           data_field=Methods.get_data_field(),
                           img_data=encoded_img_data.decode(),
                           status=Methods.get_status_text())


#################################


app.register_blueprint(bp)
app.add_url_rule('/', endpoint='index')


if __name__ == '__main__':
    app.run()
