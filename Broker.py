from time import sleep
import paho.mqtt.client as mqtt

# print("Connecting to broker ", BROKER)
# client.connect(BROKER, BROKER_PORT, 60)  # connect to broker

# # Subscribe to the topic from ditto (or elsewhere)

# while not client.connected_flag:  # wait in loop
#     print("In wait loop")
#     sleep(1)

# print("Subscribing to LED toggle topic... ")
# client.subscribe(UDMIDUINO_SUB_TOPIC)

# print("in Main Loop")
# print("Publishing...")

# while(True):
#     ret = 
#     sleep(0.4)

class Broker():
    def __init__(self):
        self.broker_host = "localhost"
        self.broker_port = 3389
        self.udmiduino_pub_topic = 'dittick/UDMIduino-000/events'
        self.udmiduino_sub_topic = 'dittick/UDMIduino-000/lum-value'
        mqtt.Client.connected_flag = False  # create flag in class
        self.client = mqtt.Client("DitTICK Dummy Gateway")  # create new instance
        self.client.on_connect = self.onConnect  # bind call back function
        self.client.on_message = self.onMessage #attach function to callback
        self.client.loop_start()


    def sendMessage(self):
        self.client.publish(UDMIDUINO_PUB_TOPIC, DUMMY_DEVICE.generateMessage())

    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True  # set flag
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)

    def onMessage(self, client, userdata, message):
        payload = str(message.payload.decode("utf-8"))
        print("message received " ,payload)
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)

    def __del__(self):
        self.client.loop_stop()  # Stop loop
        self.client.disconnect()  # disconnect
