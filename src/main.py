from xiPy.xively_connection_parameters import XivelyConnectionParameters
from xiPy.xively_client import XivelyClient
from xiPy.xively_error_codes import XivelyErrorCodes
import credentials
max_attempts = 3

def attempt_gen():
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        yield attempt

def on_connect_finished(client,result):
    if result == XivelyErrorCodes.XI_STATE_OK :
        print("[SUCCESS] Connected to Xively")

    else :
        try:
            attempt_number = next(attempt_gen())
        except StopIteration:
            print("   [FAIL] Unable to connect after %d attempts." % max_attempts)
            sys.exit(-1)
        print("   [INFO] Connection try %d/%d"  % (attempt_number, max_attempts))
        print("  [ERROR] Connection error :" , result)
        print("   [INFO] Reconnecting to the broker ... ")
        client.connect(params)


# XivelyConfig.XI_MQTT_HOSTS = [("junquera.app.xively.com", 8883, True)]
# Client connection

client = XivelyClient()
client.on_connect_finished = on_connect_finished

params = XivelyConnectionParameters()
params.use_websocket = False
params.publish_count_send_time_period = 5

params.device_id = credentials.xively['device_id']
params.username = credentials.xively['device_id']
params.password = credentials.xively['password']

print("   [INFO] ClientID: %s" %(params.client_id))
print("   [INFO] Username: %s" %(params.username))
print("   [INFO] Password: %s" %(params.password))
print("   [INFO] Connecting to Xively...")

client.connect(params)
client.join()

# client.subscribe('/_updates/fields')
