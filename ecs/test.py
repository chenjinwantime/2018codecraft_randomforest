# for i in range(1, 3):  # for(i=0;i<5;i++)
#     print i
# case_path = r'F:/devcloud/others/HuaweiMatch-master/HuaweiMatch-master/Dataset';
# result = []
# result += '1'
# result += '2'
# print result
dict={'a':1,'b':2,'c':3}
# print dict.items()
# sorted(dict, lambda x, y: cmp(x[1], y[1]))
dict=sorted(dict.items(),key = lambda x:x[1],reverse=True)
# sorted(dict.keys())
# print sorted(dict.items(), key=lambda d: d[0])
print dict