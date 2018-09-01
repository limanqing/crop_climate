#coding=utf-8

import pandas as pd
#import statsmodels.api as sm
#import os
import glob

    
if __name__ == '__main__':
    base_dir1 = r'F:\crop-climate\maize_detrend\lowess-multiplicative\*.csv'
    filelist1 = glob.glob(base_dir1)
    base_dir2 = r'F:\crop-climate\cru_detrend\lowess-multiplicative\*.csv'
    filelist2 = glob.glob(base_dir2)
    for filename1 in filelist1:
        grid_id1=filename1[-10:-4]
        for filename2 in filelist2:
            grid_id2=filename2[-10:-4]
            if grid_id1==grid_id2:
                df1=pd.read_csv(filename1)
                df2=pd.read_csv(filename2)
                dataframe=pd.merge(df1,df2)
                dataframe.to_csv(r'F:\crop-climate\maize&cru\lowess-multiplicative/%s.csv' % (grid_id1),index=False)
                break

#    csvfile1 = r'F:\crop-climate\maize_073507.csv'
#    df1 = pd.read_csv(csvfile1)  #用pandas读入数据
#    csvfile2 = r'F:\crop-climate\cru_073507.csv'
#    df2 = pd.read_csv(csvfile2)  #用pandas读入数据
#    dataframe=pd.merge(df1,df2)
#    dataframe.to_csv(r'F:\crop-climate\merge_073507.csv',index=False)