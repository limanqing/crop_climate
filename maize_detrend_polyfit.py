#coding=utf-8

import pandas as pd
from scipy import polyfit
#import pylab
#import pylab
import glob

def Polyfit_detrend(x,y):        #主程序，相当于C语言的main函数
    a,b,c = polyfit(x, y, 2)
    y_quad = a*x*x + b*x + c      #利用拟合得到的系数，计算x向量对应的y向量
    # 拟合结果绘图
#    pylab.plot(x, y, 'o')         #绘制散点
#    pylab.plot(x, y_quad, 'r-')   #绘制拟合的曲线
#    pylab.show()
    return y_quad

if __name__ == '__main__':
    base_dir = r'F:\crop-climate\maizecsv\*.csv'
    filelist = glob.glob(base_dir)
    for filename in filelist:
        df = pd.read_csv(filename)  #用pandas读入数据
        grid_id=filename[-10:-4]
        year_list =  df['Year']    #获取年份列("Year")的数据
        yield_list = df['Value']   #获取年份列("Value")的数据  
        ys=Polyfit_detrend(year_list, yield_list)
        dataframe1=pd.DataFrame({'Year':year_list,'Value':yield_list-ys})
        dataframe1.to_csv(r'F:\crop-climate\maize_detrend\polyfit-additive/%s.csv' % (grid_id),index=False)
        dataframe2=pd.DataFrame({'Year':year_list,'Value':yield_list/ys})
        dataframe2.to_csv(r'F:\crop-climate\maize_detrend\polyfit-multiplicative/%s.csv' % (grid_id),index=False)