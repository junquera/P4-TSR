import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import ssl

import requests

from app.cron import Cron
import json

# https://junquera.app.xively.com/devices/1a8d1a92-dbbd-4230-8d85-5f2a87d12734
# https://developer.xively.com/docs/mqtt-glossary#section-client
# https://developer.xively.com/docs/device-authentication-methods
# https://www.eclipse.org/paho/clients/python/docs/
# https://developer.xively.com/v1.0/docs/storing-timeseries-data
# https://developer.xively.com/reference#xively-intro

from app.config import xiv_data

tls = {
    'ca_certs': "/etc/ssl/certs/ca-certificates.crt",
    'tls_version': ssl.PROTOCOL_TLSv1
}

login_url = "https://id.xively.com/api/v1/auth/login-user"


class Xively():


    def __init__(self):
        cron = Cron()

        if self.login():
            cron.add_task(minute=25)(self.login)
        else:
            raise Exception("Error al iniciar sesión en Xively con el usuario %s" % xiv_data['login_username'])

    def login(self):
        payload = {
                "emailAddress" : xiv_data['login_username'],
                "password" : xiv_data['login_password'],
                "accountId": xiv_data['account_id'],
                "renewalType": "short"
            }

        response = requests.request("POST", login_url, data=payload)

        if response.status_code == 200:
            self.jwt = json.loads(response.text)['jwt']
            return True
        else:
            self.jwt = None
            return False

    def publish_random_value_mqtt(self, v, time=""):
        publish.single(
            xiv_data['topic'],
            payload=(time + ",Value,%f," % v),
            hostname="broker.xively.com",
            client_id=xiv_data['username'],
            auth=xiv_data,
            tls=tls,
            port=8883,
            protocol=mqtt.MQTTv311
        )

    def retrieve_random_values_http(self, page_size=100):
        if not self.jwt:
            self.login()

        # https://developer.xively.com/reference#sending-timeseries-data
        req = requests.get('https://timeseries.xively.com:443/api/v4/data/' + xiv_data['topic'] + '/latest?pageSize=%d' % page_size, headers={
        'authorization': "Bearer %s" % self.jwt
        })
        if req.status_code != 200:
            return []

        xiv_results = json.loads(req.text)['result']
        results = []
        for result in xiv_results:
            v_aux = {
                'value': result['numericValue'],
                'date': result['time']
            }
            results.append(v_aux)

        return results


    def run_regular():
        def on_message(client, userdata, msg):
            print(client)
            print(msg.topic+" "+str(msg.payload))

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe('xi/blue/v1/ad4935ed-01d5-4454-b322-7e425d644612/d/cee0d2bd-136a-4378-b7e3-760086e8d265/_log')

        client = mqtt.Client('cee0d2bd-136a-4378-b7e3-760086e8d265', clean_session=False)
        client.on_message = on_message
        client.on_connect = on_connect
        client.username_pw_set(xiv_data['device_id'], password=xiv_data['device_password'])
        client.tls_set(tls['ca_certs'], tls_version=ssl.PROTOCOL_TLSv1_2)

        client.connect('broker.xively.com', port=8883)

        # client.loop_forever()

        client.publish('xi/blue/v1/ad4935ed-01d5-4454-b322-7e425d644612/d/cee0d2bd-136a-4378-b7e3-760086e8d265/_log', payload='paho!')
        # client.disconnect()
        #
        # client.loop_stop()
