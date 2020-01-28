import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper

class Interface():
    def __init__(self, device):
        self.device = device
        wrapper(self.main)

    def main(self, stdscr):
        stdscr.addstr(0, 0, "In a world of fancy GUIs, welcome to the UDumMI!")
        stdscr.addstr(2, 0, "Press 's' to send a random message")
        stdscr.addstr(4, 0, "Press 'q' to exit")

        while True:
            c = stdscr.getch()
            if c == ord('s'):
                stdscr.clrtoeol()
                stdscr.refresh()
                stdscr.addstr(3, 0, "Sending...")
                self.device.broker.sendMessage(self.device.pub_topic, self.device.generateMessage())
                stdscr.clrtoeol()
                stdscr.refresh()
                stdscr.addstr(3, 0, "Message sent!")
            elif c == ord('q'):
                del self.device
                break  # Exit the while loop
            elif c == curses.KEY_HOME:
                x = y = 0