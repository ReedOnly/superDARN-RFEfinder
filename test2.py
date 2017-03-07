import datetime as dt
import os
import matplotlib.pyplot as plt
from davitpy import pydarn

from fanRfe import *
from tools import *



sTime=dt.datetime(2014, 12, 16, 00, 38)
rad=['inv']



newpath=os.getcwd()+'/'
year=sTime.year
day=sTime.timetuple().tm_yday
hour=sTime.hour
minute=sTime.minute
imf=get_imf(year,day,hour,minute)

plotFanRfe(0,0,newpath,imf,sTime,rad, param='velocity',interval=60, fileType='fitex',
            filtered=False, scale=[-500, 500], channel=None, coords='mlt',
            colors='lasse', gsct=True, fov=True, edgeColors='face',
            lowGray=False, fill=True, velscl=1000., legend=True,
            overlayPoes=False, poesparam='ted', poesMin=-3., poesMax=0.5,
            poesLabel=r"Total Log Energy Flux [ergs cm$^{-2}$ s$^{-1}$]",
            overlayBnd=False, show=False, png=True, pdf=False, dpi=200,
            tFreqBands=[])