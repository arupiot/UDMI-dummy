from datetime import datetime
import json
import random
import logging
import os.path
from os import path

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('UDumMI')

class UDumMI():
    def __init__(self, broker, config_path=None):
        self.pub_topic = 'dittick/UDMIduino-000/events'
        self.sub_topic = 'dittick/UDMIduino-000/lum-value'
        self.message_config = {
                    "version": 1,
                    "timestamp": "0",
                    "points": {}
                }
        self.message_config["points"] = self.buildConfigFromFile(config_path)
        self.broker = broker

    def generateMessage(self):
        self.message_config["timestamp"] = str(datetime.now())

        return json.dumps(self.message_config)

    def buildConfigFromFile(self, config_path):
        if not config_path or not path.exists(config_path):
            # Return the standard dummy device config from https://github.com/arupiot/udmiduino
            LOGGER.info("No JSON config path, using UDMIduino default")
            return {
                    "lux_level": {
                        "present_value": 0
                    },
                    "lum_value": {
                        "present_value": 0
                    },
                    "dimmer_value": {
                        "present_value": 0
                    }
                }

        LOGGER.info("Building pointset from " + str(config_path))
        with open(config_path) as json_file:
            conf = json.load(json_file)

            LOGGER.info("Constructing topic...")
            self.pub_topic = str(conf["namespace"]) + "/" + str(conf["device_name"]) + "/events"
            LOGGER.info("Parsing pointset...")

            new_pointset = {}

            for point in conf["points"]:
                new_point = {str(point["name"]) : { "present_value" : 0 } }
                new_pointset.update(new_point)

        LOGGER.info("Pointset structure: " + str(new_pointset))
        LOGGER.info("Topic: " + self.pub_topic)

        return new_pointset


    def __del__(self):
        LOGGER.info("UDumMI Died!")
        del self.broker