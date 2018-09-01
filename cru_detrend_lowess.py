#coding=utf-8

import pandas as pd
import statsmodels.api as sm
#import pylab
import glob

def Lowess_detrend(x,y):
#    z = sm.nonparametric.lowess(y, x)
#    z1 = sm.nonparametric.lowess(y, x, frac=0.1)
#    z45 = sm.nonparametric.lowess(y, x, frac=0.45)
    z9 = sm.nonparametric.lowess(y, x, frac=0.9)
#    pylab.plot(x, y, 'o')
#    pylab.plot(z[:,0], z[:,1], 'r-')
#    pylab.plot(z1[:,0], z1[:,1], 'g-')
#    pylab.plot(z45[:,0], z45[:,1], 'b-')
#    pylab.plot(z9[:,0], z9[:,1], 'y-')
#    pylab.show()
    return z9[:,1]
    
if __name__ == '__main__':
    base_dir = r'F:\crop-climate\crucsv\*.csv'
    filelist = glob.glob(base_dir)
    zero_list=[0]*116
    for filename in filelist:
        df = pd.read_csv(filename)  #用pandas读入数据
        grid_id=filename[-10:-4]
        year_list =  df['Year']    #获取年份列("Year")的数据
#        dataframe1=pd.DataFrame({'Year':year_list})
        dataframe2=pd.DataFrame({'Year':year_list})
        factor=['Cld','Pre','Tmn','Tmp','Tmx']
        for f in factor:
            cru_list = df[f]  
            if len(set(cru_list))==1:
                break
            ys=Lowess_detrend(year_list, cru_list)
            if list(ys)==zero_list:
                break
#            dataframe1[f]=cru_list-ys
            dataframe2[f]=cru_list/ys
        if len(set(cru_list))==1 or list(ys)==zero_list:
            continue
#        dataframe1.to_csv(r'F:\crop-climate\cru_detrend\lowess-additive/%s.csv' % (grid_id),index=False)
        dataframe2.to_csv(r'F:\crop-climate\cru_detrend\lowess-multiplicative/%s.csv' % (grid_id),index=False)