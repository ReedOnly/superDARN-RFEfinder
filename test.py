

from davitpy import pydarn
import davitpy.pydarn.sdio
from davitpy.pydarn.plotting import *
from davitpy.utils import *


import datetime as dt
from pylab import gca
import matplotlib.pyplot as plt
from matplotlib import *
from scipy import *
import pandas as pd
import time

a=random.random((10, 10))






sTime = dt.datetime(2014,12,15,13,59)        #Scanning start Time
eTime = dt.datetime(2014,12,15,14,10)         #Scanning end time
rad='rkn'


#Radar parameters
channel=None
bmnum=None
cp=None
fileType='fitacf'
filtered=False
src=None
count=0

#Fetching data
myPtr = pydarn.sdio.radDataOpen(sTime,rad,eTime=eTime,channel=channel,
                                bmnum=bmnum,cp=cp,fileType=fileType,
                                filtered=filtered, src=src)

myScan = pydarn.sdio.radDataReadScan(myPtr)

#Go through all scans in the time interval
while(myScan!=None):
    print myScan[0].time
    #plt.figure(figsize=(9,9))
    
    nbeams=len(myScan)#number of beams
    print 'number of beams: '+ str(nbeams)
    
    nrangs=myScan[0].prm.nrang#Number of gates
    
    
    
    velMatrix=zeros((nrangs,nbeams))
    
    for beam in range(nbeams):  #Iterate through all beams to add velicities
        print myScan[beam].prm.nrang
        gates=array(myScan[beam].fit.slist)
        print gates
        #if not myScan[beam].fit.v: print 'empty beam';continue
        velocity=array(myScan[beam].fit.v)
        
        for gate in range(len(gates)):
            velMatrix[gates[gate],beam]=velocity[gate]

    velMatrix[velMatrix>1200]=1200
    velMatrix[velMatrix<-1200]=-1200
    plt.imshow(velMatrix,cmap=plt.get_cmap('jet'),interpolation='nearest',aspect='auto')
    plt.colorbar()
    plt.show()

    myScan = pydarn.sdio.radDataReadScan(myPtr)

myPtr = pydarn.sdio.radDataOpen(sTime,rad,eTime=eTime,channel=channel,
                                bmnum=bmnum,cp=cp,fileType=fileType,
                                filtered=filtered, src=src)

myScan = pydarn.sdio.radDataReadScan(myPtr)
print myScan[0].fit.slist