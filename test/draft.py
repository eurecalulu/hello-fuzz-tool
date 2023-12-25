import time
import curses

def print_current_time_and_count(stdscr):
    count = 0
    while True:
        stdscr.clear()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output = f"Count: {count}\n=={current_time}=="
        stdscr.addstr(0, 0, output)
        stdscr.refresh()
        count += 1
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(print_current_time_and_count)
