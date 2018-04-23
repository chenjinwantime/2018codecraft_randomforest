#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-12 10:30:54
# @Author  : mianhk (yugc666@163.com)
# @Link    : ${link}
# @Version : $Id$


'''
    装配模型，输入为预测模型输出的预测对象，
    输出装好的结果
'''
import param_info
import math
import Tools
import case_info


def calcu_vm(predict_flavor_dict, case, result):
    sum_of_predict_flavor = 0
    result_tmp = ''
    for i in predict_flavor_dict:
        # print 'predict_flavor_dict[i]:  '+str(predict_flavor_dict[i])
        sum_of_predict_flavor += predict_flavor_dict[i]
        result_tmp += str(i) + ' ' + str(predict_flavor_dict[i]) + '\r\n'
    # print 'sum_of_predict_flavor:'+str(sum_of_predict_flavor)
    result.append(int(sum_of_predict_flavor))
    result.append(result_tmp)
    # 计算物理服务器的个数和分布
    result = calcu_phy_mac(predict_flavor_dict, case, result)
    return result



def calcu_phy_mac(predict_flavor_dict, case, result):
    # 判断需要优化的目标
    if ('CPU' == case.opt_target):
        VM_PARAM = sorted(case.vm_types.items(), key=lambda x: x[1], reverse=True)
    else:
        VM_PARAM = sorted(case.vm_types.items(), key=lambda x: x[1], reverse=True)
    phy_host= {1: [case.CPU, case.MEM]}
    total_host=1
    flavor_placement = {}
    temp_result = {1:''}
    for item in VM_PARAM:  # VM_PARAM是一个元组
        if (Tools.isContainKey(predict_flavor_dict, item[0])):  #判断是否在需要预测的虚拟机中
            flavor_placement[item[0]]={}
            # if(0==predict_flavor_dict[item[0]]):
            #     flavor_placement[item[0]][i] = 0
            for x in range(1, predict_flavor_dict[item[0]] + 1):
                host_num=len(phy_host)
                flag=0    #够不够放的标识符
                for i in range(1,host_num+1):
                    # print 'host_num: '+str(host_num)+' i: '+str(i)
                    if (phy_host[i][0] >= case.vm_types[item[0]][0] and phy_host[i][1] >= case.vm_types[item[0]][1]):
                        # print 'case.vm_types[item[0]][0]: ' + str(case.vm_types[item[0]][0])
                        # print 'case.vm_types[item[0]][1]: ' + str(case.vm_types[item[0]][1])
                        # print 'phy_host[i][0]: '+str(phy_host[i][0])+' phy_host[i][1]: '+str(phy_host[i][1])
                        flag = 1
                        # temp += 1
                        phy_host[i][0] -= case.vm_types[item[0]][0]
                        phy_host[i][1] -= case.vm_types[item[0]][1]
                        if not Tools.isContainKey(flavor_placement[item[0]], i):
                            flavor_placement[item[0]][i]=1
                        else:
                            flavor_placement[item[0]][i]+=1
                        # print 'flavor_placement[item[0]]: '+str(flavor_placement[item[0]])
                        break
                if 0==flag:
                    total_host += 1
                    temp_result[total_host]=''
                    phy_host[total_host]=[case.CPU, case.MEM]
                    # print 'phy_host[total_host]: '+str(phy_host[total_host])
                    phy_host[total_host][0] -= case.vm_types[item[0]][0]
                    phy_host[total_host][1] -= case.vm_types[item[0]][1]
                    # print 'phy_host[total_host][0]: '+str(phy_host[total_host][0])+'  phy_host[total_host][1]: '+str(phy_host[total_host][1])
                    # flag=1
                    if not Tools.isContainKey(flavor_placement[item[0]], total_host):
                        flavor_placement[item[0]][total_host] = 1
                    else:
                        flavor_placement[item[0]][total_host] += 1

    for i in flavor_placement:    #遍历flavor_placement字典，每个字典存放的为
        for j in flavor_placement[i]:
            # print j
            temp_result[j]=temp_result[j]+str(i)+' '+str(flavor_placement[i][j])+' '
    ##添加放置在物理机上的结果
    result.append(str(total_host)) #物理机的个数
    for i in temp_result:
        result.append(str(i)+' '+temp_result[i])#每一行即为每台物理机放的虚拟机
    # print 'temp_result'
    # print temp_result
    # print 'flavor_placement'
    # print flavor_placement
    return result



