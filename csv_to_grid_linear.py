#coding=utf-8
import os
import pandas as pd
import numpy as np
from osgeo import gdal

def output_tiff(df, val_index, nrow, ncol, nodata_value):
    data = np.zeros((nrow, ncol))
    data[:] = nodata_value
    for index, row in df.iterrows():
        pos = str(int(row[0]))
        irow = int(pos[:-3])
        icol = int(pos[-3:])
        data[irow][icol] = row[val_index]
    
    file_name = r'F:\crop-climate\TIFF\maize_polyfit_%d.tiff' % (val_index,)
    #file_name = 'maize_decade_%d.tiff' % (val_index,)
    if os.path.exists(file_name):
        os.remove(file_name)
    driver = gdal.GetDriverByName("GTiff")
    ds_out = driver.Create(file_name, ncol, nrow, 1, gdal.GDT_Float32)#1是波段数
    band_out = ds_out.GetRasterBand(1)
    band_out.SetNoDataValue(nodata_value)
    band_out.WriteArray(data)
    ds_out.FlushCache()
    ds_out = None

if __name__ == '__main__':
    nrow, ncol = 360, 720
    nodata_value = -9999

    csvfile = r'F:\crop-climate\regression\mlr\polyfit-additive.csv'
    df = pd.read_csv(csvfile,index_col=False)

    for val_index in [2,3,4]:
        print(val_index)
        output_tiff(df, val_index, nrow, ncol, nodata_value)


