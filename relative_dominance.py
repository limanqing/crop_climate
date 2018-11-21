#coding=utf-8

import pandas as pd
import glob
import numpy as np


if __name__ == '__main__':
    base_dir = r'F:\crop-climate\maize&cru_scale\360\polyfit-additive\*.csv'
    filelist = glob.glob(base_dir)
    sum1=0
    sum2=0
    sum3=0
    num=0
    pre_list=[]
    tmp_list=[]
    maize_list=[]
    df2 = pd.read_csv(r'F:\crop-climate\regression_scale\polyfit-additive\360.csv',index_col=False)#读回归系数
    for filename in filelist:
        num+=1
        df1 = pd.read_csv(filename)  
        coef1=df2.iat[num-1,2]
        coef2=df2.iat[num-1,3]
        pre=coef1*df1['Pre']
        tmp=coef2*df1['Tmp']
        pre_list.append(np.var(pre))
        tmp_list.append(np.var(tmp))
        maize_list.append(np.var(df1['Value']))
    d1=np.mean(pre_list)/np.mean(maize_list)
    d2=np.mean(tmp_list)/np.mean(maize_list)
    d3=np.std(pre_list)/np.mean(maize_list)
    d4=np.std(tmp_list)/np.mean(maize_list)
    print(d1,d3,d2,d4)
