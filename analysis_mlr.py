#coding=utf-8

import pandas as pd
import statsmodels.api as sm
import glob

def mlr(y, x):
    X = sm.add_constant(x)
    mod = sm.OLS(y, X)
    res = mod.fit()
    print(res.params)
    s=''
    for col in range(4):
        s += '%.3f,' % (res.params[col])
    return s


if __name__ == '__main__':
    datadir = r'F:\crop-climate\maize&cru\linear-additive\*.csv'
    filelist = glob.glob(datadir)
    result_file = r'F:\crop-climate\regression\mlr\linear-additive.csv'
    fresult = open(result_file, 'w')
    cols_result = ['grid','const','cld_coef','pre_coef','tmp_coef']
    fresult.write(','.join(cols_result) + '\n')#写第一列的标签

    for filename in filelist:
        grid_id=filename[-10:-4]
        line = str(grid_id) + ','
        df = pd.read_csv(filename)
        s = mlr(df['Value'], df[['Cld','Pre','Tmp']])
        line = line + s 
        fresult.write(line + '\n')
    
    fresult.close()
