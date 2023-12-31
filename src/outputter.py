import os
import time
import sys
import pandas as pd


class Outputter:
    def __init__(self):
        self.round = 0
        self.begin_time = time.time()
        self.base_folder_path = "./output/" + time.strftime("%Y-%m-%d %H %M %S", time.localtime()) + "/"
        self.cover_folder_path = self.base_folder_path + "cover/"
        self.error_folder_path = self.base_folder_path + "error/"
        self.seeds_csv_path = self.base_folder_path + "seeds.csv"
        os.mkdir(self.base_folder_path)
        os.mkdir(self.cover_folder_path)
        os.mkdir(self.error_folder_path)

        self.output_idx = 0
        self.init_csv()

    def init_csv(self):
        # 创建数据框
        headers = ["id", "seed", "cover_percent", "error", "output"]

        # 创建数据行
        df = pd.DataFrame(columns=headers)

        # 将数据写回到 CSV 文件
        df.to_csv(self.seeds_csv_path, index=False)

    def clear_console(self):
        sys.stdout.write("\033[2J\033[H")  # ANSI 清屏码
        sys.stdout.flush()

    def output(self, stdscr, cover_path, error_list, seeds_information):
        stdscr.clear()

        self.round += 1
        pass_time = round(time.time() - self.begin_time)

        stdscr.addstr(0, 0, f"Round: {self.round}\n")
        stdscr.addstr(1, 0, f"Pass Time: {pass_time}s\n")
        stdscr.addstr(2, 0, f"Error List: {len(error_list)}\n")
        stdscr.addstr(3, 0, f"Cover Path: {cover_path}\n")
        stdscr.addstr(4, 0, f"Seeds Length: {len(seeds_information)}\n")
        stdscr.refresh()

    def output_to_file(self, seed, path):
        fp = open(path + "SEED" + str(self.output_idx).zfill(10) + ".txt", "w", encoding="utf-8")
        fp.write(seed.get_name())
        fp.close()

    def output_cover(self, seed):
        self.output_to_file(seed, self.cover_folder_path)

    def output_error(self, seed):
        self.output_to_file(seed, self.error_folder_path)

    def output_seed(self, seed):
        # 读取 CSV 文件
        df = pd.read_csv(self.seeds_csv_path)
        
        # 创建新的数据行
        data = ["SEED" + str(self.output_idx).zfill(10), seed.get_name(), seed.get_percent(), seed.get_error(), seed.get_output()]
        new_row = pd.Series(data, index=df.columns)

        # 将新行追加到数据框中
        df = df.append(new_row, ignore_index=True)

        # 将数据写回到 CSV 文件
        df.to_csv(self.seeds_csv_path, index=False)

        self.output_idx += 1

if __name__ == "__main__":
    obj = Outputter()
    # while True:
    #     obj.output("001", [])
    #     time.sleep(0.5)
    