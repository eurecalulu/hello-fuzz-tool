import math
import sys
sys.path.append("")

from config.config import alpha
class Seed:
    def __init__(self, name, percent, cover_path, output, error):
        self.name = name
        self.percent = percent
        self.cover_path = cover_path
        self.output = output
        self.error = error

        # 有效变异次数，初始值为1
        self.valid_mutation_cnt = 1 

        self.power = self.cal_power()

    def cal_power(self):
        return 10
    
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

    
