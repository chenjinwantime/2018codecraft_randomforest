#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-12 10:30:54
# @Author  : mianhk (yugc666@163.com)
# @Link    : ${link}
# @Version : $Id$


'''
    工具类
'''
import param_info
import math

OPT_OBJECT = {
    'CPU': 0,
    'MEM': 1
}
# 预测时间粒度
# 训练数据粒度
TIME_GRAIN_HOUR = 0
TIME_GRAIN_DAY = 1
# TIME_GRAIN_MORE_DAY = 2
# TIME_GRAIN_SEVEN_DAY=7

# 训练时间粒度
TRAIN_GRAIN_DAYS=7

# 检查dict中是否存在key
def isContainKey(dic, key):
    return key in dic.keys()


def calcu_days(begin_day,end_day):
    predict_time_grain=0
    st_year, st_month, st_day = begin_day.split(' ')[0].split('-')
    et_year, et_month, et_day = end_day.split(' ')[0].split('-')
    day_index = (int(et_year) - int(st_year)) * 365 + \
                                 (int(et_month) - int(st_month)) * 30 + (int(et_day) - int(st_day))
    return day_index
    # pass
def get_mean(data):
    return float(sum(data))/len(data)
    
    
def get_mean_1(data):
    n=len(data)
    sum=0
    for i in range(0,n):
        sum=sum+data[i]
    #print sum
    if n==0:
        return sum
    sum=float(sum/n)
    return sum

def get_sum(data):
    n=len(data)
    sum=0
    for i in range(0,n):
        sum=sum+data[i]
    return sum
    
    
def get_median(data):
    data = sorted(data)
    size = len(data)
    if size % 2 == 0:
        median = (data[size/2]+data[size/2-1])/2
        data[0] = median
    if size % 2 == 1: 
        median = data[(size-1)/2]
        data[0] = median
    return data[0]

    
def get_variance(data):
        ex=float(sum(data))/len(data);  
        s=0;  
        for i in data:  
            s+=(i-ex)**2;  
        return float(s)/len(data); 

'''
def mean_2(list_mean)
    n,m=list_mean.shape
    sum=0
    for i in range(n)
        for j in range(m)
            sum+=list[n][m]
    sum=sum/n/m
    return sum 
'''    
    