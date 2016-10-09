#superDARN rfe plotter        Kristian reed 09.08.2016
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
from secondsToStr import *
from fanRfe import *
import time




SaveXlsx=False      #Save as .xlsx spreadsheet
SaveNpy=False        #Save as .npy file
RFEplot=False        #Make RFE plot
fanPlot=True

timerS=time.clock()


#Loading stored file
#filedir=raw_input('Numpy file to load: ')
rfe=load(os.getcwd()+'/data.npy')#15dec2014.npy
newpath=os.getcwd()+'/'

        
pandasRfe=pd.DataFrame(rfe,columns=['Site','Beam','Gate','RelVel','RadLength','Lat(mag)','Lon(mag)','Time'])
        
    
#Output result
print 'Number of rfe :',len(rfe)
print pandasRfe[['Time','Site','Beam','Gate','RelVel','RadLength']]




#Creating map with RFE
if RFEplot:
    plt.figure(figsize=(9,9))
    width = 111e3*60
    m = plotUtils.mapObj(width=width, height=width, lat_0=90., lon_0=60, coords='mag')
    # Plotting some radars
    overlayRadar(m, fontSize=12, codes=['inv','rkn','cly'])
    # Plot radar fov
    overlayFov(m, codes=['inv','rkn','cly'], maxGate=70, beams=[])#0,6,11,12,13,15
    #Add RFE points
    for i in range(len(rfe)):
        #Coordinates in map projection
        x,y=m(rfe[i,6],rfe[i,5])
        #x,y=lon,lat
        m.scatter(x, y, s=80, marker='o', facecolors='none', edgecolors='r', zorder=2)
    
    pylab.savefig(newpath+str(sTime.strftime("%Y-%m-%d-%H%M.png")))
    print 'Saved rfe plot'
    #plt.show()
    


#Produce .npy file
if SaveNpy:
    save(newpath+str(sTime.strftime("%Y-%m-%d-%H%M.npy")),rfe)
    print 'Saved .npy file'
    
#Produce .xlsx file
if SaveXlsx:
    pandasRfe.to_excel(newpath+str(sTime.strftime("%Y-%m-%d-%H%M.xlsx")))
    print 'Saved .xlsx file'


#plotFanRfe(lon,lat,newpath,sTime, rad, interval=60, fileType='fitex', param='velocity',
#            filtered=False, scale=[], channel=None, coords='geo',
#            colors='lasse', gsct=False, fov=True, edgeColors='face',
#            lowGray=False, fill=True, velscl=1000., legend=True,
#            overlayPoes=False, poesparam='ted', poesMin=-3., poesMax=0.5,
#            poesLabel=r"Total Log Energy Flux [ergs cm$^{-2}$ s$^{-1}$]",
#            overlayBnd=False, show=True, png=False, pdf=False, dpi=500,
#            tFreqBands=[]):
if fanPlot and len(rfe)>1:    
    for i in range(len(rfe)):#len(rfe)
        print '***Plot ',i,' out of ',len(rfe),'   ',secondsToStr(time.clock()-timerS),'***'
        plotFanRfe(rfe[i,6],rfe[i,5],newpath,rfe[i,7],[rfe[i,0]], param='velocity',interval=60, fileType='fitacf',
                                scale=[-500,500],coords='mag',gsct=False,fill=True,
                                show=False, png=True,pdf=False,dpi=200)
    print 'Saved fan plot figures'
    
timerE=time.clock()
print 'Total time used: '+secondsToStr(timerE-timerS)
    
    