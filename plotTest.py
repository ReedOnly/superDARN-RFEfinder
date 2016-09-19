#Plot superDARN fan plot Kristian Reed 10.08.2016


import datetime
import os
import matplotlib.pyplot as plt
from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *

from fanRfe import *

sTime = dt.datetime(2014,12,15,10,1,0,2000)  
rad=['inv']


    
pydarn.plotting.fan.plotFan(sTime,rad, param='velocity',interval=60, fileType='fitacf',
                        scale=[-500,500],coords='mag',gsct=False,fill=True,
                        show=True, png=True,pdf=False,dpi=200)


plt.figure()
plotFanRfe(-71,87,os.getcwd(),sTime,rad, param='velocity',interval=60, fileType='fitacf',
                                scale=[-500,500],coords='mag',gsct=False,fill=True,
                                show=True, png=True,pdf=False,dpi=200)

a=raw_input("Press Enter to continue...")