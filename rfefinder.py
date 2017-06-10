#Script for searching and plotting RFEs from SuperDARN data
#Written by Kristian Reed 10.06.2017

import matplotlib
matplotlib.use('Agg')
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




#Initializing
sTime = dt.datetime(2016, 12, 4, 1, 40)        #Scanning start Time
eTime = dt.datetime(2016, 12, 4, 6, 0)         #Scanning end time
radars=['lyr']  #'inv','rkn'  , 'cly'          #Radars to scan

LoadFile=False          #True for local RFE file
SaveXlsx=True           #Save as .xlsx spreadsheet
SaveNpy=True            #Save as .npy file
RFEplot=True            #Make RFE plot
fanPlot=True







#####################################################################
#Code needed to run program, dont touch unless you know what you do!
#####################################################################

timerS=time.clock()

#Make path for storage
newpath=os.getcwd()+'/files/'+datetime.datetime.now().strftime("%Y-%m-%d-%H.%M/")

if not os.path.exists(newpath):
	os.makedirs(newpath)

#Loading stored file
if LoadFile: rfe=load(os.getcwd()+'/files/'+'lyr/data.npy')

#Loading data and finding RFE
if not LoadFile:
    rfe=array([[0,0,0,0,0,0,0,0,0]])
    for rad in radars:
        save(newpath+'data.npy',rfe)
        timerSTmp=time.clock()
        rfeTmp=array([[0,0,0,0,0,0,0,0,0]])       
        rfeTmp=sdread(rfeTmp,rad,sTime,eTime)        
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
    overlayFov(m, codes=['inv','rkn','cly','lyr'], maxGate=70, beams=[])#0,6,11,12,13,15 'inv','rkn','cly'
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
    timeEvents=rfe[:,8]
    imf=rfe[:,7]
    mltplot2(newpath,timeEvents,imf,radars,mlat,mlt)

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
                                show=False, png=False,pdf=True,dpi=200)
        print 'time used: '+ secondsToStr(time.clock()-timerS)
    print 'Saved fan plot figures'
    
timerE=time.clock()
print 'Total time used: '+secondsToStr(timerE-timerS)
    
    
