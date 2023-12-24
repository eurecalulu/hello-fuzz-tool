import subprocess
import os
from scheduler import schedule, mutation

java_path = ".//Target1HelloFuzzing.java"
class_name = "Target1HelloFuzzing"


def compile_java_source(java_file):
    # 使用javac命令编译Java源代码
    proc = subprocess.Popen(['javac', java_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()  # 获取编译输出和错误信息

    if proc.returncode == 0:
        print("Java源代码编译成功")
    else:
        print("Java源代码编译失败")
        print("编译输出: ", stdout.decode())
        print("编译错误: ", stderr.decode())


def get_percent(output, perc):
    res = ((str(output)).split("\\n"))[-1]
    if perc == "":
        return output
    else:
        temp = ""
        flag = False
        for i in range(len(output)):
            if perc[i] == '1' or res[i] == '1':
                temp += '1'
            else:
                temp += '0'
            if output[i] == '1' and res[i] == '0':
                flag = True
    return temp, flag



def run_java_command(class_name, seed):
    java_command = ['java', class_name, seed]
    # 启动新进程并重定向输出流和错误流
    process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 读取输出流和错误流
    output, error = process.communicate()
    # print(output)
    # print(error)
    # print(get_percent(output))
    if error != b'':
        print("error !!!!!!!!!!!!!!!!\n\n\n\n\n")
        print(error)
    return output


if __name__ == "__main__":
    # 先在hellofuzzing-instrument目录下运行 mvn clean package
    
    # 程序插装
    os.system(
        "java -jar ..\hellofuzzing-instrument\\target\hellofuzzing-instrument-1.0-SNAPSHOT.jar " + ".\Target1.java ")
    
    # 编译程序
    compile_java_source(java_path)
    
    # 种子队列
    seeds = open("./seeds.txt", encoding="utf-8").read().split('\n')
    
    # 种子覆盖率
    weights = []
    for seed in seeds:
        weights.append(get_percent(run_java_command(class_name, seed), ""))

    # 开始循环
    init_perc = ""

    print("初始种子", seeds, weights)

    # 变异长度
    mut_len = 1
    while True:
        # 种子调度
        input_str_1, input_str_2 = schedule(seeds, weights)

        # 变异
        input_list = mutation(input_str_1, input_str_2, mut_len)
        for i in range(mut_len):
            # 计算覆盖率
            perc, flag = get_percent(run_java_command(class_name, input_list[i]), init_perc)

            # 更新最优覆盖率
            if flag:  # 更新队列
                init_perc = perc
                seeds.append(input_list[i])
                weights.append(perc)

                print(seeds, weights)