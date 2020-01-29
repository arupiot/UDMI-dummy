# run.py
# All is called from here

import argparse
from UDumMI import UDumMI
from Interface import Interface
from Broker import Broker
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('root')

# Options to control the flow of things
parser = argparse.ArgumentParser()
parser.add_argument("--interface", "-i", help="For configurations with controllable points, launch the 'interface'", action="store_true")
parser.add_argument("--config", "-c", help="Path to the JSON config. If blank, revert to UDMIduino format")
parser.add_argument("--broker_host", "-bh", help="MQTT broker hostname string. If blank, set to 'localhost'")
parser.add_argument("--broker_port", "-bp", help="MQTT broker TCP port. If blank, set to 3389")
args = parser.parse_args()

# Assemble components
broker = Broker(args.broker_host, args.broker_port)
device = UDumMI(broker, args.config)

# Execute
if args.interface:
    LOGGER.info("Launching interface...")
    Interface(device)
else:
    LOGGER.info("Interface disabled, sending random stuff...")
    device.broker.messageLoop(device.pub_topic, device.generateMessage)
