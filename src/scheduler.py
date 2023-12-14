import sys
sys.path.append("..")

import random
from src.mutation import *


def choose_seeds(seeds):
    """
    选择种子列表
    :param seeds: 种子列表
    :return: 两个种子
    """
    return seeds[0], seeds[0]

def schedule(seeds, times):
    """
    schedule模糊测试调度器
    :param seeds: 种子列表
    :param times: 变异次数
    :return: 变异后的字符串列表
    """

    param = Param()
    param.input_str_1, param.input_str_2 = choose_seeds(seeds)
    
    # 定义函数映射
    function_map = {
        0: char_flip,
        1: char_ins,
        2: char_del,
        3: Havoc,
        4: Splice,
        5: char_change,
        6: bit_revert,
        7: repeat_pattern,
        8: case_conversion,
        9: boundary_change
    }

    result = []
    for _ in range(times):
        # 选择操作
        op = random.randint(0, 9)

        # 参数设置
        param.n = random.randint(1, 10)
        param.L = random.randint(1, 10)
        param.S = random.randint(1, max(1, len(param.input_str_1)))
        param.K = random.randint(1, 10)
        param.mode = random.randint(0, 2)

        # 创建上下文
        context = Context(function_map[op])
        
        # 调用变异函数并保存结果
        result.append(context.mutation(param))
        
    return list(set(result))

if __name__ == "__main__":
    print(schedule(["123", "456"], 200))
