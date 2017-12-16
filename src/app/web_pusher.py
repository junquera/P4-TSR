import pusher
from app.config import push_data
# https://dashboard.pusher.com/apps/446452/getting_started
class WebPusher():

    def __init__(self):
        self.pusher_client = pusher.Pusher(**push_data)

    def push_message(self, message):
        self.pusher_client.trigger('my-channel', 'my-event', {'message': message})
