import os
import sys
sys.path.append("")

def instrument(file_path):
    """
    代码插桩
    :param file_path: 待插桩代码路径
    :return: 插桩后的代码路径
    """
    os.system("java -jar ./hellofuzzing-instrument/target/hellofuzzing-instrument-1.0-SNAPSHOT.jar " + file_path)

    instrument_program_path = file_path.split('.java')[0] + "HelloFuzzing.java"
    class_name = file_path.split('/')[-1].split('.java')[0] + "HelloFuzzing"
    return instrument_program_path, class_name

if __name__ == '__main__':
    instrument("./input/Target1.java")