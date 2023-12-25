import subprocess
import os
from scheduler import Scheduler
from generator import generate
from instrumentor import instrument
from outputter import Outputter
from seed import Seed

def compile_java_source(java_file):
    # 使用javac命令编译Java源代码
    proc = subprocess.Popen(['javac', java_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 获取编译输出和错误信息
    stdout, stderr = proc.communicate()  

    if proc.returncode != 0:
        print("Java源代码编译失败")
        print("编译输出: ", stdout.decode())
        print("编译错误: ", stderr.decode())
        exit(1)
    
    print("Java源代码编译成功")

    # class文件名
    class_name = java_file.split("/")[-1].split('.')[0] + ".class"
    
    # class文件路径，windows就是要用//来分割
    class_path = "input\\" + class_name

    # 移动编译后的class文件到根目录，方便后面运行
    os.system("copy " + class_path + " .")

def get_cover_path(output):
    """
    通过输出来来计算覆盖路径
    :param output: 程序运行结果
    :return: 覆盖路径
    """
    if(output == ""):
        return ""

    # 说明产生了错误
    if(output.split('\n')[-1] == ""):
        return output.split('[TARGET]')[-2].split('\n')[-1]

    return output.split('\n')[-1]


def get_percent(cover_path):
    """
    通过输出来来计算覆盖率
    :param cover_path: 覆盖路径
    :return: 覆盖率
    """
    if(cover_path == ""):
        return 0.0
    
    count_dict = {'0': 0, '1': 0}
    for char in cover_path:
        count_dict[char] += 1
    
    total_count = count_dict['0'] + count_dict['1']
    ratio = count_dict['1'] / total_count if total_count != 0 else 0
    return ratio

def update_cover_path(init_cover_path, cover_path):
    """
    更新覆盖路径
    :param init_cover_path: 初始覆盖路径
    :param cover_path: 当前覆盖路径
    :return: 更新后的覆盖路径, 是否更新的标记
    """
    if(init_cover_path == ""):
        return cover_path, True

    if(cover_path == ""):
        return init_cover_path, False

    res_cover_path = ""
    for charA, charB in zip(init_cover_path, cover_path):
        if charA == '1' or charB == '1':
            res_cover_path += '1'
        else:
            res_cover_path += '0'
    return res_cover_path, res_cover_path != init_cover_path

def update_error_list(init_error_list, err):
    """
    更新报错信息列表
    :param init_error_list: 初始报错信息列表
    :param err: 当前报错信息
    :return: 更新后的报错信息列表, 是否更新的标记
    """
    if(err not in init_error_list):
        init_error_list.append(err)
        return init_error_list, True
    else:
        return init_error_list, False

def print_seeds_information(seeds_information):
    print("打印种子信息:")
    for x in seeds_information:
        print(x)

def run_java_command(class_name, input):
    # 启动新进程并重定向输出流和错误流
    java_command = ['java', class_name, input]
    process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 读取输出流和错误流
    output, error = process.communicate()
    # print(output)
    # print(error)
    # print(get_percent(output))
    # if error != b'':
    #     print("ERROR:", error.decode(encoding="gbk"))

    return output.decode(encoding="gbk"), error.decode(encoding="gbk")

if __name__ == "__main__":
    # 先在hellofuzzing-instrument目录下运行 mvn clean package
    
    # 程序路径
    program_path = "./input/Target1.java"
    seeds_path = "./input/seeds.txt"
    # instrument_program_path = "./input/Target1HelloFuzzing.java"
    # class_name = "Target1HelloFuzzing"

    # 程序插装
    instrument_program_path, class_name = instrument(program_path)
    
    # 编译插桩后的程序
    compile_java_source(instrument_program_path)
    
    # 读取种子队列
    seeds = open(seeds_path, encoding="utf-8").read().split('\n')
    
    # 种子信息列表, 存储了种子对象
    seeds_information = []

    # 目前为止最大的覆盖路径
    init_cover_path = ""

    # 目前为止报过的错误
    init_error_list = []

    # 输出器
    outputter = Outputter()

    # 调度器
    scheduler = Scheduler()
    
    # 计算初始种子的覆盖路径
    for seed in seeds:
        output, err = run_java_command(class_name, seed)
        cover_path = get_cover_path(output)
        percent = get_percent(cover_path)
        init_cover_path, cover_path_flag = update_cover_path(init_cover_path, cover_path)
        init_error_list, error_flag = update_error_list(init_error_list, err)
        
        if cover_path_flag or error_flag:
            new_seed = Seed(seed, percent, cover_path, err)
            seeds_information.append(new_seed)

            print(init_cover_path, cover_path)
            print(init_error_list)
            print_seeds_information(seeds_information)
        

            if cover_path_flag:
                outputter.output_cover(new_seed)
            
            if error_flag:
                outputter.output_error(new_seed)
            
            outputter.output_seed(new_seed)

        outputter.output(init_cover_path, init_error_list, seeds_information)

    
    # 开始进行模糊测试
    while True:
        # 种子调度
        input_seed_1, input_seed_2 = scheduler.schedule(seeds_information)

        # 获得输入和能量
        input_str_1, input_str_2, power = \
            input_seed_1.get_name(), input_seed_2.get_name(), input_seed_1.get_power()

        # 变异，得到新的输入，输入长度为mut_len
        input_list = generate(input_str_1, input_str_2, power)
        
        for i in range(power):
            output, err = run_java_command(class_name, input_list[i])
            cover_path = get_cover_path(output)
            percent = get_percent(cover_path)
            init_cover_path, cover_path_flag = update_cover_path(init_cover_path, cover_path)
            init_error_list, error_flag = update_error_list(init_error_list, err)

            # 如果有新的报错或者新的路径覆盖，则加入到种子信息列表中
            if cover_path_flag or error_flag:
                new_seed = Seed(input_list[i], percent, cover_path, err)
                seeds_information.append(new_seed)

                print(init_cover_path, cover_path)
                print(init_error_list)
                print_seeds_information(seeds_information)
            

                if cover_path_flag:
                    outputter.output_cover(new_seed)
                
                if error_flag:
                    outputter.output_error(new_seed)

                outputter.output_seed(new_seed)
                # 产生了一次有效的变异
                input_seed_1.add_one_valid_mutation_cnt()


            # 输出结果(把下面这个函数注释掉就可以看到想看的信息了)
            outputter.output(init_cover_path, init_error_list, seeds_information)
