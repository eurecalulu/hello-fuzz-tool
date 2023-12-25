import random
import math

def choose_seeds(seeds, weights):
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

def schedule(seeds_information):
    """
    schedule模糊测试调度器
    :param seeds_information: 种子信息四元组列表(seed, 覆盖率, 覆盖路径, 报错信息)
    :return: 两个种子
    """
    seeds = [x[0] for x in seeds_information]
    weights = [math.exp(x[1]) for x in seeds_information]
    
    return choose_seeds(seeds, weights)

if __name__ == "__main__":
    print(schedule(["abcABC"], [1], 1000))