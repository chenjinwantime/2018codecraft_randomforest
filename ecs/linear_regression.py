import case_info

def linear_regression_vm(case,type,alpha,epsilon):
    print 'linear_regression_vm'
    X=[]
    Y=[]
    X_data=[]
    Y_data=[]
    error1=0
    error0=0
    cnt=0
    diff=0
    diff1=0
    #print case.train_data_days
    for x in case.train_data_days:
        if type in case.his_data_day[x]:
            print case.his_data_day[x][type]
            X.append(case.his_data_day[x][type])
        else: 
            X.append(0)
    #print 'X'
    #print X    
        
    for i in range(0,len(X)-7):
        x_data=[]
        for j in range(i,i+7):
            x_data.append(X[j])
        X_data.append(x_data)
    #print 'X_data'
    #print X_data
    for i in range(7,len(X)):
        Y_data.append(X[i])
    #print 'Y_data'
    #print Y_data
    weight={}
    weight_orgin=[0 for i in range(0,case.predict_data_range_days)]
    weight[type]=weight_orgin
    #print weight_orgin
    while True:
        cnt+=1
        for i in range(0,len(X_data)):
            diff1=0
            for j in range(0,case.predict_data_range_days):
                diff1+=weight[type][j]*X_data[i][j]
            diff=Y_data[i]-diff1
            #print 'diff'
            #print diff
            for j in range(0,case.predict_data_range_days):
                weight[type][j]+=alpha*diff*X_data[i][j]
            #print weight
        error1=0
        for i in range(0,len(X_data)):
            error_temp=0
            for j in range(0,case.predict_data_range_days):
                error_temp += weight[type][j]*X_data[i][j] 
            error1+=(Y_data[i]-error_temp)**2/2
        #print 'error1'
        #print error1
        #print 'error0'
        #print error0
        #print error1-error0
        if abs(error1-error0) < epsilon:  
            break  
        else:  
            error0 = error1 
        
        
    
    #print 'error1'
    #print error1    
    print type    
    print 'weight' 
    print weight
    print 'cnt' 
    print cnt
    
    return weight[type]
    
    
    
    
def linear_sum(case,weight,type):
    predict_data_type={}
    X=[]
    for x in case.train_data_days[case.train_data_range_days-case.predict_data_range_days-1:case.train_data_range_days-1]:
        print 'linear_sum_x'
        print x
        if type in case.his_data_day[x]:
            print case.his_data_day[x][type]
            X.append(case.his_data_day[x][type])
        else: 
            X.append(0)
    print X
    for day in range(0,case.predict_data_range_days):
        flavor_num=0
        for i in range(0,case.predict_data_range_days):
            flavor_num+=X[i]*weight[type][i]
        flavor_num=int(flavor_num)
        del X[0]
        X.append(flavor_num)
    predict_data_type[type]=X
    return predict_data_type