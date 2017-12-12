import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import ssl

from obtain import get_a_value

auth = {
    'account_id': 'ad4935ed-01d5-4454-b322-7e425d644612',
    'username': 'cee0d2bd-136a-4378-b7e3-760086e8d265',
    'password': '/2sI17f4lxo6dc3nGIxpHrZO3rbYjj8DsafJNuYr5ZI='
}

tls = {
    'ca_certs': "/etc/ssl/certs/ca-certificates.crt",
    'tls_version': ssl.PROTOCOL_TLSv1
}

topic = "xi/blue/v1/ad4935ed-01d5-4454-b322-7e425d644612/d/cee0d2bd-136a-4378-b7e3-760086e8d265/random_values"

def publish_random_value(v):
    publish.single(
        topic,
        payload=",Value,%f," % v,
        hostname="broker.xively.com",
        client_id="cee0d2bd-136a-4378-b7e3-760086e8d265",
        auth=auth,
        tls=tls,
        port=8883,
        protocol=mqtt.MQTTv311
    )

publish_random_value(get_a_value())

def retrieve_random_values():
    # https://developer.xively.com/reference#sending-timeseries-data
    pass

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
    client.username_pw_set(auth['device_id'], password=auth['device_password'])
    client.tls_set(tls['ca_certs'], tls_version=ssl.PROTOCOL_TLSv1_2)

    client.connect('broker.xively.com', port=8883)



    client.loop_forever()

    client.publish('xi/blue/v1/ad4935ed-01d5-4454-b322-7e425d644612/d/cee0d2bd-136a-4378-b7e3-760086e8d265/_log', payload='paho!')
    #
    # client.disconnect()
    #
    # client.loop_stop()
