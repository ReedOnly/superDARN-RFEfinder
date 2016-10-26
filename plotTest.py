#Plot superDARN fan plot Kristian Reed 10.08.2016


import datetime as dt
import os
import matplotlib.pyplot as plt
from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *

from fanRfe import *

import davitpy.pydarn.plotting.plotMapGrd
import matplotlib.cm as cm

sTime = dt.datetime(2014, 12, 16, 0, 38)  
rad=['inv']


    
#pydarn.plotting.fan.plotFan(sTime,rad, param='velocity',interval=60, fileType='fitacf',
#                        scale=[-500,500],coords='mag',gsct=False,fill=True,
#                        show=False, png=True,pdf=False,dpi=200)


plotFanRfe(-31,76,os.getcwd()+'/',sTime,rad, param='velocity',interval=60, fileType='fitacf',
                                scale=[-500,500],coords='mlt',gsct=False,fill=True,
                                show=False, png=True,pdf=False,dpi=200)




fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
mObj = plotUtils.mapObj(boundinglat=50.,gridLabels=True, coords='mlt',dateTime=sTime)
mapDatObj = davitpy.pydarn.plotting.plotMapGrd.MapConv(sTime, mObj, ax)
#mapDatObj.overlayMapFitVel()
mapDatObj.overlayCnvCntrs()




#a=raw_input("Press Enter to continue...")






#fig.savefig(os.getcwd()+"/convection_los.png",dpi=400)