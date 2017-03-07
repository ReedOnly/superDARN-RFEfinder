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

newpath=os.getcwd()+'/files/'+'rfemappe/'
if not os.path.exists(newpath):
	os.makedirs(newpath)
 
 
 
"""
    World radar day 2014
     ['cly',dt.datetime(2014, 12, 20, 23, 44),4,5],         #1
     ['inv',dt.datetime(2014, 12, 16, 00, 38),24,25],       #2
     ['inv',dt.datetime(2014, 12, 16, 21, 20),4,1],         #3
    
    World radar day 2015
     ['rkn',dt.datetime(2015, 12, 10, 18, 39)],         #4
     ['rkn',dt.datetime(2015, 12, 11, 13, 57)],         #5
     ['rkn',dt.datetime(2015, 12, 12, 13, 36)],         #6
     ['rkn',dt.datetime(2015, 12, 12, 17, 32)],         #7
     ['rkn',dt.datetime(2015, 12, 13, 14, 57)]          #8
     
     ['inv',dt.datetime(2015, 12, 9, 23, 03)],          #9
     
     
     
     ['inv',dt.datetime(2014, 12, 15, 0, 41),5,6],         #10
     ['inv',dt.datetime(2014, 12, 18, 21, 43),5,6],         #11
     ['inv',dt.datetime(2014, 12, 20, 19, 34),5,6],         #12
     
     ['rkn',dt.datetime(2014, 12, 15, 0, 29),5,6],         #13
     ['rkn',dt.datetime(2014, 12, 15, 0, 40),5,6],         #14
     ['rkn',dt.datetime(2014, 12, 15, 1, 11),5,6],         #15
     ['rkn',dt.datetime(2014, 12, 17, 15, 0),5,6],         #16
     ['rkn',dt.datetime(2014, 12, 17, 16, 0),5,6],         #17
     ['rkn',dt.datetime(2014, 12, 18, 14, 05),5,6],         #18
     ['rkn',dt.datetime(2014, 12, 20, 17, 26),5,6],         #19
     
     ['cly',dt.datetime(2014, 12, 3, 11, 12),5,6],         #20
     ['cly',dt.datetime(2014, 12, 3, 12, 32),5,6],         #21
     ['cly',dt.datetime(2014, 12, 3, 21, 32),5,6],         #22
     ['cly',dt.datetime(2014, 12, 4, 7, 45),5,6],         #23
     ['cly',dt.datetime(2014, 12, 4, 10, 35),5,6],         #24
     ['cly',dt.datetime(2014, 12, 6, 10, 08),5,6],        #25
     ['cly',dt.datetime(2014, 12, 8, 22, 03),5,6],        #26
     ['cly',dt.datetime(2014, 12, 11, 21, 54),5,6],         #27
     ['cly',dt.datetime(2014, 12, 13, 1, 42),5,6],         #28
     
     ['cly',dt.datetime(2014, 12, 15, 1, 11),5,6],         #29
     ['cly',dt.datetime(2014, 12, 17, 15, 0),5,6],         #30
     ['cly',dt.datetime(2014, 12, 17, 16, 0),5,6],         #31
     ['cly',dt.datetime(2014, 12, 18, 14, 05),5,6],        #32
     ['cly',dt.datetime(2014, 12, 20, 17, 26),5,6],        #33
     
     
     
     
"""
 
 
 
 
 
 
 
 

rfe=[     ['inv',dt.datetime(2014, 12, 15, 0, 41),5,6],         #10
     ['inv',dt.datetime(2014, 12, 18, 21, 43),5,6],         #11
     #['inv',dt.datetime(2014, 12, 20, 19, 34),5,4],         #12
     #['rkn',dt.datetime(2014, 12, 15, 0, 29),4,6],         #13
     #['rkn',dt.datetime(2014, 12, 15, 0, 40),5,6],         #14
     #['rkn',dt.datetime(2014, 12, 15, 1, 11),5,6],         #15
     #['rkn',dt.datetime(2014, 12, 17, 15, 0),5,6],         #16
     #['rkn',dt.datetime(2014, 12, 17, 16, 0),5,6],         #17
     ['rkn',dt.datetime(2014, 12, 18, 14, 05),5,6],         #18
     ['rkn',dt.datetime(2014, 12, 20, 17, 26),5,6],         #19
     ['cly',dt.datetime(2014, 12, 3, 11, 12),5,6],         #20
     ['cly',dt.datetime(2014, 12, 3, 12, 32),5,6],         #21
     ['cly',dt.datetime(2014, 12, 3, 21, 32),5,6],         #22
     ['cly',dt.datetime(2014, 12, 4, 7, 45),5,6],         #23
     ['cly',dt.datetime(2014, 12, 4, 10, 35),5,6],         #24
     ['cly',dt.datetime(2014, 12, 6, 10, 8),5,6],        #25
     ['cly',dt.datetime(2014, 12, 8, 22, 03),5,6],        #26
     ['cly',dt.datetime(2014, 12, 11, 21, 54),5,6],         #27
     ['cly',dt.datetime(2014, 12, 13, 1, 42),5,6]]         #28
      

for n in range(len(rfe)):
    element=rfe[n]      
    sTimeRfe = element[1]
    rad=[element[0]]
    for t in range(-element[2],element[3]):
        sTime= sTimeRfe + dt.timedelta(minutes=t)
        
        year=sTime.year
        day=sTime.timetuple().tm_yday
        hour=sTime.hour
        minute=sTime.minute
        imf=get_imf(year,day,hour,minute)
        
            
#       pydarn.plotting.fan.plotFan(sTime,rad, param='velocity',interval=60, fileType='fitex',
#                                scale=[-500,500],coords='mlt',gsct=False,fill=True,
#                                show=False, png=True,pdf=False,dpi=200)
        
        print sTime
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