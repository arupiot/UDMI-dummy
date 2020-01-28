from datetime import datetime
import json
import random
import logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('UDumMI')

class UDumMI():
    def __init__(self, broker):
        self.pub_topic = 'dittick/UDMIduino-000/events'
        self.sub_topic = 'dittick/UDMIduino-000/lum-value'
        self.message_config = {
            "version": 1,
            "timestamp": "0",
            "points": {
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
        }
        self.broker = broker

    def generateMessage(self):
        self.message_config["timestamp"] = str(datetime.now())
        self.message_config["points"]["lux_level"]["present_value"] = random.uniform(50, 60)
        self.message_config["points"]["lum_value"]["present_value"] = random.uniform(95, 100)
        self.message_config["points"]["dimmer_value"]["present_value"] = random.uniform(20, 30)

        return json.dumps(self.message_config)

    def __del__(self):
        LOGGER.info("UDumMI Died!")
        del self.broker