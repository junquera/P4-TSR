from flask import Flask, request, render_template, url_for
from app.cron import Cron

from app.almacenamiento import Almacenamiento
from app.obtain import get_a_value

import time

import datetime

from app.web_pusher import WebPusher
import threading

wp = WebPusher()

db = Almacenamiento()

app = Flask(__name__)

def format_datetime(value, format='medium'):
    if type(value) == datetime.datetime:
        return value
    else:
        if value[-1] == 'Z':
            value = value[:-1]
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

app.jinja_env.filters['datetime'] = format_datetime

cron = Cron()
@cron.add_task(minute=2, fast_boot=True)
def save_value():
    db.add_value(get_a_value())

# @cron.add_task(minute=0.1)
# def alert():
#     wp.push_message("prueba")

def check_umbral(max_threshold, min_threshold):
    result = {}
    while (max_threshold and not 'max' in result) or (min_threshold and not 'min' in result):
        v = get_a_value()

        if max_threshold and not 'max' in result:
            if max_threshold:
                if v > max_threshold:
                    result['max'] = v
                    wp.push_message("Umbral máximo %d superado %f" % (max_threshold, v))
                    print("Umbral máximo %d superado %f" % (max_threshold, v))
            if min_threshold:
                if v < min_threshold and not 'min' in result:
                    result['min'] = v
                    wp.push_message("Umbral mínimo %d superado %f" % (min_threshold, v))
                    print("Umbral mínimo %d superado %f" % (min_threshold, v))

        time.sleep(1)

@app.route('/umbral_async', methods=['POST'])
def umbral_async():
    if request.method == 'POST':

        max_threshold = None
        min_threshold = None

        if 'max_threshold' in request.form:
            try:
                max_threshold = float(request.form['max_threshold'])
            except:
                pass

        if 'min_threshold' in request.form:
            try:
                min_threshold = float(request.form['min_threshold'])
            except:
                pass

        # TODO Cellery?
        threading.Thread(target=check_umbral, args=(max_threshold, min_threshold)).start()

        return "OK", 200

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
            try:
                max_threshold = float(request.form['max_threshold'])
            except:
                pass

        if 'min_threshold' in request.form:
            try:
                min_threshold = float(request.form['min_threshold'])
            except:
                pass

        if max_threshold or min_threshold:
            threshhold_values = db.get_by_threshold(max=max_threshold, min=min_threshold)
        else:
            threshhold_values = []

        args['values'] = threshhold_values


    return render_template('index.html', **args)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
