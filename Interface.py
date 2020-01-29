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
        stdscr.addstr(6, 0, "Sending...")

    def cleandown(self, stdscr, msg):
        stdscr.clrtoeol()
        stdscr.refresh()
        stdscr.addstr(6, 0, "Last sent: " + str(msg))

    def dynamicKeyPress(self, c, stdscr):
        for point, val in self.device.value_mapping.items():
            in_char = chr(c)
            if in_char == val[1] and val[0] == 'digital':
                self.cleanup(stdscr)
                message = self.device.generateMessage(point)
                self.device.broker.sendMessage(self.device.pub_topic, message)
                self.cleandown(stdscr, message)
                return True
        return False


    def main(self, stdscr):
        stdscr.addstr(0, 0, "In a world of fancy interfaces, welcome to the UDumMI!")
        stdscr.addstr(1, 0, "Sending on topic: " + str(self.device.pub_topic))
        stdscr.addstr(4, 0, "Press (or hold) 's' to send a random message" )

        # printing key mapping
        keymap_row = 3

        for point, val in self.device.value_mapping.items():
            if val[0] == 'digital':
                stdscr.addstr(keymap_row, 0, "Press '" + str(val[1]) +"' to toggle '" + str(point) + "' between 0->100")
                keymap_row += 1

        stdscr.addstr(11+keymap_row, 0, "Press 'q' to exit")

        while True:
            c = stdscr.getch()

            if self.dynamicKeyPress(c, stdscr):
                # Message sending logic is done in the method...
                pass
            elif c == ord('s'):
                self.cleanup(stdscr)
                message = self.device.generateMessage()
                self.device.broker.sendMessage(self.device.pub_topic, message)
                self.cleandown(stdscr, message)
            elif c == ord('q'):
                del self.device
                break  # Exit the while loop
            elif c == curses.KEY_HOME:
                x = y = 0
