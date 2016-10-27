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

sTime = dt.datetime(2014, 12, 18, 0, 38)  
rad=['inv']

year=sTime.year
day=sTime.timetuple().tm_yday
hour=sTime.hour
minute=sTime.minute
imf=get_imf(year,day,hour,minute)

    
#pydarn.plotting.fan.plotFan(sTime,rad, param='velocity',interval=60, fileType='fitacf',
#                        scale=[-500,500],coords='mag',gsct=False,fill=True,
#                        show=False, png=True,pdf=False,dpi=200)


plotFanRfe(-31,76,os.getcwd()+'/',imf,sTime,rad, param='velocity',interval=60, fileType='fitex',
            filtered=False, scale=[], channel=None, coords='mlt',
            colors='lasse', gsct=True, fov=True, edgeColors='face',
            lowGray=False, fill=True, velscl=1000., legend=True,
            overlayPoes=False, poesparam='ted', poesMin=-3., poesMax=0.5,
            poesLabel=r"Total Log Energy Flux [ergs cm$^{-2}$ s$^{-1}$]",
            overlayBnd=False, show=True, png=False, pdf=False, dpi=400,
            tFreqBands=[])




#fig = plt.figure(figsize=(10,10))
#ax = fig.add_subplot(111)
#mObj = plotUtils.mapObj(boundinglat=50.,gridLabels=True, coords='mlt',dateTime=sTime)
#mapDatObj = davitpy.pydarn.plotting.plotMapGrd.MapConv(sTime, mObj, ax)
##mapDatObj.overlayMapFitVel()
#mapDatObj.overlayCnvCntrs()




#a=raw_input("Press Enter to continue...")






#fig.savefig(os.getcwd()+"/convection_los.png",dpi=400)