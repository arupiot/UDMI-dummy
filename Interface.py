import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper
from time import sleep
import threading

SPACE_CHAR = 32
TITLE_ROW = 0
AUTOSEND_INFO_ROW = 3
MESSAGE_INFO_ROW = 4
KEYMAP_START_ROW = 5
SENDING_ROW = 8
TOPIC_INFO_START_ROW = 13
BROKER_INFO_START_ROW = 14
EXIT_START_ROW = 16

class Interface():
    def __init__(self, device):
        self.device = device
        self.auto_send = False
        self.auto_send_delay = 0.4
        self.auto_timer_started_at = 0
        self.auto_timer_elapsed = 0
        self.stdscr = None

        self.auto_send_thread = threading.Thread(target=self.autoMessage, args=())
        self.auto_send_thread.start()
        self.auto_send_break = False

        wrapper(self.main)

    def cleanup(self):
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

    def autoMessage(self):
        while 1:
            if self.auto_send:
                self.sendRandomMessage()
            sleep(self.auto_send_delay)
            if self.auto_send_break: break

    def dynamicKeyPress(self, c):
        for point, val in self.device.value_mapping.items():
            in_char = chr(c)
            if in_char == val[1] and val[0] == 'digital':
                self.cleanup()
                msg = self.device.generateMessage(point)
                self.device.broker.sendMessage(self.device.pub_topic, msg)
                self.cleanup()
                self.stdscr.addstr(SENDING_ROW, 0, "Last sent: " + str(msg))
                return True
        return False

    def sendRandomMessage(self):
        self.cleanup()
        msg = self.device.generateMessage()
        self.device.broker.sendMessage(self.device.pub_topic, msg)
        self.cleanup()
        self.stdscr.addstr(SENDING_ROW, 0, "Last sent: " + str(msg))

    def main(self, stdscr):
        self.stdscr = stdscr
        stdscr.addstr(TITLE_ROW, 0, "In a world of fancy interfaces, welcome to the UDumMI!")
        stdscr.addstr(AUTOSEND_INFO_ROW, 0, "Press the space bar to autosend")
        stdscr.addstr(MESSAGE_INFO_ROW, 0, "Press (or hold) 's' to send a random message" )

        # printing key mapping
        keymap_row = KEYMAP_START_ROW

        for point, val in self.device.value_mapping.items():
            if val[0] == 'digital':
                stdscr.addstr(keymap_row, 0, "Press '" + str(val[1]) +"' to toggle '" + str(point) + "' between 0->100")
                keymap_row += 1

        stdscr.addstr(TOPIC_INFO_START_ROW+keymap_row, 0, "Sending on MQTT topic: '" + str(self.device.pub_topic) + "'")
        stdscr.addstr(BROKER_INFO_START_ROW+keymap_row, 0, "to broker: " + str(self.device.broker.host) + " on port: " + str(self.device.broker.port))
        stdscr.addstr(EXIT_START_ROW+keymap_row, 0, "Press 'q' to exit")

        while 1:
            c = stdscr.getch()

            if self.dynamicKeyPress(c):
                # Message sending logic is done in the method...
                pass
            elif c == ord('s'):
                self.sendRandomMessage()
            elif c == SPACE_CHAR:
                self.auto_send = not self.auto_send
                if self.auto_send:
                    self.cleanup()
                    stdscr.addstr(AUTOSEND_INFO_ROW, 0, "Autosend is ON! Press space to turn it off")
                    self.cleanup()
                if not self.auto_send:
                    self.cleanup()
                    stdscr.addstr(AUTOSEND_INFO_ROW, 0, "Press the space bar to autosend")
                    self.cleanup()
            elif c == ord('q'):
                self.auto_send_break = True
                del self.device
                break  # Exit the while loop

    def __del__(self):
        curses.endwin()
