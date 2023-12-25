import sys
sys.path.append("..")
sys.path.append("")

import random
from config.config import CANDIDATES

# 变异算子会使用到的参数
class Param:
    input_str_1 = ""
    input_str_2 = ""
    n = 0
    L = 0
    S = 0
    K = 0
    mode = 0
    candidates = []

# 策略模式的上下文
class Context:
    def __init__(self, strategy):
        self.mStrategy = strategy
        
    def verify_input(self, input_str):
        return all(c in CANDIDATES for c in input_str)

    def mutation(self, param):
        param.candidates = CANDIDATES
        
        if(self.verify_input(param.input_str_1) == False):
            raise Exception("Context verify input_str_1 failed")

        if(self.verify_input(param.input_str_2) == False):
            raise Exception("Context verify input_str_2 failed")

        return self.mStrategy(param)

def generate(input_str_1, input_str_2, times):
    """
    :param input_str_1: 输入字符串1
    :param input_str_2: 输入字符串2
    :return: 变异后的字符串列表
    """
    # 定义参数
    param = Param()

    # 初始化输入字符串
    param.input_str_1, param.input_str_2 = input_str_1, input_str_2
    
    # 定义函数映射
    not_empty_function_list = [
        char_ins,
        Havoc,
        Splice,
        # char_change,
        # repeat_pattern,
        # case_conversion,
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
        # case_conversion,
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

def random_chr(candidates):
    """
    随机生成字符
    :return: 字符
    """
    return random.choice(candidates)

def char_plus_n(char, candidates, n):
    """
    先在candidates里找char，给char的序号+n，然后返回candidates中的字符
    :param char: 字符
    :param candidates: 候选字符列表
    :param n: 增量
    :return: 字符
    """
    if(char not in candidates):
        raise Exception("char not in candidates")
    
    idx = candidates.index(char)
    new_idx = (idx + n) % len(candidates)
    return candidates[new_idx]


def char_flip(param):
    """
    CharFlip模糊测试算子
    :param input_str: 输入字符串
    :param n: 增量
    :param L: 总长
    :param S: 步长
    :return: 翻转后的字符串
    """
    input_str, n, L, S = param.input_str_1, param.n, param.L, param.S

    if(input_str == ""):
        print("char_flip input_str should not be empty")
        return input_str

    if(len(input_str) < S):
        print("char_flip S should be less than the length of input string")
        return input_str
    
    if(S == 0):
        print("char_flip S should be greater than 0")
        return input_str

    input_list = list(input_str)

    while L >= S:
        # 获取字符串长度
        list_len = len(input_list)
        
        pos = random.randint(0, list_len - S)
    
        # 翻转字符
        temp_list = input_list[pos: pos + S]
        temp_list.reverse()

        # +n
        for idx in range(S):
            temp_list[idx] = char_plus_n(temp_list[idx], param.candidates, n)
        
        # 替换字符串
        input_list[pos: pos + S] = temp_list

        L -= S

    return "".join(input_list)

def char_ins(param):
    """
    CharIns模糊测试算子
    :param input_str: 输入字符串
    :param n: 位置数
    :param K: 字符个数
    :param candiates: 候选字符列表
    :return: 插入字符后的字符串
    """
    input_str, n, K, candiates = param.input_str_1, param.n, param.K, param.candidates

    if(len(input_str) < n):
        # print("n should be less than the length of input string")
        n = len(input_str)
        # print("n is set to %d")

    if(input_str == ""):
        ins_pos_list = [0]
    else:
        ins_pos_list = random.choices(range(len(input_str) + 1), k=n)



    for _ in range(K):
        # 要插入字符
        ins_chars = random_chr(candiates)  # 随机生成小写字母作为插入字符
        
        # 获取字符串长度
        str_len = len(input_str)

        # 计算插入的位置
        ins_pos = random.choice(ins_pos_list)

        # 插入字符
        input_str = input_str[:ins_pos] + ins_chars + input_str[ins_pos:]

    return input_str

def char_del(param):
    """
    CharDel模糊测试算子
    :param input_str: 输入字符串
    :param n: 位置数
    :param K: 字符个数
    :return: 删除字符后的字符串
    """
    input_str, n, K = param.input_str_1, param.n, param.K


    if(input_str == ""):
        print("char_del input_str should not be empty")
        return input_str
    
    if(len(input_str) <= K):
        return input_str

    if(n <= len(input_str)):
        del_pos_list = random.choices(range(len(input_str)), k=n)
    else:
        del_pos_list = [x for x in range(len(input_str))]

    for _ in range(K):
        # 获取字符串长度
        str_len = len(input_str)

        # 计算删除的位置
        del_pos = random.choice(del_pos_list)

        if(del_pos >= str_len):
            del_pos = str_len - 1

        # 删除字符
        input_str = input_str[:del_pos] + input_str[del_pos+1:]
        
    return input_str

def Havoc(param):
    """
    Havoc模糊测试算子
    :param input_str: 输入字符串
    :return: 随机执行所有的基础算子若干次
    """
    input_str = param.input_str_1

    mParam = Param()

    # 定义函数映射
    function_list = [
        char_flip,
        char_ins,
        char_del
    ]

    

    times = random.randint(0, 10)
    for _ in range(times):
        # 选择操作
        if(input_str == ""):
            op = char_ins
        else:
            op = random.choice(function_list)

        # 参数设置
        mParam.input_str_1 = input_str
        mParam.n = random.randint(1, 10)
        mParam.L = random.randint(1, 10)
        mParam.S = random.randint(1, max(1, len(mParam.input_str_1)))
        mParam.K = random.randint(1, 10)

        # 创建上下文
        context = Context(op)

        # 调用变异函数并保存结果
        input_str = context.mutation(mParam)

    return input_str
    

def Splice(param):
    """
    Splice模糊测试算子
    :param input_str_1: 输入字符串1
    :param input_str_2: 输入字符串2
    :return: 拼接后的字符串
    """
    input_str_1, input_str_2 = param.input_str_1, param.input_str_2

    # 将两个种子切分，之后将前后段拼接（遗传算法中的杂交操作）
    str_len_1 = len(input_str_1)
    str_len_2 = len(input_str_2)

    # 计算切分位置
    split_pos_1 = random.randint(0, str_len_1)
    split_pos_2 = random.randint(0, str_len_2)

    if(random.randint(0, 1) == 0):
        return input_str_1[:split_pos_1] + input_str_2[split_pos_2:]
    else:
        return input_str_2[:split_pos_2] + input_str_1[split_pos_1:]
    
def char_change(param):
    """
    char_change模糊测试算子，挑选n个位置将其字符替换为随机字符
    :param input_str: 输入字符串
    :param n: 位置数
    :param candiates: 候选字符列表
    :return: 替换后的字符串
    """
    if(char_change == ""):
        print("char_change input_str should not be empty")
        return ""

    input_str, n, candiates = param.input_str_1, param.n, param.candidates

    input_list = list(input_str)

    for _ in range(n):
        # 获取字符串长度
        list_len = len(input_list)
        
        pos = random.randint(0, list_len - 1)

        # 替换字符
        input_list[pos] = random_chr(candiates)

    return "".join(input_list)

# def bit_revert(param):
#     """
#     bit_revert模糊测试算子，挑选n个位置进行比特翻转
#     :input input_str: 输入字符串
#     :param n: 位置数
#     :return: 比特翻转后的字符串
#     """
#     input_str, n = param.input_str_1, param.n

#     if(n >= len(input_str)):
#         n = len(input_str)

#     input_list = list(input_str)

#     posList = random.sample(range(len(input_str)), n)
#     for pos in posList:
#         if(ord(input_list[pos]) == 127):
#             continue
#         input_list[pos] = chr(127 - ord(input_list[pos]))
    
#     return "".join(input_list)

def repeat_pattern(param):
    """
    repeat_pattern模糊测试算子，重复输入字符串n次
    :param input_str: 输入字符串
    :param n: 重复次数
    :param S: 重复模式长度
    :return: 重复后的字符串
    """
    input_str, n, S = param.input_str_1, param.n, param.S

    if(n < 1):
        print("n should be greater than 0")
        return input_str
    
    if(S < 1):
        print("L should be greater than 0")
        return input_str

    if(S > len(input_str)):
        print("L should be less than the length of input string")
        S = len(input_str)
        print("L is set to be %d")

    # 随机选择一个位置插入重复模式
    insertion_point = random.randint(0, len(input_str) - S)

    # 提取重复模式
    pattern = input_str[insertion_point: insertion_point + S]

    # 在输入字符串中插入重复模式
    input_str = input_str[:insertion_point] + pattern * n + input_str[insertion_point:]

    return input_str

def case_conversion(param):
    """
    case_conversion模糊测试算子, 转换字符串大小写
    :param input_str: 输入字符串
    :param mode: 转换模式。0: 全部大写；1: 全部小写；2: 随机大小写
    :return: 转换后的字符串
    """
    input_str, mode = param.input_str_1, param.mode

    if(mode not in [0, 1, 2]):
        print("mode should be 0, 1 or 2")
        return input_str

    input_list = list(input_str)
    for idx in range(len(input_list)):
        if(input_str[idx].isalpha() == False):
            continue

        if mode == 0:
            input_list[idx] = input_list[idx].upper()
        elif mode == 1:
            input_list[idx] = input_list[idx].lower()
        elif mode == 2:
            if random.randint(0, 1) == 0:
                input_list[idx] = input_list[idx].upper()
            else:
                input_list[idx] = input_list[idx].lower()

    return "".join(input_list)

def boundary_change(param):
    """
    bounary_change模糊测试算子，将字符串的边界字符添加随机字符
    :param input_str: 输入字符串
    :param mode: 边界模式。0为首字符，1为尾字符，2为首尾字符
    :param candiates: 随机字符集
    :return: 添加边界字符后的字符串
    """
    input_str, mode, candidates = param.input_str_1, param.mode, param.candidates


    if(mode not in [0, 1, 2]):
        print("mode should be 0, 1 or 2")
        return input_str

    if mode == 0:
        input_str = random_chr(candidates) + input_str
    elif mode == 1:
        input_str = input_str + random_chr(candidates)
    elif mode == 2:
        input_str = random_chr(candidates) + input_str + random_chr(candidates)

    return input_str