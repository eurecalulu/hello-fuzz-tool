import random


def choose_seeds(seeds):
    """
    选择种子列表
    :param seeds: 种子列表
    :return: 两个种子
    """
    return seeds[0], seeds[0]

def random_chr():
    """
    随机生成字符
    :return: 字符
    """
    x = random.randint(1, 127)
    if(x == 92): return "\\"
    else: return chr(x)

def schedule(seeds, times):
    """
    schedule模糊测试调度器
    :param seeds: 种子列表
    :param times: 变异次数
    :return: 变异后的字符串列表
    """
    input_str_1, input_str_2 = choose_seeds(seeds)

    result = []
    for _ in range(times):
        op = random.randint(0, 6)
        if op == 0 and 0 < len(input_str_1):
            L = random.randint(1, 10)
            S = random.randint(1, min(L, len(input_str_1)))
            result.append(char_flip(input_str_1, random.randint(0, 10), L, S))
        elif op == 1:
            result.append(char_ins(input_str_1, random.randint(0, 10), random.randint(0, 10)))
        elif op == 2:
            result.append(char_del(input_str_1, random.randint(0, 10), random.randint(0, 10)))
        elif op == 3:
            result.append(Havoc(input_str_1))
        elif op == 4:
            result.append(Splice(input_str_1, input_str_2))
        elif op == 5:
            result.append(char_change(input_str_1, random.randint(0, 10)))
        elif op == 6:
            result.append(bit_revert(input_str_1, random.randint(0, 10)))
        elif op == 7:
            result.append(repeat_pattern(input_str_1, random.randint(1, 10), random.randint(1, len(input_str_1))))
        elif op == 8:
            result.append(case_conversion(input_str_1, random.randint(0, 2)))
        elif op == 9:
            result.append(boundary_change(input_str_1, random.randint(0, 2)))
        
    return result


def char_flip(input_str, n, L, S):
    """
    CharFlip模糊测试算子
    :param input_str: 输入字符串
    :param n: 增量
    :param L: 总长
    :param S: 步长
    :return: 翻转后的字符串
    """
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

def char_ins(input_str, n, K):
    """
    CharIns模糊测试算子
    :param input_str: 输入字符串
    :param n: 位置数
    :param K: 字符个数
    :return: 插入字符后的字符串
    """
    for _ in range(n):
        # 获取字符串长度
        str_len = len(input_str)

        # 计算插入的位置
        ins_pos = random.randint(0, str_len)
    
        # 插入字符
        ins_chars = [random_chr() for _ in range(K)]  # 随机生成小写字母作为插入字符
        input_str = input_str[:ins_pos] + "".join(ins_chars) + input_str[ins_pos:]

    return input_str

def char_del(input_str, n, K):
    """
    CharDel模糊测试算子
    :param input_str: 输入字符串
    :param n: 位置数
    :param K: 字符个数
    :return: 删除字符后的字符串
    """
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

def Havoc(input_str):
    """
    Havoc模糊测试算子
    :param input_str: 输入字符串
    :return: 随机执行所有的基础算子若干次
    """
    times = random.randint(0, 100)
    for _ in range(times):
        op = random.randint(0, 2)
        if op == 0 and 0 < len(input_str):
            # 执行CharFlip算子，如果input_str为空，该语句会报错
            L = random.randint(1, 10)
            S = random.randint(1, min(L, len(input_str)))
            input_str = char_flip(input_str, random.randint(0, 10), L, S)
        elif op == 1:
            input_str = char_ins(input_str, random.randint(0, 10), random.randint(0, 10))
        elif op == 2:
            input_str = char_del(input_str, random.randint(0, 10), random.randint(0, 10))

    return input_str
    

def Splice(input_str_1, input_str_2):
    """
    Splice模糊测试算子
    :param input_str_1: 输入字符串1
    :param input_str_2: 输入字符串2
    :return: 拼接后的字符串
    """
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
    
def char_change(input_str, n):
    """
    char_change模糊测试算子，挑选n个位置将其字符替换为随机字符
    :param input_str: 输入字符串
    :param n: 位置数
    :return: 替换后的字符串
    """
    input_list = list(input_str)

    for _ in range(n):
        # 获取字符串长度
        list_len = len(input_list)
        
        pos = random.randint(0, list_len - 1)

        # 替换字符
        input_list[pos] = random_chr()

    return "".join(input_list)

def bit_revert(input_str, n):
    """
    bit_revert模糊测试算子，挑选n个位置进行比特翻转
    :input input_str: 输入字符串
    :param n: 位置数
    :return: 比特翻转后的字符串
    """
    if(n >= len(input_str)):
        n = len(input_str)

    input_list = list(input_str)

    posList = random.sample(range(len(input_str)), n)
    for pos in posList:
        input_list[pos] = chr(127 - ord(input_list[pos]))

    return "".join(input_list)

def repeat_pattern(input_str, n, L):
    """
    repeat_pattern模糊测试算子，重复输入字符串n次
    :param input_str: 输入字符串
    :param n: 重复次数
    :param L: 重复模式长度
    :return: 重复后的字符串
    """
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

def case_conversion(input_str, mode):
    """
    case_conversion模糊测试算子, 转换字符串大小写
    :param input_str: 输入字符串
    :param mode: 转换模式。0: 全部大写；1: 全部小写；2: 随机大小写
    :return: 转换后的字符串
    """
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

def boundary_change(input_str, mode):
    """
    bounary_change模糊测试算子，将字符串的边界字符添加随机字符
    :param input_str: 输入字符串
    :param mode: 边界模式。0为首字符，1为尾字符，2为首尾字符
    :return: 添加边界字符后的字符串
    """
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





if __name__ == "__main__":
    print(char_ins("123456789", 2, 7))
