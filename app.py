from flask import Flask
from sneratio import bp


app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(bp)
app.add_url_rule('/', endpoint='index')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)

"""
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
rq worker

"""
