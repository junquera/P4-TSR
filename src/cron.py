import time
import threading
class Cron():

    def __init__(self):
        self.tasks = []

    def add_task(self, **kwargs):
        if 'minute' in kwargs:
            minute = kwargs['minute']

        def wrapper(f):
            def launch(f, minute):
                while 1:
                    time.sleep(60 * minute)
                    f()
            return threading.Thread(target=launch, args=(f, minute,)).start()

        return wrapper

def thread(f):
    def wrapper():
        threading.Thread(target=f).start()
    return wrapper

@thread
def test():
    time.sleep(2)
    print("test!")
