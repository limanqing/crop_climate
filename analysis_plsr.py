#coding=utf-8

import pandas as pd
import glob

from sklearn.cross_decomposition import PLSRegression

def plsr(y,x,ncomp=2):
    
    pls = PLSRegression(n_components=ncomp)
    pls.fit(x, y)

    n = len(pls.x_std_)
    s=''
    for i in range(n):
        print('coef%d: %f' % (i, pls.coef_[i,0]/pls.x_std_[i]))
        s += '%.3f, ' % (pls.coef_[i,0]/pls.x_std_[i])
    return s



if __name__ == '__main__':
    datadir = r'F:\crop-climate\maize&cru\polyfit-multiplicative\*.csv'
    filelist = glob.glob(datadir)
    result_file = r'F:\crop-climate\regression\plsr\polyfit-multiplicative.csv'
    fresult = open(result_file, 'w')
    cols_result = ['grid','cld_coef','pre_coef','tmn_coef','tmp_coef','tmx_coef']
    fresult.write(','.join(cols_result) + '\n')#写第一列的标签

    for filename in filelist:
        grid_id=filename[-10:-4]
        line = str(grid_id) + ','
        print(grid_id)
        df = pd.read_csv(filename)
        s=plsr(df['Value'], df[['Cld','Pre','Tmn','Tmp','Tmx']], 3)
        line = line + s 
        fresult.write(line + '\n')
    
    fresult.close()
