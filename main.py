# main.py

# All is called from here

INTERFACE = False


from UDumMI import UDumMI
from Interface import Interface
from Broker import Broker
import logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('ROOT')

broker = Broker()
device = UDumMI(broker)

if INTERFACE:
    LOGGER.info("Launching interface...")
    Interface(device)
elif not INTERFACE:
    LOGGER.info("Interface disabled, sending random stuff...")
    device.broker.messageLoop(device.pub_topic, device.generateMessage)
