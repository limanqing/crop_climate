#coding=utf-8
import pandas as pd
import statsmodels.api as sm
import pylab
import os
import glob

def linear_detrend(sid, region, inputfile, outputfile, df_all=None, ycol_list=None):
    """用statsmodels实现线性去趋势"""
    df = pd.read_csv(inputfile)  #用pandas读入数据

    xcol  = df.columns[0]      #默认第一列是x变量，剩下的为y变量
    x = df[xcol]
    X = sm.add_constant(x)

    infofile = outputfile[:-4] + '_info.csv'
    f_info = open(infofile, 'w')
    f_info.write('column,slp,p,R2\n')

    if not ycol_list:
        ycol_list = df.columns[1:]

    for ycol in ycol_list:
        y   = df[ycol]
        mod = sm.OLS(y, X)
        res = mod.fit()        #res是存放拟合结果的对象
        s = '%s,%.3f,%.3f,%.3f\n' % (ycol, res.params[xcol], res.pvalues[xcol], res.rsquared)
        f_info.write(s)

        ys  = res.predict(X)
        dy  = y - ys
        df[ycol] = dy
    
    df['sid'] = sid
    df['georegion'] = region

    df_all = pd.concat([df_all, df])

    df.to_csv(outputfile, index=False)
    f_info.close()

    return df_all


if __name__ == '__main__':
    basedir = r'D:\program\soybean\data'
    region_file = basedir + os.sep + 'agri_region.csv'
    df_region = pd.read_csv(region_file)
    # get region info for each site
    region_dic = {}
    for index,row in df_region.iterrows():
        sid = str(row['sid'])
        region = row['georegion']
        region_dic[sid] = region

    met_dir = r'D:\program\soybean\data\met_bygp\*.csv'
    filelist = glob.glob(met_dir)
    
    df_all = None
    for filepath in filelist:
        dirname, filename = os.path.split(filepath)
        sid = os.path.basename(filename).split('_')[-1][:-4]
        detrend_dir = dirname + os.sep + 'detrend_linear'
        if not os.path.exists(detrend_dir):
            os.mkdir(detrend_dir)
        outputfile = detrend_dir + os.sep + filename
        print(filepath, outputfile)
        df_all = linear_detrend(sid, region_dic[sid], filepath, outputfile, df_all)
 
    result_all_file = basedir + os.sep + 'pheno_detrend_all.csv'
    df_all.to_csv(result_all_file, index=False)

    print('done!')
