# 种子调度模拟退火算法降温因子
SCHEDULER_K = 0.9

# 种子调度模拟退火初始温度
SCHEDULER_T = 10

# 种子调度模拟退火最低温度
SCHEDULER_T_MIN = 0.01

# 模拟退火权重因子
alpha = 0.2

# 变异后的最大字符长度
LARGEST_LENGTH=5

# 允许使用数字
USE_NUMBER=False

# 允许使用小写字母
USE_LOWER_ALPHABET=True

# 允许使用大写字母
USE_UPPER_ALPHABET=False

# 允许使用全部ASCII字符
USE_ALL_ASCII=False

LOWER_ALPHABET_LIST=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

UPPER_APLPHABET_LIST=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

NUMBER_LIST=['0','1','2','3','4','5','6','7','8','9']

ASCII_LIST=[chr(x) for x in range(1,128)]

CANDIDATES=[]

if(USE_ALL_ASCII):
    CANDIDATES += USE_ALL_ASCII
else:
    if(USE_NUMBER):
        CANDIDATES += NUMBER_LIST
    if(USE_UPPER_ALPHABET):
        CANDIDATES += UPPER_APLPHABET_LIST
    if(USE_LOWER_ALPHABET):
        CANDIDATES += LOWER_ALPHABET_LIST


print("CANDIDATES: ", CANDIDATES)