# main.py

# All is called from here

# include standard modules
import argparse
from UDumMI import UDumMI
from Interface import Interface
from Broker import Broker
import logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('ROOT')

parser = argparse.ArgumentParser()
parser.add_argument("--interface", "-i", help="For configurations with controllable points, launch the 'interface'", action="store_true")
parser.add_argument("--config", "-c", help="Path to the JSON config. If blank, revert to UDMIduino format")
args = parser.parse_args()

broker = Broker()
device = UDumMI(broker)

# check for --interface
if args.interface:
    LOGGER.info("Launching interface...")
    Interface(device)
else:
    LOGGER.info("Interface disabled, sending random stuff...")
    device.broker.messageLoop(device.pub_topic, device.generateMessage)
