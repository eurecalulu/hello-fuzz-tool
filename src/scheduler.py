import random


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
    input_str_1, input_str_2 = choose_seeds(seeds)

    result = []
    for _ in range(times):
        op = random.randint(0, 4)
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
            temp_list[idx] = chr(ord(temp_list[idx]) + n)
        
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
        ins_chars = [chr(random.randint(0, 256)) for _ in range(K)]  # 随机生成小写字母作为插入字符
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

if __name__ == "__main__":
    print(char_ins("123456789", 2, 7))
