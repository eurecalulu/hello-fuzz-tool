import sys
sys.path.append("..")
# sys.path.append("")

import random
from src.mutation import *


def choose_seeds(seeds, weights):
    """
    选择种子列表
    :param seeds: 种子列表
    :param weight: 种子选择概率
    :return: 两个种子
    """
    x = random.choices(seeds, weights=weights, k=2)
    return x[0], x[1]

def schedule(seeds, weights, times):
    """
    schedule模糊测试调度器
    :param seeds: 种子
    :param weight: 种子选择概率
    :param times: 变异次数
    :return: 变异后的字符串列表
    """

    param = Param()
    param.input_str_1, param.input_str_2 = choose_seeds(seeds, weights)

    # 定义函数映射
    not_empty_function_list = [
        char_ins,
        Havoc,
        Splice,
        char_change,
        repeat_pattern,
        case_conversion,
        boundary_change,
    ]

    function_list = [
        char_flip,
        char_ins,
        char_del,
        Havoc,
        Splice,
        char_change,
        repeat_pattern,
        case_conversion,
        boundary_change,
    ]

    result = []
    for _ in range(times):
        # 选择操作
        if(param.input_str_1 == ""):
            op = random.choice(not_empty_function_list)
        else:
            op = random.choice(function_list)

        # 参数设置
        param.n = random.randint(1, max(1, len(param.input_str_1)))
        param.L = random.randint(param.n, param.n * 3)
        param.S = random.randint(1, max(1, len(param.input_str_1)))
        param.K = random.randint(1, max(1, len(param.input_str_1)))
        param.mode = random.randint(0, 2)

        # 创建上下文
        context = Context(op)
        
        # 调用变异函数并保存结果
        result.append(context.mutation(param))
        
    return list(set(result))

if __name__ == "__main__":
    print(schedule(["abcABC"], [1], 1000))