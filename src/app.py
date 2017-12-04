from flask import Flask, request, render_template, url_for
from cron import Cron

import time

app = Flask(__name__)

cron = Cron()
@cron.add_task(minute=2)
def save_values():
    print("Saving!")

@app.route('/')
def index():
    args = {
        't': time.time
    }
    return render_template('index.html', **args)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
