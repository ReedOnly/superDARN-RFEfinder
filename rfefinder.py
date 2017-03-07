#superDARN rfe plotter        Kristian reed 09.08.2016
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *

import os
import datetime as dt

import matplotlib.pyplot as plt
from matplotlib import *
from scipy import *
import pandas as pd

from sdread import *
from tools import *
from fanRfe import *
from mltplot import *
import time




#sTime = dt.datetime(2014, 9, 15, 00)       
#eTime = dt.datetime(2014, 12, 22, 00) 


#Initializing
sTime = dt.datetime(2014, 12, 16, 0)        #Scanning start Time
eTime = dt.datetime(2015, 1, 15, 0)     #Scanning end time
radars=['han']  #'inv','rkn'  , 'cly'            #Radars to scan

rfelist=array([['cly',dt.datetime(2014, 12, 20, 23, 44)],
     ['inv',dt.datetime(2014, 12, 16, 00, 38)],
     ['inv',dt.datetime(2014, 12, 16, 21, 20)],
     ['rkn',dt.datetime(2015, 12, 10, 18, 39)],
     ['rkn',dt.datetime(2015, 12, 11, 13, 57)],
     ['rkn',dt.datetime(2015, 12, 12, 13, 36)],
     ['rkn',dt.datetime(2015, 12, 12, 17, 32)],
     ['rkn',dt.datetime(2015, 12, 13, 14, 57)],
     ['inv',dt.datetime(2015, 12, 9, 23, 03)]])
      

LoadFile=False  #True for local RFE file
SaveScratch=False	#Save in /scratch folder
SaveXlsx=True     #Save as .xlsx spreadsheet
SaveNpy=True        #Save as .npy file
RFEplot=True        #Make RFE plot
fanPlot=True

timerS=time.clock()

#Make path for storage
if SaveScratch:
	newpath='/scratch/rfeFiles/'+datetime.datetime.now().strftime("%Y-%m-%d-%H.%M/")
else:
	newpath=os.getcwd()+'/files/'+datetime.datetime.now().strftime("%Y-%m-%d-%H.%M/")

if not os.path.exists(newpath):
	os.makedirs(newpath)

#Loading stored file
if LoadFile: rfe=load(os.getcwd()+'/files/'+'lyr/data.npy')#15dec2014.npy

#Loading data and finding RFE
if not LoadFile:
    rfe=array([[0,0,0,0,0,0,0,0,0]])
    for rad in radars:         #Uncomment for normal run!
    #for n in range(len(rfelist)):    #Comment out for normal run!
        save(newpath+'data.npy',rfe)          #Save for every radar in case it stops
        timerSTmp=time.clock()
        rfeTmp=array([[0,0,0,0,0,0,0,0,0]])
        
        rfeTmp=sdread(rfeTmp,rad,sTime,eTime)      #Uncomment for normal run!
        #event=rfelist[n]            #Comment out for normal run!
        #rfeTmp=sdread(rfeTmp,event[0],event[1],event[1]+datetime.timedelta(minutes=1))   #Comment out for normal run!
        
        rfeTmp = delete(rfeTmp, 0, axis=0)
        rfe = append(rfe,rfeTmp,axis=0)
        timerETmp=time.clock()
        print 'Time used for '+str(radars)+': '+secondsToStr(timerETmp-timerSTmp)
    
    if len(rfe)>1:
        rfe = delete(rfe, 0, axis=0)
        
pandasRfe=pd.DataFrame(rfe,columns=['Site','Beam','Gate','Lon(MLT)','MLT','Lat(mag)','Lon(mag)','IMF','Time'])
        
    
#Output result
print pandasRfe[['Time','Site','Beam','Gate','MLT', 'IMF']]
print 'Time used: '+secondsToStr(time.clock()-timerS)




#Creating map with RFE
if RFEplot:
    plt.figure(figsize=(9,9))
    #plt.title(str(radars)+' from '+sTime.strftime("%Y.%m.%d %H:%M")+' until '+ eTime.strftime("%H:%M UTC"),fontsize="x-large")
    width = 111e3*60
    m = plotUtils.mapObj(width=width, height=width, lat_0=90., lon_0=60, coords='mag')
    # Plotting some radars
    overlayRadar(m, fontSize=30, codes=['inv','rkn','cly'])#'lyr'
    # Plot radar fov
    overlayFov(m, codes=['inv','rkn','cly'], maxGate=70, beams=[])#0,6,11,12,13,15 'inv','rkn','cly'
    #Add RFE points
    for i in range(len(rfe)):
        #Coordinates in map projection
        x,y=m(rfe[i,6],rfe[i,5])
        #x,y=lon,lat
        m.scatter(x, y, s=2, linewidths=2, color='r', zorder=2)
    
    pylab.savefig(newpath+str(sTime.strftime("%Y-%m-%d-%H%M.png")),dpi=400)
    print 'Saved rfe plot'
    #plt.show()
    
    #Make MLT plot
    mlat=array(rfe[:,5],dtype=float)
    mlt=array(rfe[:,4],dtype=float)
    mltplot(newpath,sTime,eTime,radars,mlat,mlt)


#Produce .npy file
if SaveNpy:
    save(newpath+'data.npy',rfe)
    print 'Saved .npy file'
    
#Produce .xlsx file
if SaveXlsx:
    pandasRfe.to_excel(newpath+str(sTime.strftime("%Y-%m-%d-%H%M.xlsx")))
    print 'Saved .xlsx file'


#plotFanRfe(lon,lat,newpath,imf,sTime, rad, interval=60, fileType='fitex', param='velocity',
#            filtered=False, scale=[], channel=None, coords='geo',
#            colors='lasse', gsct=False, fov=True, edgeColors='face',
#            lowGray=False, fill=True, velscl=1000., legend=True,
#            overlayPoes=False, poesparam='ted', poesMin=-3., poesMax=0.5,
#            poesLabel=r"Total Log Energy Flux [ergs cm$^{-2}$ s$^{-1}$]",
#            overlayBnd=False, show=True, png=False, pdf=False, dpi=500,
#            tFreqBands=[]):
if fanPlot and len(rfe)>1:    
    for i in range(len(rfe)):#len(rfe)
        #i=-5+n
        print '***Plot ',i,' out of ',len(rfe)-1,'   ',secondsToStr(time.clock()-timerS),'***'
        plotFanRfe(rfe[i,3],rfe[i,5],newpath,rfe[i,7],rfe[i,8],[rfe[i,0]], param='velocity',interval=60, fileType='fitex',
                                scale=[-500,500],coords='mlt',gsct=True,fill=True,overlayPoes=False,
                                show=False, png=True,pdf=False,dpi=200)
        print 'time used: '+ secondsToStr(time.clock()-timerS)
    print 'Saved fan plot figures'
    
timerE=time.clock()
print 'Total time used: '+secondsToStr(timerE-timerS)
    
    
