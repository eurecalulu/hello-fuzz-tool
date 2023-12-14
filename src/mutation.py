import random
from typing import Any

# 变异算子会使用到的参数
class Param:
    input_str_1 = ""
    input_str_2 = ""
    n = 0
    L = 0
    S = 0
    K = 0
    mode = 0

# 策略模式的上下文
class Context:
    def __init__(self, strategy):
        self.mStrategy = strategy
    
    def mutation(self, param):
        return self.mStrategy(param)


def random_chr():
    """
    随机生成字符
    :return: 字符
    """
    x = random.randint(1, 127)
    if(x == 92): return "\\"
    else: return chr(x)

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
        print("input_str should not be empty")
        return input_str

    if(len(input_str) < S):
        print("S should be less than the length of input string")
        return input_str
    
    if(S == 0):
        print("S should be greater than 0")
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
            temp_list[idx] = chr((ord(temp_list[idx]) + n) % 127 + 1) # 不需要空字符
        
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
    :return: 插入字符后的字符串
    """
    input_str, n, K = param.input_str_1, param.n, param.K

    for _ in range(n):
        # 获取字符串长度
        str_len = len(input_str)

        # 计算插入的位置
        ins_pos = random.randint(0, str_len)
    
        # 插入字符
        ins_chars = [random_chr() for _ in range(K)]  # 随机生成小写字母作为插入字符
        input_str = input_str[:ins_pos] + "".join(ins_chars) + input_str[ins_pos:]

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

    if(n * K >= len(input_str)):
        return ""

    for _ in range(n):
        # 获取字符串长度
        str_len = len(input_str)

        # 计算删除的位置
        del_pos = random.randint(0, str_len - K)
    
        # 删除字符
        input_str = input_str[:del_pos] + input_str[del_pos + K:]

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
    function_map = {
        0: char_flip,
        1: char_ins,
        2: char_del
    }

    times = random.randint(0, 100)
    for _ in range(times):
        # 选择操作
        op = random.randint(0, 2)

        # 参数设置
        mParam.input_str_1 = input_str
        mParam.n = random.randint(1, 10)
        mParam.L = random.randint(1, 10)
        mParam.S = random.randint(1, max(1, len(mParam.input_str_1)))
        mParam.K = random.randint(1, 10)

        # 创建上下文
        context = Context(function_map[op])

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
    :return: 替换后的字符串
    """
    input_str, n = param.input_str_1, param.n

    input_list = list(input_str)

    for _ in range(n):
        # 获取字符串长度
        list_len = len(input_list)
        
        pos = random.randint(0, list_len - 1)

        # 替换字符
        input_list[pos] = random_chr()

    return "".join(input_list)

def bit_revert(param):
    """
    bit_revert模糊测试算子，挑选n个位置进行比特翻转
    :input input_str: 输入字符串
    :param n: 位置数
    :return: 比特翻转后的字符串
    """
    input_str, n = param.input_str_1, param.n

    if(n >= len(input_str)):
        n = len(input_str)

    input_list = list(input_str)

    posList = random.sample(range(len(input_str)), n)
    for pos in posList:
        input_list[pos] = chr(127 - ord(input_list[pos]))

    return "".join(input_list)

def repeat_pattern(param):
    """
    repeat_pattern模糊测试算子，重复输入字符串n次
    :param input_str: 输入字符串
    :param n: 重复次数
    :param L: 重复模式长度
    :return: 重复后的字符串
    """
    input_str, n, L = param.input_str_1, param.n, param.L

    if(n < 1):
        print("n should be greater than 0")
        return input_str
    
    if(L < 1):
        print("L should be greater than 0")
        return input_str

    if(L > len(input_str)):
        print("L should be less than the length of input string")
        return input_str

    # 随机选择一个位置插入重复模式
    insertion_point = random.randint(0, len(input_str) - L)

    # 提取重复模式
    pattern = input_str[insertion_point: insertion_point + L]

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
    :return: 添加边界字符后的字符串
    """
    input_str, mode = param.input_str_1, param.mode

    if(mode not in [0, 1, 2]):
        print("mode should be 0, 1 or 2")
        return input_str

    if mode == 0:
        input_str = random_chr() + input_str
    elif mode == 1:
        input_str = input_str + random_chr()
    elif mode == 2:
        input_str = random_chr() + input_str + random_chr()

    return input_str
