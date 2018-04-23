#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-12 10:30:54
# @Author  : mianhk (yugc666@163.com)
# @Link    : ${link}
# @Version : $Id$


'''
    装配模型，输入为预测模型输出的预测对象，
    在转配模型中可维护一个历史物理机集群状态对象，
    可为另一种转配理解。
'''
import param_info
import math
import case_info


def calcu_vm(predict_flavor_dict, case, result):

    sum_of_predict_flavor = 0
    result_tmp = ''
    index_tmp = 0
    for i in predict_flavor_dict:
        # if(CaseProcess.isContainKey(ParamInfo.VM_PARAM, i)):
        sum_of_predict_flavor += predict_flavor_dict[i]
        result_tmp += str(i) + ' ' + str(predict_flavor_dict[i]) + '\r\n'
    # result_tmp += '\n'
    result.append(int(sum_of_predict_flavor))
    result.append(result_tmp)
    print result
    # result = 'hildsjldajslkdjlkj'
    # 计算物理服务器的个数和分布
    result = calcu_phy_mac(predict_flavor_dict, 'CPU', case, result)
    return result


def set_phy_mac(case):
    pass


def calcu_phy_mac(predict_flavor_dict, opt_target, case, result):
    # 计算需要的物理CPU和MEM的总数
    predict_CPU=0
    predict_MEM=0
    for i in predict_flavor_dict:
        for x in range(1, predict_flavor_dict[i] + 1):
            predict_CPU+=param_info.VM_PARAM[i][0]
            predict_MEM+=param_info.VM_PARAM[i][1]
    print 'predict_CPU:  '+str(predict_CPU)
    print 'predict_MEM:  ' + str(predict_MEM)
    total_phy_mac = int(math.ceil(max((predict_CPU + 0.0) / case.CPU, (predict_MEM + 0.0) / case.MEM)))  #上取整计算物理机数量
    print 'total_phy_mac:  '+str(total_phy_mac)
    index_phy_mac = 1
    tmp_result = ''
    tmp_result = str(1) + ' '
    # tmp_result.append(' ')
    total_cpu = total_phy_mac * case.CPU
    # total_cpu = 3
    total_mem = total_phy_mac * case.MEM
    # print 'total_cpu: ' + str(total_cpu) + '  total_mem: ' + str(total_mem)
    print 'predict_flavor_dict: '+str(predict_flavor_dict)
    ##放置虚拟机策略：先计算虚拟机的资源，先将虚拟机的型号根据优化条件排序，之后遍历，从大到小开始一个个放，尽量放满
    #排序
    # print ParamInfo.VM_PARAM.items()
    if('CPU'==case.opt_target):
        param_info.VM_PARAM=sorted(param_info.VM_PARAM.items(), key = lambda x:x[1], reverse=True)
    else:
        param_info.VM_PARAM =sorted(param_info.VM_PARAM.items(), key = lambda x:x[1], reverse=True)
    print param_info.VM_PARAM
    for i in predict_flavor_dict:
        tmp_total = 0
        # print ParamInfo.VM_PARAM[i][0]  # 虚拟机的CPU
        for x in range(1, predict_flavor_dict[i] + 1):
            # print 'x: ' + str(x)
            # print 'total_cpu: ' + str(total_cpu) + '  total_mem: ' + str(total_mem)
            # print 'ParamInfo.VM_PARAM[i][0]: ' + str(ParamInfo.VM_PARAM[i][0])
            # print 'ParamInfo.VM_PARAM[i][1]: ' + str(ParamInfo.VM_PARAM[i][1])
            if(total_cpu >= param_info.VM_PARAM[i][0] and total_mem >= param_info.VM_PARAM[i][1]):
                # print '***************************'
                tmp_total += 1
                total_cpu -= param_info.VM_PARAM[i][0]
                total_mem -= param_info.VM_PARAM[i][1]

            else:
                tmp_result += i + ' ' + str(tmp_total) + '\r\n'
                tmp_total = 0
                total_cpu += case.CPU
                total_mem += case.MEM
                total_phy_mac += 1
                index_phy_mac += 1
                tmp_result += str(index_phy_mac) + ' '
                tmp_total += 1
                total_cpu -= param_info.VM_PARAM[i][0]
                total_mem -= param_info.VM_PARAM[i][1]
            # print 'tmp_total: ' + str(tmp_total)
        tmp_result += i + ' ' + str(tmp_total) + ' '
    # print tmp_result
    # print total_phy_mac
    result.append(int(total_phy_mac))
    result.append(tmp_result)

    return result
    # if(opt_target == 'CPU')
    #     for i in predict_flavor_dict:


def calcu_phy_mac1(predict_flavor_dict, case, result):
    # 计算需要的物理CPU和MEM的总数
    predict_CPU=0
    predict_MEM=0
    for item in predict_flavor_dict:
        for x in range(1, predict_flavor_dict[item] + 1):
            predict_CPU+=param_info.VM_PARAM[item][0]
            predict_MEM+=param_info.VM_PARAM[item][1]
    print 'predict_CPU:  '+str(predict_CPU)
    print 'predict_MEM:  ' + str(predict_MEM)
    total_phy_mac = int(math.ceil(max((predict_CPU + 0.0) / case.CPU, (predict_MEM + 0.0) / case.MEM)))  #上取整计算物理机数量
    print 'total_phy_mac:  '+str(total_phy_mac)
    #生成total_phy_mac个数的物理机
    phy_host={}
    total_palcement = [100,'']
    for i in range(1,total_phy_mac+1):
        phy_host[i]=[case.CPU,case.MEM]
        # total_palcement[i]=''
    print 'phy_host:'
    print phy_host
    index_phy_mac = 1
    tmp_result = ''
    tmp_result = str(1) + ' '
    # tmp_result.append(' ')
    total_cpu = total_phy_mac * case.CPU
    # total_cpu = 3
    total_mem = total_phy_mac * case.MEM
    print 'total_cpu: ' + str(total_cpu) + '  total_mem: ' + str(total_mem)
    print 'predict_flavor_dict: '+str(predict_flavor_dict)
    ##放置虚拟机策略：先计算虚拟机的资源，先将虚拟机的型号根据优化条件排序，之后遍历，从大到小开始一个个放，尽量放满
    #排序
    if('CPU'==case.opt_target):
        VM_PARAM=sorted(case.vm_types.items(),key = lambda x:x[1],reverse=True)
    else:
        VM_PARAM =sorted(case.vm_types.items(), key = lambda x:x[1],reverse=True)
    print VM_PARAM
    print predict_flavor_dict
    #temp_placement 放置的字典
    temp_placement={}

    for item in VM_PARAM:  #VM_PARAM是一个元组
        tmp_total = {}

        if(Tool.isContainKey(predict_flavor_dict,item[0])):
            tmp_total[item[0]]=[0,0]
            print 'item[0]:'
            print item[0]
            # print case.vm_types[i][0]  # 虚拟机的CPU
            # if(0==predict_flavor_dict[item[0]]):
            #     break
            for x in range(1, predict_flavor_dict[item[0]] + 1):
                # print 'x: ' + str(x)
                # print 'total_cpu: ' + str(total_cpu) + '  total_mem: ' + str(total_mem)
                #循环放置
                flag=0 #够放的标识符
                for i in phy_host:
                    temp=0
                    print 'i: '+str(i)
                    print 'phy_host[i][0]'
                    print phy_host[i][0]
                    if (phy_host[i][0] >= case.vm_types[item[0]][0] and phy_host[i][1] >= case.vm_types[item[0]][1]):
                        print 'case.vm_types[item[0]][0]: ' + str(case.vm_types[item[0]][0])
                        print 'case.vm_types[item[0]][1]: ' + str(case.vm_types[item[0]][1])
                        flag=1
                        temp+=1
                        phy_host[i][0]-=case.vm_types[item[0]][0]
                        phy_host[i][1]-=case.vm_types[item[0]][1]
                        tmp_total[item[0]]=[i,tmp_total[item[0]][1]+1]
                        # temp_placement[i]=tmp_total
                        # if not Tool.isContainKey(temp_placement,case.vm_types[item[0]]):
                        #     temp_placement[i]=[item[0],1]
                        # else:
                        #     temp_placement[i] = [item[0], temp_placement[i][2]+1]
                    total_palcement[i]=tmp_total[item[0]]
                    break
                if(0==flag):
                    phy_host[total_phy_mac+1]=[case.CPU,case.MEM]
                    flag = 1
                    phy_host[total_phy_mac+1][0] -= case.vm_types[item[0]][0]
                    phy_host[total_phy_mac+1][1] -= case.vm_types[item[0]][1]
                    # if not Tool.isContainKey(temp_placement, case.vm_types[item[0]]):
                    #     temp_placement[i] = [item[0], 1]
                    # else:
                    #     temp_placement[i] = [item[0], temp_placement[i][2] + 1]
                    tmp_total[item[0]] = [i, tmp_total[item[0]][1] + 1]
                    temp_placement[i]=tmp_total[item[0]]
                    total_phy_mac += 1

        # temp_placement[item[0]]=str(tmp_total)
    print 'temp_placement:  '
    print temp_placement





            #     if(total_cpu >= case.vm_types[item[0]][0] and total_mem >= case.vm_types[item[0]][1]):
            #         # print '***************************'
            #         tmp_total += 1
            #         total_cpu -= case.vm_types[item[0]][0]
            #         total_mem -= case.vm_types[item[0]][1]
            #
            #     else:
            #         tmp_result += item[0] + ' ' + str(tmp_total) + '\r\n'
            #         tmp_total = 0
            #         total_cpu += case.CPU
            #         total_mem += case.MEM
            #         total_phy_mac += 1
            #         index_phy_mac += 1
            #         tmp_result += str(index_phy_mac) + ' '
            #         tmp_total += 1
            #         total_cpu -= case.vm_types[item[0]][0]
            #         total_mem -= case.vm_types[item[0]][1]
            #     # print 'tmp_total: ' + str(tmp_total)
            # tmp_result += item[0] + ' ' + str(tmp_total) + ' '
    # print tmp_result
    # print total_phy_mac
    result.append(int(total_phy_mac))
    result.append(tmp_result)

    return result
    # if(opt_target == 'CPU')
    #     for i in predict_flavor_dict:
