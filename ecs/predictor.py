#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-10 22:43:06
# @Author  : mianhk (yugc666@163.com)
# @Link    : ${link}
# @Version : $Id$
import case_info
import param_info
import prediction_vm
import placement_vm


def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result

    case = case_info.Case(ecs_lines, input_lines)  # 获取case中的数据
    # 调用预测函数，返回预测后的字典：结构为{'flavor3': 0, 'flavor2': 2...}每一个虚拟机及其对应的个数
    predict_flavor_dict = prediction_vm.predict_all(case)
    # 调用放置虚拟机函数，将预测的虚拟机放在物理机上
    result = placement_vm.calcu_vm(predict_flavor_dict, case, result)

    return result
