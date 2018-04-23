#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-10 22:44:22
# @Author  : mianhk (yugc666@163.com)
# @Link    : ${link}
# @Version : $Id$





import collections
import Tools
import math


class Case(object):
    '''
    输入文件的一些信息
    '''
    CPU = 0  # 每台物理机的cpu数
    MEM = 0  # 每台物理机的内存大小 单位G

    opt_target = ''  # 优化目标，值为CPU和MEM

    # vm_type_size = 0  # 需要预测虚拟机类型数量
    vm_types = []  # {虚拟机：[CPU，MEM]} 虚拟机类型,字典：eg:{'flavor3': [1, 4], 'flavor2': [1, 2]}

    time_grain = -1  # 预测时间粒度
    date_range_size = 0  # 需要预测的时间量
    train_data_range = []  # 预测开始时间与结束时间，左闭右开

    train_data_range_days = 0  # 训练数据的天数
    predict_data_range_days = 0  # 预测的天数，简单处理

    # 训练数据中虚拟机、日期二维映射表 [虚拟机类型,日期]
    his_data = {}
    his_data_RF={}
    his_data_features=['d7','d6','d5','d4','d3','d2','d1','mean','max','median','variance','d']
    his_data_features_dict={'d7':0,'d6':1,'d5':2,'d4':3,'d3':4,'d2':5,'d1':6,'mean':7,'max':8,'median':9,'variance':10,'d':11}

    #case的初始化
    def __init__(self, origin_train_data, origin_case_info, predict_time_grain=Tools.TIME_GRAIN_DAY):
        '''
        origin_data  predictor中的input_lines数组
        origin_train_data predictor中的ecs_lines数组
        初始化CaseInfo中的属性
        '''
        self.time_grain = predict_time_grain   #获取时间粒度
        self.set_case_info(origin_case_info, predict_time_grain)  #获取input文件的数据
        self.set_his_data(origin_train_data, predict_time_grain) #获取训练数据
        self.set_his_data_RF(origin_train_data, predict_time_grain)
        
    def set_case_info(self, origin_case_info, predict_time_grain):
        '''
        更改 案例属性信息
        info[0]=CPU MEM HDD
        info[2]=vm_type_size
        info[3:(3+vm_type_size)]=vm_types
        info[4+vm_type_size]=opt_target;
        info[6+vm_type_size]=start_time;
        info[7+vm_type_size]=end_time;
        '''

        # 处理 CPU MEM HDD
        tmp = origin_case_info[0].split(' ')
        self.CPU = int(tmp[0])
        self.MEM = int(tmp[1])

        # 处理虚拟机类型
        tsize = int(origin_case_info[2].replace('\r', ''))
        self.vm_types = {}
        for i in range(tsize):
            _type = origin_case_info[3 + i].replace('\r', '')
            _typename, _cpu, _mem = _type.split(' ')
            self.vm_types[_typename] = [int(_cpu), int(_mem) / 1024]
        # print self.vm_types

        # 处理优化目标
        self.opt_target = origin_case_info[4 + tsize][0:3]

        # 需要预测时间处理
        _st = origin_case_info[6 + tsize]
        _et = origin_case_info[7 + tsize]
        self.predict_data_range_days=Tools.calcu_days(_st,_et)
        # print 'self.data_range_days'  # 打印预测的天数
        # print self.data_range_days

    def set_his_data(self, origin_train_data, predict_time_grain):
        hisdata = {}
        train_begin_time = origin_train_data[0].split('\t')[2]  #训练时间开始
        train_end_time = origin_train_data[-1].split('\t')[2]   #训练时间结束
        # print ' print train_begin_time'
        # print train_begin_time
        # print train_end_time
        self.train_data_range_days=Tools.calcu_days(train_begin_time,train_end_time)+1  #计算训练时间的天数
        print 'train_data_range_days'
        print self.train_data_range_days
        for line in origin_train_data:
            _, vm_type, time = line.split('\t')
            if not Tools.isContainKey(hisdata, vm_type):
                hisdata[vm_type] = collections.OrderedDict()
            ##按天数存储
            # print 'time:   '
            # print time
            day_index = Tools.calcu_days(train_begin_time,get_grain_time(time, predict_time_grain))+1 #加1表示从第一天开始
            #除以训练的时间粒度
            # gt=gt/Tools.TRAIN_GRAIN_DAYS+1  #加1天，表示从1开始
            # print '*******gt:    '
            # print day_index
            point = hisdata[vm_type]
            if not Tools.isContainKey(point, day_index):
                point[day_index] = 0
            cot = point[day_index] + 1
            point[day_index] = cot
        self.his_data = hisdata
        #print 'self.his_data'
        #print self.his_data

        
    def set_his_data_RF(self,origin_train_data, predict_time_grain):
        hisdata = {}
        train_begin_time = origin_train_data[0].split('\t')[2]  #训练时间开始
        train_end_time = origin_train_data[-1].split('\t')[2]   #训练时间结束
        # print ' print train_begin_time'
        # print train_begin_time
        # print train_end_time
        self.train_data_range_days=Tools.calcu_days(train_begin_time,train_end_time)+1  #计算训练时间的天数
        #print 'train_data_range_days'
        #print self.train_data_range_days
        for line in origin_train_data:
            _, vm_type, time = line.split('\t')
            if not Tools.isContainKey(hisdata, vm_type):
                hisdata[vm_type] = collections.OrderedDict()
            ##按天数存储
            # print 'time:   '
            # print time
            day_index = Tools.calcu_days(train_begin_time,get_grain_time(time, predict_time_grain))+1 #加1表示从第一天开始
            #除以训练的时间粒度
            # gt=gt/Tools.TRAIN_GRAIN_DAYS+1  #加1天，表示从1开始
            # print '*******gt:    '
            # print day_index
            point = hisdata[vm_type]
            if not Tools.isContainKey(point, day_index):
                point[day_index] = 0
            cot = point[day_index] + 1
            point[day_index] = cot
        hisdata_RF={}
        hisdata_RF1={}
        for vm_type in hisdata.keys():
            print vm_type
            RF_d=[]
            for day in range(self.train_data_range_days):
                #print hisdata[vm_type].keys()
                if Tools.isContainKey(hisdata[vm_type],day):
                    RF_d.append(float(hisdata[vm_type][day]))
                else:
                    RF_d.append(0.0)
            #print 'RF_d'
            #print RF_d
            RF_d1=[0]
            RF_d1=RF_d1+RF_d[:-1]
            #RF_d1.append(RF_d[:-1])
            #print 'RF_d1'
            #print RF_d1
            RF_d2=[0]    
            RF_d2=RF_d2+RF_d1[:-1]
           
            #print 'RF_d2'
            #print RF_d2
            RF_d3=[0]    
            RF_d3=RF_d3+RF_d2[:-1]
            #print 'RF_d3'
            #print RF_d3
            RF_d4=[0]    
            RF_d4=RF_d4+RF_d3[:-1]
            RF_d5=[0]    
            RF_d5=RF_d5+RF_d4[:-1]
            RF_d6=[0]    
            RF_d6=RF_d6+RF_d5[:-1]
            RF_d7=[0]    
            RF_d7=RF_d7+RF_d6[:-1]
            
            hisdata_RF[vm_type]=[RF_d7,RF_d6,RF_d5,RF_d4,RF_d3,RF_d2,RF_d1]
            RF_mean=[]
            RF_max=[]
            RF_median=[]
            RF_variance=[]
            
            
            
            for row in range(len(hisdata_RF[vm_type][0])):
                row_data=[]
                for list_RF in hisdata_RF[vm_type]:
                    #row_data.append([dt[row] for dt in list_RF])
                    #featList = [dt[i] for dt in dataSet]
                    row_data.append(list_RF[row])
                row_mean=Tools.get_mean(row_data)
                row_max= max(row_data)
                row_median=Tools.get_median(row_data)
                #row_median=Math.median(row_data)
                row_variance=Tools.get_variance(row_data)
                RF_mean.append(row_mean)
                RF_max.append(row_max)
                RF_median.append(row_median)
                RF_variance.append(row_variance)
                #print 'row'
                #print row
                #print 'row_data'
                #print row_data
                #print row_mean
                #print row_max
                #print row_median
                #print row_variance
                
            hisdata_RF1[vm_type]=[RF_d7,RF_d6,RF_d5,RF_d4,RF_d3,RF_d2,RF_d1,\
                                    RF_mean,RF_max,RF_median,RF_variance,RF_d]        
        
        
        
        
        self.his_data_RF=hisdata_RF1
        #print 'his_data_RF'
        #print self.his_data_RF
       


# 获取粒度时间
split_append_tmp = [[13, ':00:00'], [10, ' 00:00:00']];


def get_grain_time(time_str, time_grain):
    sp_len_tmp = split_append_tmp[time_grain][0]
    sp_str_tmp = split_append_tmp[time_grain][1]
    return time_str[:sp_len_tmp] + sp_str_tmp;


