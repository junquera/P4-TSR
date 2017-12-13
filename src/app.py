from flask import Flask, request, render_template, url_for
from cron import Cron

from almacenamiento import Almacenamiento
from obtain import get_a_value

import time

import datetime

db = Almacenamiento()

app = Flask(__name__)

def format_datetime(value, format='medium'):
    print(value)
    if type(value) == datetime.datetime:
        return value.isoformat(' ')
    else:
        if value[-1] == 'Z':
            value = value[:-1]
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').isoformat(' ')
        except:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').isoformat(' ')

app.jinja_env.filters['datetime'] = format_datetime

cron = Cron()
@cron.add_task(minute=2, fast_boot=True)
def save_value():
    db.add_value(get_a_value())

@app.route('/', methods=['POST', 'GET'])
def index():
    args = {
        't': time.time,
        'method': request.method,
        'request': request
    }
    if request.method == 'GET':
        values = db.get_all()
        if 'avg' in request.args:
            if len(values) > 0:
                s = 0
                i = 0
                for v in values:
                    s += v['value']
                    i += 1
                args['avg'] = s / i

        args['values'] = values
    elif request.method == 'POST':

        max_threshold = None
        min_threshold = None

        if 'max_threshold' in request.form:
            max_threshold = request.form['max_threshold']

        if 'min_threshold' in request.form:
            min_threshold = request.form['min_threshold']

        if max_threshold or min_threshold:
            threshhold_values = db.get_by_threshold(max=max_threshold, min=min_threshold)
        else:
            threshhold_values = []
        # result_values = []
        # if 'min' in threshhold_values:
        #     result_values += threshhold_values['min']
        # if 'max' in threshhold_values:
        #     result_values += threshhold_values['max']
        # print(result_values)
        args['values'] = threshhold_values


    return render_template('index.html', **args)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
