from datetime import datetime
import json
import random
import logging
import os.path
from os import path

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('UDumMI')

class UDumMI():
    def __init__(self, broker, config_path=None):
        self.pub_topic = 'dittick/UDMIduino-000/events'
        self.sub_topic = 'dittick/UDMIduino-000/lum-value'
        self.config_path = config_path
        self.message_config = {
                    "version": 1,
                    "timestamp": "0",
                    "points": {}
                }
        self.message_config["points"] = self.buildPointsetFromFile(self.config_path)
        self.value_mapping = self.buildValueMappingFromFile(self.config_path)
        self.broker = broker

    def generateMessage(self, point_select=None):
        self.message_config["timestamp"] = str(datetime.now())
        for point, v in self.message_config["points"].items():
            point_type = self.value_mapping[str(point)][0]
            if point_type == "analogue":
                low = self.value_mapping[str(point)][1]
                high =  self.value_mapping[str(point)][2]
                self.message_config["points"][str(point)]["present_value"] = random.uniform(low, high)

            if point_type == "digital" and point_select and point == point_select:
                current_val = self.message_config["points"][str(point)]["present_value"]
                # Toggle a 'digital point'
                if current_val == 100:
                    self.message_config["points"][str(point)]["present_value"] = 0
                if current_val == 0:
                    self.message_config["points"][str(point)]["present_value"] = 100

        return json.dumps(self.message_config)

    def buildValueMappingFromFile(self, config_path):
        LOGGER.info("*** Value Mapping ***")
        if not config_path or not path.exists(config_path):
            LOGGER.info("No JSON config path for value mapper, using UDMIduino default!")
            return {
                "lux_level": ["analogue", 20, 30],
                "lum_value": ["digital", 'w'],
                "dimmer_value": ["analogue", 50, 60]
            }

        with open(config_path) as json_file:
            conf = json.load(json_file)
            new_value_mapping = {}

            for point in conf["points"]:
                LOGGER.info("Processing: " + point["name"])
                if point["digital"] == "true":
                    value_map = { str(point["name"]) : ["digital", str(point["keybinding"]) ] }
                    new_value_mapping.update(value_map)

                if point["digital"] == "false":
                    value_map = { str(point["name"]) : ["analogue", point["analogue"]["low"], point["analogue"]["high"] ] }
                    new_value_mapping.update(value_map)

        LOGGER.info(new_value_mapping)

        return new_value_mapping

    def buildPointsetFromFile(self, config_path):
        LOGGER.info("*** Pointset Building ***")
        if not config_path or not path.exists(config_path):
            # Return the standard dummy device config from https://github.com/arupiot/udmiduino
            LOGGER.info("No JSON config path for pointset builder, using UDMIduino default!")
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
                LOGGER.info("Processing: " + point["name"])
                new_point = {str(point["name"]) : { "present_value" : 0 } }
                new_pointset.update(new_point)

        LOGGER.info("Pointset structure: " + str(new_pointset))
        LOGGER.info("Topic: " + self.pub_topic)

        return new_pointset


    def __del__(self):
        LOGGER.info("UDumMI Died!")