#Code used for finding RFEs and making the plots used in the Master Theisis of Kristian Reed
#Written by Kristian Reed 10.06.2017


import datetime as dt
import os
import matplotlib.pyplot as plt
from davitpy import pydarn
from fanRfe import *
from tools import *


sTime=dt.datetime(2014, 12, 13, 0, 21)
rad=['cly']



newpath=os.getcwd()+'/files/'
year=sTime.year
day=sTime.timetuple().tm_yday
hour=sTime.hour
minute=sTime.minute
imf=get_imf(sTime)

plotFanRfe(0,0,newpath,imf,sTime,rad, param='velocity',interval=60, fileType='fitex',
            filtered=False, scale=[-500, 500], channel=None, coords='mlt',
            colors='lasse', gsct=True, fov=True, edgeColors='face',
            lowGray=False, fill=True, velscl=1000., legend=True,
            overlayPoes=False, poesparam='ted', poesMin=-3., poesMax=0.5,
            poesLabel=r"Total Log Energy Flux [ergs cm$^{-2}$ s$^{-1}$]",
            overlayBnd=False, show=False, png=False, pdf=True, dpi=200,
            tFreqBands=[])


#pydarn.plotting.fan.plotFan(sTime,rad, param='velocity',interval=60, fileType='fitex',
#                            scale=[-500,500],coords='mlt',gsct=False,fill=True,
#                            show=False, png=True,pdf=True,dpi=200)