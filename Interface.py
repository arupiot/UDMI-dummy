import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper

class Interface():
    def __init__(self, device):
        wrapper(self.main)

    def main(self, stdscr):
        stdscr.addstr(0, 0, "In a world of fancy GUIs, welcome to the UDumMI!")
        stdscr.addstr(1, 0, "Awaiting control...")
        stdscr.addstr(3, 0, "Press 'q' to exit")

        while True:
            c = stdscr.getch()
            if c == ord('a'):
                stdscr.refresh()
                stdscr.addstr(1, 0, "Toggle the __whatever___       ")
            if c == ord('s'):
                stdscr.refresh()
                stdscr.addstr(1, 0, "Toggle the __whatever else___       ")
            elif c == ord('q'):
                break  # Exit the while loop
            elif c == curses.KEY_HOME:
                x = y = 0