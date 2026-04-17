import curses

from motor import Motor

m = Motor()

actions = {
    curses.KEY_UP:    m.forward,
    curses.KEY_LEFT:  m.left,
    curses.KEY_RIGHT: m.right,
    curses.KEY_DOWN: m.back,
    }

speed = 50

def main(window):
    next_key = None
    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY DOWN
            curses.halfdelay(3)
            action = actions.get(key)
            if action is not None:
                action(speed)
            next_key = key
            while next_key == key:
                next_key = window.getch()
            # KEY UP
            m.stop()   
curses.wrapper(main)