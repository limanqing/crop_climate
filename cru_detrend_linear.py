#coding=utf-8

import pandas as pd
import statsmodels.api as sm
#import pylab
import glob

def linear_detrend(x, y):
    """用statsmodels实现线性拟合"""
    X = sm.add_constant(x)   #给矩阵左侧加上一列1
    mod = sm.OLS(y, X)    #确定为普通最小二乘模型
    res = mod.fit()          #res是存放拟合结果的对象

#    print( res.summary() )   #用res的summary()函数可以给出拟合结果的描述
    return res

def linear_result(x, y, x_name, res):
    """回执线性拟合结果"""
    X = sm.add_constant(x)
    ys = res.predict(X)      #用拟合结果推测x向量所对应的拟合值

#    pylab.clf()          #清除当前图像窗口    
#    pylab.plot(x, y, 'o')    #用matplotlib画用于拟合的点数据，o是圆形的点
#    pylab.plot(x, ys, 'r-')  #画拟合线，第三个参数指定绘图符号,r是红色，-是实线
#    
#    slp, p, r2 = res.params[x_name], res.pvalues[x_name], res.rsquared
#    pylab.title('slp:%.3f p:%.3f r2:%.3f' % (slp, p, r2))   #把拟合的主要结果放到图标题上,r2是决定系数
#    pylab.show()
    return ys

if __name__ == '__main__':
    base_dir = r'F:\crop-climate\crucsv\*.csv'
    filelist = glob.glob(base_dir)
    for filename in filelist:
        df = pd.read_csv(filename)  #用pandas读入数据
        grid_id=filename[-10:-4]
        x_name = 'Year'
        year_list =  df[x_name]    #获取年份列("Year")的数据
        dataframe1=pd.DataFrame({'Year':year_list})
        dataframe2=pd.DataFrame({'Year':year_list})
        factor=['Cld','Pre','Tmn','Tmp','Tmx']
        for f in factor:
            cru_list = df[f]  
            if len(set(cru_list))==1:
                break
            fit_result = linear_detrend(year_list, cru_list)
            ys=linear_result(year_list, cru_list, x_name, fit_result)
            dataframe1[f]=cru_list-ys
            dataframe2[f]=cru_list/ys
        if len(set(cru_list))==1:
            continue
        dataframe1.to_csv(r'F:\crop-climate\cru_detrend\linear-additive/%s.csv' % (grid_id),index=False)
        dataframe2.to_csv(r'F:\crop-climate\cru_detrend\linear-multiplicative/%s.csv' % (grid_id),index=False)
        
    

