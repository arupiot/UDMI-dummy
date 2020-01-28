from time import sleep
import paho.mqtt.client as mqtt
from UDumMI import UDumMI

BROKER = "localhost"
BROKER_PORT = 3389
DUMMY_DEVICE = UDumMI()
UDMIDUINO_PUB_TOPIC = 'dittick/UDMIduino-000/events'
UDMIDUINO_SUB_TOPIC = 'dittick/UDMIduino-000/lum-value'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    print("message received " ,payload)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


mqtt.Client.connected_flag = False  # create flag in class
client = mqtt.Client("DitTICK Dummy Gateway")  # create new instance
client.on_connect = on_connect  # bind call back function
client.on_message = on_message #attach function to callback
client.loop_start()

print("Connecting to broker ", BROKER)
client.connect(BROKER, BROKER_PORT, 60)  # connect to broker

# Subscribe to the topic from ditto (or elsewhere)

while not client.connected_flag:  # wait in loop
    print("In wait loop")
    sleep(1)

print("Subscribing to LED toggle topic... ")
client.subscribe(UDMIDUINO_SUB_TOPIC)

print("in Main Loop")
print("Publishing...")

while(True):
    ret = client.publish(UDMIDUINO_PUB_TOPIC, DUMMY_DEVICE.generateMessage())
    sleep(0.4)

client.loop_stop()  # Stop loop
client.disconnect()  # disconnect
