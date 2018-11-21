#coding=utf-8

import pandas as pd
import pylab
import matplotlib.pyplot as plt


if __name__ == '__main__':
    df = pd.read_csv(r'F:\crop-climate\linear relative dominance.csv',index_col=False)
    x=df['scale']
    p1=df['pre1']
    p2=df['pre_low']
    p3=df['pre_high']
    t1=df['tmp1']
    t2=df['tmp_low']
    t3=df['tmp_high']
    


    pylab.plot(x,p1,'ob-')
    pylab.plot(x,t1,'or-')
    plt.fill_between(x,p2,p3,color='b',alpha=0.2)
    plt.fill_between(x,t2,t3,color='r',alpha=0.2)
    
    ax = pylab.gca()
    ax.set_xscale('log')
    pylab.show()