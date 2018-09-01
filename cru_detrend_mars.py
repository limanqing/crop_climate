#coding=utf-8

import pandas as pd
from pyearth import Earth
#from matplotlib import pyplot
import glob

def Mars_detrend(x,y):
    model = Earth()
    model.fit(x,y)
    
#    print(model.trace())
#    print(model.summary())

    y_hat = model.predict(x)
#    pyplot.figure()
#    pyplot.plot(x,y,'r.')
#    pyplot.plot(x,y_hat,'b.')
#    pyplot.xlabel('x_6')
#    pyplot.ylabel('y')
#    pyplot.title('Maize yield in a grid')
#    pyplot.show()
    return y_hat

if __name__ == '__main__':
    base_dir = r'F:\crop-climate\crucsv\*.csv'
    filelist = glob.glob(base_dir)
    for filename in filelist:
        df = pd.read_csv(filename)  #用pandas读入数据
        grid_id=filename[-10:-4]
        year_list =  df['Year']    #获取年份列("Year")的数据
        dataframe1=pd.DataFrame({'Year':year_list})
        dataframe2=pd.DataFrame({'Year':year_list})
        factor=['Cld','Pre','Tmn','Tmp','Tmx']
        for f in factor:
            cru_list = df[f]   
            if len(set(cru_list))==1:
                break
            ys=Mars_detrend(year_list, cru_list)
            dataframe1[f]=cru_list-ys
            dataframe2[f]=cru_list/ys
        if len(set(cru_list))==1:
            continue
        dataframe1.to_csv(r'F:\crop-climate\cru_detrend\mars-additive/%s.csv' % (grid_id),index=False)
        dataframe2.to_csv(r'F:\crop-climate\cru_detrend\mars-multiplicative/%s.csv' % (grid_id),index=False)