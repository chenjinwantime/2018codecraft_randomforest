#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-11 10:19:20
# @Author  : mianhk (yugc666@163.com)
# @Link    : ${link}
# @Version : $Id$


'''
预测模型

'''
import math
import param_info
import case_info
import Tools
import randomforest

def predict_all(case):
    '''
    输入为case_info对象，
    返回一个结果对象，结构为{vm_type:[v1,v2,v3....]};
    数组长度为case_info,中date_range_size,代表各个时间粒度内，
    该虚拟机被请求数
    返回值为：predict_flavor_dict  字典：{'flavor3': 0, 'flavor2': 2,}
            {虚拟机型号：个数}
    '''
    # print 'case.his_data'
    # print case.his_data
    predict_flavor_dict={}  #新建预测字典
    #对于每一个his_data训练数据中的虚拟机遍历
    for i in case.his_data:
        #如果该虚拟机在预测的虚拟机列表中，则开始进行预测
        if (i in case.vm_types):
            #predict_flavor_dict=predict_one(case,i,predict_flavor_dict)  #调用predict_one预测每一台虚拟机
            predict_flavor_dict[i]=int(randomforest.RandomForestRegression(case,i))
    print 'predict_flavor_dict: '
    print predict_flavor_dict
    return predict_flavor_dict

#指数平滑法预测
def predict_one(case,i,predict_flavor_dict):
    '''
    描述：预测单个虚拟机
    :param case:  输入的case
    :param i: 第几个虚拟机
    :param predict_flavor_dict: 输出字典
    :return: predict_flavor_dict
    '''
    train_data_range_days=case.train_data_range_days/Tools.TRAIN_GRAIN_DAYS #训练时间的周期=总的训练天数/训练的时间粒度
    predict_data_range_days=case.predict_data_range_days/Tools.TRAIN_GRAIN_DAYS#预测时间的周期=总的预测天数/训练的时间粒度
    # print 'train_data_range_days:   '
    # print train_data_range_days
    # print predict_data_range_days
    whole_days=train_data_range_days+predict_data_range_days #总的周期
    # predict_flavor_dict=[]
    his_array=[0 for x in range(whole_days)] #历史数组初始化

    for p in case.his_data[i]:
        his_array[p/Tools.TRAIN_GRAIN_DAYS]+=case.his_data[i][p]
    #调用指数平滑预测
    # predict_flavor_dict[i]=int(predict_array1[train_data_range_days])

        predict_flavor_dict[i]=int(e_prediction(his_array,train_data_range_days,predict_data_range_days, 3))
    # print 'predict_flavor_dict[i]:  '
    # print predict_flavor_dict[i]

    #直接截取预测
    # predict_flavor_dict[i]=0
    # for x in range(predict_data_range_days):
    #     predict_flavor_dict[i]+=int(predict_array[x])
    ##瞎预测一个
    # if(train_data_range_days>2):
    #     predict_flavor_dict[i]=int(predict_array1[train_data_range_days/2])
    # else:
    #     predict_flavor_dict[i] = int(predict_array1[0])
    # print 'predict_flavor_dict[i]: '+str(predict_flavor_dict)
    # predict[0]=a*his_array[case.train_data_range_days-1]+(1-a)*s[case.train_data_range_days-1]
    # for i in range(1,case.predict_data_range_days):

    return predict_flavor_dict


def e_prediction(his_array,train_data_range_days,predict_data_range_days,times):
    # a1 = 0.974 # 加权系数a  0.026最高分的一个了。。
    a1 = 0.974 # 加权系数a  0.026最高分的一个了。。
    predict_array1=his_array
    # y=predict_array1
    y2=predict_array1
    y3=predict_array1
    # print 'len(his_array):'
    # print len(predict_array1)
    #一次平滑
    # for x in range(times):
    # 一阶
    # 确定第一个
    if (len(predict_array1) >= 3):
        predict_array1[0]=(his_array[0]+his_array[1]+his_array[2]+0.0)/3
    else:
        predict_array1[0] = his_array[0]
    # print 'predict_array1[0] '
    # print predict_array1[0]
    # predict_array3=predict_array2
    #一阶循环
    for j in range(1, len(predict_array1)):
        predict_array1[j] = (a1) * his_array[j] + (1-a1) * predict_array1[j - 1]
    # 二阶
    predict_array2 = predict_array1
    #二阶第一个
    if (len(predict_array1) >= 3):
        predict_array2[0] = (predict_array1[0] + predict_array1[1] + predict_array1[2] + 0.0) / 3
    else:
        predict_array2[0] = predict_array1[0]
    # predict_array2[0]=
    #二阶循环
    for j in range(1, len(predict_array1)):
        predict_array2[j] = (a1) * predict_array1[j] + (1-a1) * predict_array2[j - 1]
        # print predict_array1[j]
        # predict_array3[j]=(1-a)* predict_array2[j] + (a) * predict_array3[j - 1]
        # print predict_array1[j]
        at2=2*(predict_array1[j])-predict_array2[j]
        bt2=a1/(1-a1)*(predict_array1[j]-predict_array2[j])
        y2[j] = at2 + bt2 * j
        # at3=3*(predict_array1[j])-3*(predict_array2[j])+predict_array3[j]
        # bt3=a/pow((1-a),2)/2*((6-5*a)*predict_array1[j]-2*(5-4*a)*predict_array2[j]+(4-3*a)*predict_array3[j])
        # ct3=pow((a),2)/pow((1-a),2)/2*(predict_array1[j]-2*predict_array2[j]+predict_array3[j])
        # y3[j]=at3+bt3*j+ct3*pow(j,2)
        # if (j > len(his_array)):
        #     predict_array1[j] = int(predict_array1[j])
        #     # print '***********'

    # print predict_array1
    # a=2*(predict_array1[-predict_data_range_days])-predict_array1[-predict_data_range_days]
    # print y
    res=0
    for x in range(predict_data_range_days):
            res+=y2[-x-1]
    return res
    # return y3[-1]
    # return  predict_array1





