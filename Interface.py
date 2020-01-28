import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper

class Interface():
    def __init__(self, device):
        self.device = device
        wrapper(self.main)

    def cleanup(self, stdscr):
        stdscr.clrtoeol()
        stdscr.refresh()
        stdscr.addstr(5, 0, "Sending...")

    def cleandown(self, stdscr, msg):
        stdscr.clrtoeol()
        stdscr.refresh()
        stdscr.addstr(5, 0, "Last sent: " + str(msg))

    def main(self, stdscr):
        stdscr.addstr(0, 0, "In a world of fancy interfaces, welcome to the UDumMI!")
        stdscr.addstr(2, 0, "Press 's' to send a random message to topic: " + str(self.device.pub_topic))
        stdscr.addstr(3, 0, "Press 'w' to toggle 'lum_value' between 0->100")
        stdscr.addstr(11, 0, "Press 'q' to exit")

        while True:
            c = stdscr.getch()
            if c == ord('s'):
                self.cleanup(stdscr)
                message = self.device.generateMessage()
                self.device.broker.sendMessage(self.device.pub_topic, message)
                self.cleandown(stdscr, message)
            elif c == ord('w'):
                self.cleanup(stdscr)
                message = self.device.generateMessage("lum_value")
                self.device.broker.sendMessage(self.device.pub_topic, message)
                self.cleandown(stdscr, message)
            elif c == ord('q'):
                del self.device
                break  # Exit the while loop
            elif c == curses.KEY_HOME:
                x = y = 0