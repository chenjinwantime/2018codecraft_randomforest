# coding=utf-8
import sys
import os
import predictor
case = 1
base_path = r'F:\devcloud\sdk-python/Data';


def main():
    print 'main function begin.'
    # Read the input files
    ecsDataPath = '../test_file/TrainData.txt'
    inputFilePath = '../test_file/input_15flavors_cpu_7days.txt'
    resultFilePath = '../test_file/output.txt'

    ecs_infor_array = read_lines(ecsDataPath)
    input_file_array = read_lines(inputFilePath)

    # implementation the function predictVm
    predic_result = predictor.predict_vm(ecs_infor_array, input_file_array)  #调用预测函数，返回结果
    print predic_result
    # 写入结果
    if len(predic_result) != 0:
        write_result(predic_result, resultFilePath)
    else:
        predic_result.append("NA")
        write_result(predic_result, resultFilePath)
    print 'main function end.'

def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\r\n" % item)

def write_result1(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\r" % item)
        # for item in array:
        #     output_file.write("%s\n" % item)
            # output_file.write('\r')
            # output_file.write(item)


def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None


if __name__ == "__main__":
    main()
