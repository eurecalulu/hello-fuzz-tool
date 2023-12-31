import math
import sys
sys.path.append("")

from config.config import alpha
class Seed:
    def __init__(self, name, percent, cover_path, output, error, exec_ms):
        self.name = name
        self.percent = percent
        self.cover_path = cover_path
        self.output = output
        self.error = error

        # 有效变异次数，初始值为1
        self.valid_mutation_cnt = 1

        # 启发式计算power的参数
        self.exec_ms = exec_ms
        self.handicap = 16
        self.depth = sum(1 for x in cover_path if x == '1')

        self.cal_power()

    def cal_power(self):
        self.power = 5

        if(self.exec_ms <= 100):
            self.power *= 2.0
        elif(100 < self.exec_ms <= 200):
            self.power *= 1.5

        if(self.handicap > 4):
            self.power *= 4
            self.handicap -= 4
        elif(self.handicap >= 2):
            self.power *= 2
            self.handicap -= 1

        if(0 <= self.depth and self.depth <= 3):
            pass
        elif(4 <= self.depth and self.depth <= 7):
            self.power *= 2
        elif(8 <= self.depth and self.depth <= 13):
            self.power *= 3
        elif(14 <= self.depth and self.depth <= 25):
            self.power *= 4
        else:
            self.power *= 5

        self.power = int(self.power)

    def set_exec_ms(self, exec_ms):
        self.exec_ms = exec_ms

    def add_one_valid_mutation_cnt(self):
        self.valid_mutation_cnt += 1

    def set_power(self, power):
        self.power = power

    def get_valid_mutation_cnt(self):
        return self.valid_mutation_cnt

    def get_name(self):
        return self.name
    
    def get_percent(self):
        return self.percent

    def get_cover_path(self):
        return self.cover_path

    def get_output(self):
        return self.output

    def get_error(self):
        return self.error
    
    def get_power(self):
        return self.power
    
    def get_weight(self, T):
        valid_mutation_weight = (1.0 / (1.0 + math.exp(-T * self.valid_mutation_cnt)) - 0.5) * 2
        return valid_mutation_weight * alpha + self.percent * (1.0 - alpha)

    def __str__(self) -> str:
        return f'seed: {self.name}, power: {self.power}, percent: {self.percent}, cover_path: {self.cover_path}, error: {self.error}'

    
