from datetime import datetime
import json
import random

class UDumMI():
    def __init__(self, broker):
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

    def generateMessage(self):
        self.message_config["timestamp"] = str(datetime.now())
        self.message_config["points"]["lux_level"]["present_value"] = random.uniform(50, 60)
        self.message_config["points"]["lum_value"]["present_value"] = random.uniform(95, 100)
        self.message_config["points"]["dimmer_value"]["present_value"] = random.uniform(20, 30)

        return json.dumps(self.message_config)