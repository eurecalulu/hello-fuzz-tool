import random
import sys
sys.path.append("")

from config.config import SCHEDULER_T, SCHEDULER_K, SCHEDULER_T_MIN


class Scheduler:
    def __init__(self) -> None:
        # 模拟退火的温度
        self.T = SCHEDULER_T

        # 模拟退火的降温系统
        self.K = SCHEDULER_K


    def choose_seeds(self, seeds, weights):
        """
        选择种子列表
        :param seeds: 种子列表
        :param weight: 种子选择概率
        :return: 两个种子
        """
        seeds_length= len(seeds)

        if(seeds_length == 0):
            return "", ""
        elif(seeds_length == 1):
            return seeds[0], seeds[0]
        else:
            x = random.choices(seeds, weights=weights, k=2)
            return x[0], x[1]

    def schedule(self, seeds_information):
        """
        schedule模糊测试调度器
        :param seeds_information: 种子对象列表
        :return: 两个种子
        """
        # 计算每个种子的权重
        weights = [x.get_weight(self.T) for x in seeds_information]

        # 模拟退火降温
        if(self.T >= SCHEDULER_T_MIN):    
            self.T = self.K * self.T

        seed_1, seed_2 = self.choose_seeds(seeds_information, weights)
        seed_1.cal_power()
        return seed_1, seed_2

if __name__ == "__main__":
    pass
    # print(schedule(["abcABC"], [1], 1000))