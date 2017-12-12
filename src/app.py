from flask import Flask, request, render_template, url_for
from cron import Cron

from almacenamiento import Internal_DB
from obtain import get_a_value

db = Internal_DB()

import time

app = Flask(__name__)

def format_datetime(value, format='medium'):
    return value

app.jinja_env.filters['datetime'] = format_datetime

cron = Cron()
@cron.add_task(minute=2)
def save_value():
    db.add_value(get_a_value())

@app.route('/')
def index():
    args = {
        't': time.time,
        'values': db.get_all()
    }
    return render_template('index.html', **args)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
