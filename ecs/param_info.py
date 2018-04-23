#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-10 22:43:06
# @Author  : mianhk (yugc666@163.com)
# @Link    : ${link}
# @Version : $Id$

import os

# 所有虚拟机的参数
# [CPU,MEM, W(M/C) ] [U数，M数，存储比核的权重]
VM_PARAM = {
    'flavor1': [1, 1, 1.0],
    'flavor2': [1, 2, 2.0],
    'flavor3': [1, 4, 4.0],

    'flavor4': [2, 2, 1.0],
    'flavor5': [2, 4, 2.0],
    'flavor6': [2, 8, 4.0],

    'flavor7': [4, 4, 1.0],
    'flavor8': [4, 8, 2.0],
    'flavor9': [4, 16, 4.0],

    'flavor10': [8, 8, 1.0],
    'flavor11': [8, 16, 2.0],
    'flavor12': [8, 32, 4.0],

    'flavor13': [16, 16, 1.0],
    'flavor14': [16, 32, 2.0],
    'flavor15': [16, 64, 4.0]
}


