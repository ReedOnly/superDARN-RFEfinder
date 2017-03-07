#superDARN rfe plotter        Kristian reed 09.08.2016

#Put this file in same folder as .npy file to plot the RFE which is stored there
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *


import os, sys
sys.path.append('../..')
import datetime as dt

import matplotlib.pyplot as plt
from matplotlib import *
from scipy import *
import pandas as pd
from tools import *
from fanRfe import *
import time



timerS=time.clock()


#Loading stored file
#filedir=raw_input('Numpy file to load: ')
rfe=load(os.getcwd()+'/data.npy')#15dec2014.npy
newpath=os.getcwd()+'/'

        
pandasRfe=pd.DataFrame(rfe,columns=['Site','Beam','Gate','Lon(MLT)','MLT','Lat(mag)','Lon(mag)','IMF','Time'])
        
    
#Output result
print 'Number of rfe :',len(rfe)
print pandasRfe[['Time','Site','Beam','Gate','MLT', 'IMF']]



if len(rfe)>1:    
    for i in range(len(rfe)):#len(rfe)
	#if i==71: continue	#Remove rfe if error while plotting
        print '***Plot ',i,' out of ',len(rfe),'   ',secondsToStr(time.clock()-timerS),'***'
        plotFanRfe(rfe[i,3],rfe[i,5],newpath,rfe[i,7],rfe[i,8],[rfe[i,0]], param='velocity',interval=60, fileType='fitex',
                                scale=[-500,500],coords='mlt',gsct=True,fill=True,overlayPoes=False,
                                show=False, png=True,pdf=False,dpi=200)
        print 'time used: '+ secondsToStr(time.clock()-timerS)
    print 'Saved fan plot figures'
    
timerE=time.clock()
print 'Total time used: '+secondsToStr(timerE-timerS)
