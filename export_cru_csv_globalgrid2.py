#coding=utf-8
import glob
from netCDF4 import Dataset
import datetime
    
def calculate_month(day):#计算日期所属月份,不要再考虑闰年
    dt=datetime.date(2001,1,1)
    dt2=dt+datetime.timedelta(days=int(day-1))
    return dt2.month
   
def calculate_average(data,time,i,j,start_day,end_day,start_day2,end_day2,grid_dic):
    sum=0
    start_month1=calculate_month(start_day[i][j])#计算玉米生长期的开始月份和结束月份
    end_month1=calculate_month(end_day[i][j])
    if start_month1<=end_month1:#有可能存在开始月份是12月，而结束月份为2月的情况
        plant_month=list(range(start_month1,end_month1+1))
    else:
        plant_month=list(range(start_month1,13))+list(range(1,end_month1+1))
    if str(start_day2[i][j])!='--':#如果有第二个生长期，就计算第二个生长期
        start_month2=calculate_month(start_day2[i][j])
        end_month2=calculate_month(end_day2[i][j])
        if start_month1<=end_month1:
            plant_month.extend(range(start_month2,end_month2+1))
        else:
            plant_month.extend(range(start_month2,13))
            plant_month.extend(range(1,end_month2+1))
        
    years=time//12
    for year in range(years):
        for month in plant_month:#累加每个生长季的数据
            h=year*12+month-1
            sum+=data[h][359-i][j]
        avg=sum/len(plant_month)
        sum=0

        k = '%03d%03d' % (i,j)
        grid_dic.setdefault(k,{})
        grid_dic[k].setdefault(year+1901,[])
        grid_dic[k][year+1901].append(avg)  
        
        

if __name__ == '__main__':
    base_dir = r'F:\crop-climate\cru\*.nc'
    filelist = glob.glob(base_dir)
    grid_dic = {}
    maize_day_ds= Dataset(r'F:\crop-climate\maizedata\phenology\Maize.crop.calendar.fill.nc')
    start_day= maize_day_ds['plant.start']
    end_day=maize_day_ds['plant.end']
    maize_day_ds2= Dataset(r'F:\crop-climate\maizedata\phenology\Maize.2.crop.calendar.fill.nc')
    start_day2= maize_day_ds2['plant.start']
    end_day2=maize_day_ds2['plant.end']

    for filename in filelist:
        factor=filename[-10:-7]
        ds = Dataset(filename)
        data = ds.variables[factor]
        time,nrow,ncol = data.shape

        for i in range(nrow):
            for j in range(ncol):#一个一个栅格的计算
                print(factor,i,j)
                if str(start_day[i][j])=='--' or str(end_day[i][j])=='--':#如果这个地区没有玉米的物候信息，就去下个栅格
                    continue
                if str(data[0][359-i][j])=='--':#如果这个地区没有气象要素数据，就去下个栅格
                    continue
                calculate_average(data,time,i,j,start_day,end_day,start_day2,end_day2,grid_dic)
        ds.close()
    maize_day_ds.close()
    maize_day_ds2.close()

    for grid_id in grid_dic:
        grid_data = grid_dic[grid_id]
        if len(grid_data) <=100:
            continue
        outputfile = r'F:\crop-climate\crucsv/%s.csv' % (grid_id,)
        f = open(outputfile, 'w')
        f.write('Year,Cld,Pre,Tmn,Tmp,Tmx\n')
        for year in range(1901,2017):
            s = '%d,%f,%f,%f,%f,%f\n' % (year,grid_data[year][0],grid_data[year][1],grid_data[year][2],grid_data[year][3],grid_data[year][4])
            f.write(s)          
        f.close()
