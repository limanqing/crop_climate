#coding=utf-8

import pandas as pd
import glob
import numpy as np

def accumulate():
    global num
    num+=1
    df1 = pd.read_csv(filename)  
    coef1=df2.iat[num-1,2]
    coef2=df2.iat[num-1,3]
    pre=coef1*df1['Pre']
    tmp=coef2*df1['Tmp']
    pre_list.append(np.std(pre))
    tmp_list.append(np.std(tmp))
    maize_list.append(np.std(df1['Value']))
            
if __name__ == '__main__':
    base_dir = r'F:\crop-climate\maize&cru\linear-additive\*.csv'
    filelist = glob.glob(base_dir)
    pre_list=[]
    tmp_list=[]
    maize_list=[]
    num=0
    x_ref=59
    df2 = pd.read_csv(r'F:\crop-climate\regression\mlr\linear-additive.csv',index_col=False)#读回归系数
    result_file = r'F:\crop-climate\IAV2.csv'
    fresult = open(result_file, 'w')
    cols_result = ['lat','pre','pre_std','tmp','tmp_std']
    fresult.write(','.join(cols_result) + '\n')#写第一列的标签
    for filename in filelist:
        grid_id=filename[-10:-4]
        x=int(grid_id)//1000
        if x<=x_ref:#添加元素
            accumulate()
        else:#计算平均值，写入文件，并开始新一轮的累加           
            lat=89.75-(x_ref-4.5)/2
            m1=np.mean(pre_list)
            m2=np.mean(tmp_list)
            u1=np.std(pre_list)
            u2=np.std(tmp_list)
            line= '%f,%f,%f,%f,%f,' % (lat,m1,u1,m2,u2)
            fresult.write(line + '\n')

            x_ref+=10
            pre_list=[]
            tmp_list=[]
            accumulate()
            
    lat=89.75-(x_ref-4.5)/2#最后一个维度写入文件
    m1=np.mean(pre_list)
    m2=np.mean(tmp_list)
    u1=np.std(pre_list)
    u2=np.std(tmp_list)
    line= '%f,%f,%f,%f,%f,' % (lat,m1,u1,m2,u2)
    fresult.write(line + '\n')
    fresult.close()
    print(np.mean(maize_list))
          
