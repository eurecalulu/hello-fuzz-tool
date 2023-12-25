import time
import curses

def print_current_time_and_count(stdscr):
    count = 0
    while True:
        global AA
        stdscr.clear()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output = f"Count: {count}\n=={current_time}=={AA}"
        stdscr.addstr(0, 0, output)
        stdscr.refresh()
        count += 1
        time.sleep(1)

if __name__ == "__main__":
    AA = 10
    curses.wrapper(print_current_time_and_count)
    for x in range(10):
        AA += 1
        time.sleep(1)
