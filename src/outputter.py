import os
import time
import sys
import curses


class Outputter:
    def __init__(self):
        self.round = 0
        self.begin_time = time.time()

    def clear_console(self):
        sys.stdout.write("\033[2J\033[H")  # ANSI 清屏码
        sys.stdout.flush()

    def output(self,  cover_path, error_list):
        self.clear_console()

        self.round += 1
        pass_time = round(time.time() - self.begin_time)
        
        sys.stdout.write(f"Round: {self.round}\n")
        sys.stdout.write(f"Pass Time: {pass_time}s\n")
        sys.stdout.write(f"Error List: {len(error_list)}\n")
        sys.stdout.write(f"Cover Path: {cover_path}\n")
        
        sys.stdout.flush()

if __name__ == "__main__":
    obj = Outputter()
    while True:
        obj.output("001", [])
        time.sleep(0.5)
    