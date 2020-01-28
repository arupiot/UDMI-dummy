from time import sleep
import paho.mqtt.client as mqtt
import logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('Broker')

class Broker():
    def __init__(self):
        self.broker_host = "localhost"
        self.broker_port = 3389
        mqtt.Client.connected_flag = False  # create flag in class
        self.client = mqtt.Client("DitTICK Dummy Gateway")  # create new instance
        self.client.on_connect = self.on_connect  # bind call back function
        self.client.on_message = self.on_message #attach function to callback
        print("Connecting to broker:", self.broker_host, "on port:", self.broker_port)
        self.client.connect(self.broker_host, self.broker_port, 60)  # connect to broker
        self.client.loop_start()
        while not self.client.connected_flag:  # wait in loop
            LOGGER.info("Waiting for connection...")
            sleep(1)

    def messageLoop(self, topic, message_gen_cb):
        while(True):
            self.sendMessage(topic, message_gen_cb())
            sleep(0.4)

    def sendMessage(self, topic, message):
        self.client.publish(topic, message)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.connected_flag = True  # set flag
            LOGGER.info("Connected OK!")
        else:
            print("Bad connection Returned code=", rc)

    def on_message(self, client, userdata, message):
        payload = str(message.payload.decode("utf-8"))
        print("message received " ,payload)
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)

    def __del__(self):
        LOGGER.info("Broker died!")
        self.client.loop_stop()  # Stop loop
        self.client.disconnect()  # disconnect
