# -*- coding: utf-8 -*-
import pandas as pd
from osgeo import gdal
import numpy as np
import sys

def Read(RasterFile): #读取每个图像的信息     
    ds = gdal.Open(RasterFile)
    if ds is None:
        print('Cannot open ',RasterFile)
        sys.exit(1)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray(0,0,cols,rows)
    return data

def area(i,j):
    sum=0
    num=0
    for h in range(6*i,6*(i+1)):
        for k in range(6*j,6*(j+1)):
            if np.isnan(maizearea[h,k])==False:
                sum+=maizearea[h,k]
                num+=1
    if num==0:
        return 0
    return sum/num

def avg(i,j,n):
    maizesum=0
    areasum=0
    for x in range(i,i+n):
        for y in range(j,j+n):
            grid_id=int('%03d%03d' % (x,y))
            if grid_id in grid_list:
                grid_id='%03d%03d' % (x,y)
                df = pd.read_csv(r'F:\crop-climate\maizecsv/%s.csv' % (grid_id))
                maizesum+=df['Value']*area(x,y)
                areasum+=area(x,y)
    if areasum!=0:
        maizesum=maizesum/areasum
        dataframe=pd.DataFrame({'Year':df['Year']})
        dataframe['Value']=maizesum
        grid_id='%03d%03d' % (i,j)
        dataframe.to_csv(r'F:\crop-climate\maize_scale\360/%s.csv' % (grid_id),index=False)

if __name__ == '__main__':
    df = pd.read_csv(r'F:\crop-climate\maize_scale\grid_id.csv',index_col=False)
    grid_list=df['grid'].tolist()
    maizearea=Read(r'F:\crop-climate\maize_HarvestedAreaFraction.tif')
    for i in range(0,360,720):
        for j in range(0,720,720):
            avg(i,j,720)
                
            