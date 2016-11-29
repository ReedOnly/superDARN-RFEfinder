#Plot superDARN fan plot Kristian Reed 10.08.2016


import datetime as dt
import os
import matplotlib.pyplot as plt
from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *

from fanRfe import *
from tools import *

import davitpy.pydarn.plotting.plotMapGrd
import matplotlib.cm as cm

newpath=os.getcwd()+'/files/'+datetime.datetime.now().strftime("%Y-%m-%d-%H.%M/")
if not os.path.exists(newpath):
	os.makedirs(newpath)
 
 
 
"""
    World radar day 2014
     ['cly',dt.datetime(2014, 12, 20, 23, 44),4,5],
     ['inv',dt.datetime(2014, 12, 16, 00, 38),24,25],
     ['inv',dt.datetime(2014, 12, 16, 21, 20),4,1],
    
    World radar day 2015
     ['rkn',dt.datetime(2015, 12, 10, 18, 39)],
     ['rkn',dt.datetime(2015, 12, 11, 13, 57)],
     ['rkn',dt.datetime(2015, 12, 12, 13, 36)],
     ['rkn',dt.datetime(2015, 12, 12, 17, 32)],
     ['rkn',dt.datetime(2015, 12, 13, 14, 57)]
     
     ['inv',dt.datetime(2015, 12, 9, 23, 03)],
     
    fitACF
     ['rkn',dt.datetime(2014, 12, 19, 17, 14)],
     ['rkn',dt.datetime(2014, 12, 21, 17, 31)],
     ['cly',dt.datetime(2014, 12, 18, 16, 58)],
     ['cly',dt.datetime(2014, 12, 21, 20, 25)]
"""
 
 
 
 
 
 
 
 

rfe=[['inv',dt.datetime(2014, 12, 16, 00, 38),24,25]]
      

for n in range(len(rfe)):
    element=rfe[n]      
    sTime = element[1]
    rad=[element[0]]
    for t in range(sTime.minute-element[2],sTime.minute+element[3]):
        
        if t >59:
            sTime=sTime.replace(minute=t-60)
            if t==60: sTime=sTime.replace(hour=sTime.hour+1)
        else:
            sTime=sTime.replace(minute=t)
        
        year=sTime.year
        day=sTime.timetuple().tm_yday
        hour=sTime.hour
        minute=sTime.minute
        imf=get_imf(year,day,hour,minute)
        
            
        #pydarn.plotting.fan.plotFan(sTime,rad, param='velocity',interval=60, fileType='fitacf',
                                #scale=[-500,500],coords='mag',gsct=False,fill=True,
                                #show=False, png=True,pdf=False,dpi=200)
        
        
        plotFanRfe(0,0,newpath,imf,sTime,rad, param='velocity',interval=60, fileType='fitex',
                    filtered=False, scale=[-500, 500], channel=None, coords='mlt',
                    colors='lasse', gsct=True, fov=True, edgeColors='face',
                    lowGray=False, fill=True, velscl=1000., legend=True,
                    overlayPoes=False, poesparam='ted', poesMin=-3., poesMax=0.5,
                    poesLabel=r"Total Log Energy Flux [ergs cm$^{-2}$ s$^{-1}$]",
                    overlayBnd=False, show=False, png=True, pdf=False, dpi=200,
                    tFreqBands=[])




#fig = plt.figure(figsize=(10,10))
#ax = fig.add_subplot(111)
#mObj = plotUtils.mapObj(boundinglat=50.,gridLabels=True, coords='mlt',dateTime=sTime)
#mapDatObj = davitpy.pydarn.plotting.plotMapGrd.MapConv(sTime, mObj, ax)
##mapDatObj.overlayMapFitVel()
#mapDatObj.overlayCnvCntrs()




#a=raw_input("Press Enter to continue...")






#fig.savefig(os.getcwd()+"/convection_los.png",dpi=400)