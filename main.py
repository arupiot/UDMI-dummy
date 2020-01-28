from UDumMI import UDumMI
from Interface import Interface
from Broker import Broker

broker = Broker()
device = UDumMI(broker)
Interface(device)
