import subprocess
import os
from scheduler import choose_seeds, schedule

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


def get_percent(output):  # 捕捉输出流的最后11位
    return str(output[-11:]).count("1") / 11


def run_java_command(class_name, seed):
    java_command = ['java', class_name, seed]
    # 启动新进程并重定向输出流和错误流
    process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 读取输出流和错误流
    output, error = process.communicate()
    print(output)
    print(get_percent(output))
    return get_percent(output)


if __name__ == "__main__":
    # 先在hellofuzzing-instrument目录下运行 mvn clean package
    # 插装
    tmp = open("seeds.txt", encoding="utf-8").read().split('\n')
    os.system(
        "java -jar ..\hellofuzzing-instrument\\target\hellofuzzing-instrument-1.0-SNAPSHOT.jar " + ".\Target1.java ")
    compile_java_source(java_path)

    # 开始循环
    init_perc = 0.0
    circle = tmp    # 种子队列

    while True:
        seeds = schedule(circle, 1)
        print(seeds)
        perc = run_java_command(class_name, seeds[0])
        if perc > init_perc:  # 更新队列
            init_perc = perc
            circle.append(seeds[0])
